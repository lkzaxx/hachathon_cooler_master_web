import boto3
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseForbidden


def health_check(request):
    return HttpResponse("OK", status=200)


def protected_media(request, key):
    # 權限檢查（範例：必須登入）
    if not request.user.is_authenticated:
        return HttpResponseForbidden("未授權")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    try:
        obj = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        file_data = obj["Body"].read()
        content_type = obj.get("ContentType", "application/octet-stream")
        return HttpResponse(file_data, content_type=content_type)
    except s3.exceptions.NoSuchKey:
        raise Http404("檔案不存在")
