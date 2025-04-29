import json
import re
from textwrap import dedent
from typing import Dict, Any


def _strip_trailing_commas(json_str: str) -> str:
    """
    刪除物件或陣列結尾多餘的逗號，例如
    {"a":1,}  或  [1,2,]
    """
    return re.sub(r',\s*(?=[}\]])', '', json_str)


def _parse_input(json_input: str) -> Dict[str, Any]:
    """
    解析輸入：
    1. 若外層是 { "answer": "XXX" } 取出 answer
    2. 去掉多餘逗號再 loads
    """
    try:
        outer = json.loads(json_input)
    except json.JSONDecodeError as e:
        raise ValueError(f"外層 JSON 解析失敗：{e}")

    inner_str = outer["answer"] if isinstance(outer, dict) and "answer" in outer else json_input
    cleaned = _strip_trailing_commas(inner_str)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"內層 JSON 解析失敗：{e}")


def generate_prompt_from_json(json_input_str: str) -> str:
    """
    傳入 JSON 字串，回傳組裝好的 Prompt。
    支援：
      • 直接物件 JSON
      • 外層 {"answer": "<字串化的 JSON>"} 包裝
      • 自動修剪結尾逗號
    """
    data = _parse_input(json_input_str)

    # ---- 安全取欄位 ----
    style = data.get("style", "")
    chassis_frame = data.get("chassis_frame", "")

    front = data.get("front_panel", {})
    front_material = front.get("material", "")
    front_layout = front.get("layout", "")
    features = front.get("features", [])
    features_block = "\n".join(f"- {feat}" for feat in features)

    side = data.get("side_panel", {})
    side_type = side.get("type", "")
    side_frame = side.get("frame", "")
    interior_view = side.get("interior_view", "")

    vs = data.get("view_settings", {})
    angle = vs.get("angle", "")
    camera_height = vs.get("camera_height", "")
    lighting_conditions = vs.get("lighting", "")

    # ---- 組 Prompt ----
    prompt = dedent(f"""\
        Generate a {style} style computer case.

        The chassis frame features {chassis_frame}.

        The front panel is made of {front_material}, designed with {front_layout}, featuring:
        {features_block}

        The side panel is a {side_type}, framed with {side_frame}, showing the interior illuminated by and featuring {interior_view}.

        The view angle is {angle}, with the camera height at {camera_height}.
        The lighting setup is {lighting_conditions}.

        The overall atmosphere should be clean, futuristic, and premium.
    """).strip()

    return prompt


# ------------------- 測試範例 --------------------
if __name__ == "__main__":
    raw_input = '''
    {
      "answer": "{\\n  \\"view_settings\\": {\\n    \\"angle\\": \\"three-quarter front-left\\",\\n    \\"camera_height\\": \\"eye-level\\",\\n    \\"lighting\\": \\"studio soft-box, mild reflections\\",\\n  },\\n  \\"front_panel\\": {\\n    \\"material\\": \\"tempered glass\\",\\n    \\"layout\\": \\"vertical symmetry\\",\\n    \\"features\\": [\\n      \\"dual RGB light strips along left & right edges, soft violet hue\\",\\n      \\"small glowing power logo near the top\\",\\n    ]\\n  },\\n  \\"side_panel\\": {\\n    \\"type\\": \\"tempered glass\\",\\n    \\"frame\\": \\"curved aluminum bezel\\",\\n    \\"interior_view\\": \\"purple LED illumination, visible 140 mm fan, custom water-cool loop\\"\\n  },\\n  \\"chassis_frame\\": \\"signature Cosmos top & bottom aluminum bars\\",\\n  \\"style\\": \\"high-end workstation, clean, futuristic, photorealistic\\"\\n}\\n"
    }
    '''
    print(generate_prompt_from_json(raw_input))