import base64
import datetime  # 為時間戳目錄添加
import json
import os
import random
import threading
import time
import uuid
from io import BytesIO
from random import randint

import boto3
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from dotenv import load_dotenv
from images.prompt_agent import ask_agent
from PIL import Image, ImageDraw
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import IMAGE_GENERATION_PARAMS  # 導入常量
from .models import Image as ImageModel
from .models import ImageCategory
from .serializers import ImageCategorySerializer, ImageSerializer
from .tool import _parse_input, generate_prompt_from_json  # 導入工具函數

# 讀取 .env 檔
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "us-east-1")

# 確保 MEDIA_ROOT 和必要目錄存在
try:
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "generated"), exist_ok=True)
    print(f"確保 MEDIA_ROOT 目錄存在: {settings.MEDIA_ROOT}")
except Exception as e:
    print(f"創建 MEDIA_ROOT 目錄時出錯: {e}")

# 設置AWS認證 (如果.env未設置)
if not os.getenv("AWS_ACCESS_KEY_ID"):
    print("環境中未找到AWS認證，使用硬編碼憑證")
    os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
    os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
    os.environ["AWS_REGION_NAME"] = "us-east-1"


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer


class ImageCategoryViewSet(viewsets.ModelViewSet):
    queryset = ImageCategory.objects.all()
    serializer_class = ImageCategorySerializer


class BedrockAgentView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "缺少 prompt"}, status=400)

        answer = ask_agent(prompt, session_id=request.session.session_key)
        return _parse_input({"answer": answer})


# View for handling reference image uploads
@api_view(["POST"])
def upload_reference_image(request):
    if "image" not in request.FILES:
        return Response(
            {"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    file = request.FILES["image"]
    # Define the path RELATIVE to MEDIA_ROOT where the file will be saved
    # e.g., MEDIA_ROOT/uploads/filename.png
    save_dir = "uploads"
    filename = os.path.join(save_dir, default_storage.get_valid_name(file.name))

    try:
        # Ensure the target directory inside MEDIA_ROOT exists
        # default_storage.save will typically handle directory creation
        # if using FileSystemStorage, but explicit check can be good.
        full_dir_path = os.path.join(settings.MEDIA_ROOT, save_dir)
        os.makedirs(full_dir_path, exist_ok=True)

        # Save the file using Django's default storage.
        # It will automatically save relative to MEDIA_ROOT.
        saved_name = default_storage.save(filename, file)
        print(
            f"File saved as: {saved_name} (relative to MEDIA_ROOT: {settings.MEDIA_ROOT})"
        )

        # Construct the URL using MEDIA_URL
        file_url = os.path.join(settings.MEDIA_URL, saved_name).replace(
            "\\", "/"
        )  # Ensure forward slashes for URL

        return Response(
            {
                "message": "File uploaded successfully",
                "fileUrl": file_url,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        print(f"Error saving file: {e}")
        return Response(
            {"error": "Could not save file."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def save_image_to_s3(base64_data: str, relative_path: str) -> str:
    # relative_path 範例： "generated/from_agent.png"
    decoded = base64.b64decode(base64_data)
    path = default_storage.save(relative_path, ContentFile(decoded))
    # default_storage.url 會回傳 S3 上的可存取 URL
    return default_storage.url(path)


def save_image(base64_data: str, relative_path: str) -> str:
    save_dir = os.path.join(settings.MEDIA_ROOT, "generated")
    os.makedirs(save_dir, exist_ok=True)
    filename = relative_path.lstrip("/")
    image_path = os.path.join(save_dir, filename)
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(base64_data))
    return image_path


class AgentGenerateImageView(APIView):
    """
    一支 API 同時：
     1. 呼叫 Agent (ask_agent) → 拿到 JSON answer（字串）
     2. 解析 JSON、產出真正的文字 Prompt
     3. 丟給 Bedrock 產圖、存檔，並回傳可存取的 URL
    """

    def post(self, request):
        # 1. 取得前端傳來的 prompt
        user_prompt = request.data.get("prompt")
        if not user_prompt:
            return Response({"error": "缺少 prompt"}, status=400)

        # 2. 呼叫你的 agent
        raw_answer = ask_agent(user_prompt, session_id=request.session.session_key)

        # 3. 解析 agent 回傳的 JSON，並組出最終要給 Bedrock 的文字 prompt
        try:
            container = json.dumps({"answer": raw_answer})
            image_prompt = generate_prompt_from_json(container)
        except ValueError as e:
            return Response({"error": f"解析 Agent JSON 失敗：{e}"}, status=400)

        # 4. 呼叫 Bedrock 產圖
        try:
            bedrock = boto3.client(
                "bedrock-runtime",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION_NAME", "us-east-1"),
            )
            payload = {
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {"text": image_prompt},
                "imageGenerationConfig": {
                    "width": 1024,
                    "height": 1024,
                    "quality": "standard",
                    "cfgScale": 6.5,
                    "seed": 42,
                    "numberOfImages": 4,
                },
            }
            resp = bedrock.invoke_model(
                modelId="amazon.nova-canvas-v1:0",
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload),
            )
            data = json.loads(resp["body"].read())
        except Exception as e:
            return Response({"error": f"Bedrock 呼叫失敗：{e}"}, status=500)

        # 5. 取出 Base64 圖片、存檔，回傳 URL
        images = data.get("images") or []
        if not images:
            return Response({"error": data.get("error", "Unknown error")}, status=500)
        unique_filename = f"from_agent_{uuid.uuid4().hex}.png"
        s3_key = f"generated/{unique_filename}"

        # 存檔並回傳 MEDIA_URL 下的檔案路徑
        save_dir = os.path.join(settings.MEDIA_ROOT, "generated")
        os.makedirs(save_dir, exist_ok=True)
        filename = unique_filename
        full_path = os.path.join(save_dir, filename)
        with open(full_path, "wb") as f:
            f.write(base64.b64decode(images[0]))
        save_image_to_s3(images[0], filename)
        file_url = save_image_to_s3(images[0], s3_key)
        return Response({"fileUrl": file_url}, status=200)


def create_mask(mode: int) -> bytes:
    """創建遮罩圖像"""
    mask = Image.new("L", (1024, 1024), 0)
    draw = ImageDraw.Draw(mask)
    if mode == 0:
        draw.rectangle([171, 53, 908, 914], fill=255)
    elif mode == 1:
        draw.rectangle([529, 53, 839, 930], fill=255)
    elif mode == 2:
        draw.rectangle([182, 59, 568, 906], fill=255)
    else:
        raise ValueError(f"Unsupported mode: {mode}")
    buf = BytesIO()
    mask.save(buf, format="PNG")
    return buf.getvalue()


def image_to_base64(path: str) -> str:
    """將圖片轉換為 base64 編碼"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# 全局字典用於存儲生成任務狀態
# 格式: { 'task_id': { 'urls': [url1, url2, ...], 'status': 'processing|completed', 'timestamp': datetime } }
generation_tasks = {}


# 新增 API 視圖 - 使用用戶選擇生成圖像
class GenerateImagesView(APIView):
    """
    API 端點，用於:
    1. 接收前端的用戶選擇參數
    2. 立即生成第一張圖片並回應前端
    3. 背景處理剩餘三張圖片
    4. 提供查詢API讓前端能確認生成進度
    """

    def post(self, request):
        # 1. 獲取前端傳來的選擇
        user_selections = request.data.get("userSelections")
        mask_mode_value = request.data.get("mask_mode", 0)
        print(f"接收到的 mask_mode: {mask_mode_value}")

        if not user_selections or not isinstance(user_selections, dict):
            return Response({"error": "缺少或無效的用戶選擇"}, status=400)

        # 2. 組合 prompt 數據 (保持不變)
        try:
            data_for_prompt = {
                "style": user_selections.get("style", "minimalistic"),
                "chassis_frame": user_selections.get("chassis_frame", "aluminum frame"),
                "front_panel": {
                    "material": IMAGE_GENERATION_PARAMS.get(
                        "front_material", "brushed aluminum"
                    ),
                    "layout": user_selections.get(
                        "front_layout", "minimalist front panel"
                    ),
                    "features": [
                        IMAGE_GENERATION_PARAMS.get("features_block", "RGB lighting")
                    ],
                },
                "side_panel": {
                    "type": user_selections.get(
                        "side_type", "tempered glass side panel"
                    ),
                    "frame": IMAGE_GENERATION_PARAMS.get("side_frame", "aluminum trim"),
                    "interior_view": user_selections.get(
                        "interior_view", "high-end components"
                    ),
                },
                "view_settings": {
                    "angle": IMAGE_GENERATION_PARAMS.get(
                        "angle", "front-left 3/4 view"
                    ),
                    "camera_height": IMAGE_GENERATION_PARAMS.get(
                        "camera_height", "camera angle 45 degrees"
                    ),
                    "lighting": user_selections.get(
                        "lighting_conditions", "product photography lighting"
                    ),
                },
            }
            json_input_str = json.dumps(data_for_prompt)
        except Exception as e:
            return Response({"error": f"準備 prompt 數據時出錯: {e}"}, status=500)

        # 3. 生成 prompt (保持不變)
        try:
            image_prompt = generate_prompt_from_json(json_input_str)
            print("--- 生成的 Bedrock Prompt ---")
            print(image_prompt)
            print("------------------------------")
        except ValueError as e:
            return Response({"error": f"從 JSON 生成 prompt 失敗: {e}"}, status=400)
        except Exception as e:
            return Response({"error": f"生成 prompt 時出錯: {e}"}, status=500)

        # 4. 檢查並加載 cosmos 圖片
        source_b64 = None  # 初始化
        try:
            possible_paths = [
                os.path.join(settings.MEDIA_ROOT, "cosmos", "cosmos.jpg"),
                # ... 其他路徑 ...
                "W:/hackathon/hackathon_web/backend/media/cosmos/cosmos.jpg",
                "/w:/hackathon/hackathon_web/backend/media/cosmos/cosmos.jpg",
            ]
            cosmos_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    cosmos_path = path
                    print(f"找到 cosmos.jpg: {cosmos_path}")
                    break
            if cosmos_path is None:
                print("錯誤：找不到 cosmos.jpg 文件。")
                return Response({"error": "找不到 cosmos.jpg 圖片"}, status=500)

            # 加載源圖像為 base64
            print(f"加載源圖像 {cosmos_path}...")
            source_b64 = image_to_base64(cosmos_path)
            print(f"源圖像 base64 (前 50 字元): {source_b64[:50]}...")
        except Exception as e:
            print(f"檢查或加載 cosmos 圖片時出錯：{e}")
            return Response({"error": f"處理 cosmos 圖片失敗: {str(e)}"}, status=500)

        # 5. 創建時間戳目錄和任務ID
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        task_id = f"task_{timestamp_str}_{uuid.uuid4().hex[:8]}"
        relative_save_dir = os.path.join("generated", timestamp_str)
        absolute_save_dir = os.path.join(settings.MEDIA_ROOT, relative_save_dir)
        try:
            os.makedirs(absolute_save_dir, exist_ok=True)
        except Exception as dir_err:
            print(f"創建時間戳目錄失敗: {dir_err}")
            return Response({"error": f"無法創建輸出目錄: {dir_err}"}, status=500)

        # 6. 初始化任務狀態
        generation_tasks[task_id] = {
            "urls": [None, None, None, None],  # 四張圖的URL
            "status": "processing",  # 狀態：processing 或 completed
            "timestamp": datetime.datetime.now(),
            "task_data": {  # 存儲生成所需數據
                "image_prompt": image_prompt,
                "source_b64": source_b64,
                "mask_mode_value": mask_mode_value,
                "relative_save_dir": relative_save_dir,
                "absolute_save_dir": absolute_save_dir,
                "timestamp_str": timestamp_str,
            },
        }

        # 7. 生成第一張圖片
        try:
            print(f"\n--- 開始生成第 1 張圖片 (Outpainting) ---")
            first_image_url = self._generate_single_image(
                task_id=task_id, image_index=0
            )

            # 啟動背景線程處理剩餘圖片
            thread = threading.Thread(
                target=self._background_process_remaining_images, args=(task_id,)
            )
            thread.daemon = True
            thread.start()

            # 立即回應前端第一張圖片
            return Response(
                {
                    "fileUrls": [first_image_url],  # 只回傳第一張圖片URL
                    "taskId": task_id,  # 回傳任務ID供後續查詢
                    "message": "已生成第一張圖片，其餘三張正在背景處理",
                },
                status=200,
            )

        except Exception as e:
            print(f"生成第一張圖片時發生錯誤: {e}")
            # 標記任務失敗
            if task_id in generation_tasks:
                generation_tasks[task_id]["status"] = "failed"
                generation_tasks[task_id]["error"] = str(e)
            return Response({"error": f"生成圖片失敗: {str(e)}"}, status=500)

    def _generate_single_image(self, task_id, image_index):
        """生成單張圖片，返回URL"""
        task_data = generation_tasks[task_id]["task_data"]
        image_prompt = task_data["image_prompt"]
        source_b64 = task_data["source_b64"]
        mask_mode_value = task_data["mask_mode_value"]
        timestamp_str = task_data["timestamp_str"]
        absolute_save_dir = task_data["absolute_save_dir"]
        relative_save_dir = task_data["relative_save_dir"]

        # 創建mask
        mask_bytes = create_mask(mask_mode_value)
        mask_b64 = base64.b64encode(mask_bytes).decode("utf-8")

        # 使用隨機種子
        current_seed = randint(1, 858993459)
        print(f"使用種子: {current_seed}")

        # 調用API生成圖片
        result = attempt_real_api_call(
            image_prompt, seed=current_seed, mask_b64=mask_b64, source_b64=source_b64
        )

        # 處理結果
        if (
            result
            and "images" in result
            and result["images"]
            and len(result["images"]) == 1
        ):
            img_b64 = result["images"][0]
            filename = f"{timestamp_str}_{image_index+1}.png"
            full_path = os.path.join(absolute_save_dir, filename)
            relative_path = os.path.join(relative_save_dir, filename).replace("\\", "/")

            # 保存圖片到本地
            decoded_image = base64.b64decode(img_b64)
            with open(full_path, "wb") as f:
                f.write(decoded_image)
            print(f"圖片已保存到本地: {full_path}")

            # 根據環境獲取URL
            file_url = None
            if settings.DEBUG:
                media_url = settings.MEDIA_URL
                if not media_url.endswith("/"):
                    media_url += "/"
                file_url = f"{media_url}{relative_path.lstrip('/')}"
            else:
                try:
                    s3_path = default_storage.save(
                        relative_path, ContentFile(decoded_image)
                    )
                    file_url = default_storage.url(s3_path)
                except Exception as s3_err:
                    print(f"保存到 S3 失敗: {s3_err}")
                    raise s3_err

            # 更新任務狀態
            generation_tasks[task_id]["urls"][image_index] = file_url
            return file_url
        else:
            error_msg = f"第 {image_index+1} 張圖片 Bedrock API (Outpainting) 調用失敗或未返回有效圖像。"
            if result and "error" in result:
                error_msg += f" 錯誤信息: {result.get('error', '未知錯誤')}"
            print(error_msg)
            raise Exception(error_msg)

    def _background_process_remaining_images(self, task_id):
        """背景處理剩餘三張圖片"""
        try:
            # 處理後三張圖 (索引 1,2,3)
            for i in range(1, 4):
                print(f"\n--- 後台處理：開始生成第 {i+1} 張圖片 ---")
                try:
                    self._generate_single_image(task_id, i)
                    # 短暫暫停，避免 Bedrock API 速率限制
                    time.sleep(1)
                except Exception as e:
                    print(f"生成第 {i+1} 張圖片時出錯: {e}")
                    generation_tasks[task_id]["urls"][i] = None

            # 全部完成，更新狀態
            generation_tasks[task_id]["status"] = "completed"
            print(
                f"任務 {task_id} 全部完成，共生成 {len([u for u in generation_tasks[task_id]['urls'] if u])} 張圖片"
            )

        except Exception as e:
            print(f"背景處理圖片時發生錯誤: {e}")
            generation_tasks[task_id]["status"] = "partial"
            generation_tasks[task_id]["error"] = str(e)

    def get(self, request):
        """查詢生成任務狀態"""
        task_id = request.query_params.get("taskId")
        if not task_id or task_id not in generation_tasks:
            return Response({"error": "找不到指定的任務ID"}, status=404)

        task = generation_tasks[task_id]

        # 計算任務運行時間
        elapsed_time = (datetime.datetime.now() - task["timestamp"]).total_seconds()

        # 如果任務狀態為處理中 且 已超過 30 秒，但至少有一張圖片
        valid_urls = [url for url in task["urls"] if url]
        if task["status"] == "processing" and elapsed_time > 30 and valid_urls:
            return Response(
                {
                    "fileUrls": valid_urls,
                    "status": "partial",
                    "message": "部分圖片已生成，其餘仍在處理中",
                    "total": len(valid_urls),
                }
            )

        # 任務完成或失敗
        if task["status"] in ["completed", "failed", "partial"]:
            return Response(
                {
                    "fileUrls": [url for url in task["urls"] if url],
                    "status": task["status"],
                    "message": f"圖片生成{task['status'] == 'completed' and '完成' or '部分完成'}",
                    "error": task.get("error", None),
                    "total": len([url for url in task["urls"] if url]),
                }
            )

        # 任務仍在處理中，時間未超過 30 秒
        return Response(
            {
                "fileUrls": [url for url in task["urls"] if url],
                "status": "processing",
                "message": "正在生成圖片中",
                "total": len([url for url in task["urls"] if url]),
            }
        )


# 新增BedrockImageGenerator類，完全按照成功範例實現
class BedrockImageGenerator:
    """
    使用 AWS Bedrock Runtime API 呼叫圖像生成功能
    """

    def __init__(
        self, output_directory: str, model_id: str = "amazon.nova-canvas-v1:0"
    ):
        self.client = boto3.client("bedrock-runtime", region_name="us-east-1")
        self.output_directory = output_directory
        self.model_id = model_id

    def generate_images(self, inference_params: dict) -> dict:
        """完全按照成功範例實現的API調用方法"""
        response = self.client.invoke_model(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(inference_params),
        )
        raw_body = response["body"].read().decode("utf-8")
        return json.loads(raw_body)


def attempt_real_api_call(prompt, seed, mask_b64, source_b64):  # <-- 添加 source_b64
    """嘗試使用 Bedrock OUTPAINTING API 調用"""
    try:
        client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION_NAME", "us-east-1"),
        )

        # <-- 修改：構建 OUTPAINTING 參數 -->
        api_params = {
            "taskType": "OUTPAINTING",
            "outPaintingParams": {
                "image": source_b64,  # 源圖像 base64
                "text": prompt,  # 文本提示
                "maskImage": mask_b64,  # 遮罩圖像 base64
                "outPaintingMode": "DEFAULT",  # 或 PRECISE
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",  # 使用 quality 替代 height/width
                "cfgScale": 7.0,
                "seed": seed,
            },
        }
        # <-- 結束修改 -->

        print("API 請求參數 (Outpainting):", json.dumps(api_params, indent=2))

        response = client.invoke_model(
            modelId="amazon.nova-canvas-v1:0",  # 確認此模型是否支持 OUTPAINTING
            contentType="application/json",
            accept="application/json",
            body=json.dumps(api_params),
        )

        result = json.loads(response["body"].read())
        print("Outpainting API 調用成功")
        return result
    except Exception as e:
        print(f"Outpainting API 調用失敗: {e}")
        return {"error": str(e), "images": []}
