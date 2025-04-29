# AWS Elastic Beanstalk 部署 Django 專案教學

## IAM 權限需求
請確保你的 IAM 使用者擁有下列權限（JSON Policy 範例）：

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sns:*",
                "iam:*",
                "elasticbeanstalk:*",
                "iam:GetRole",
                "iam:PassRole",
                "s3:*",
                "cloudwatch:*",
                "cloudformation:*",
                "ec2:*",
                "iam:ListRoles",
                "elasticloadbalancing:*",
                "autoscaling:*"
            ],
            "Resource": "*"
        }
    ]
}
```

---

## 部署步驟

### 1. 安裝 AWS CLI 與 EB CLI

```bash
pip install awscli awsebcli
```

### 2. 設定 AWS CLI 金鑰

```bash
aws configure
```
- 輸入 Access Key、Secret Key、region（如 ap-northeast-1）、output format（json）

### 3. 初始化 Elastic Beanstalk 專案

```bash
cd backend
# 若未初始化過
eb init
```
- 選擇 region
- 選擇 Python 3.11 平台
- 其他選項預設即可
- SSH 金鑰可依需求建立

### 4. 建立 Procfile（若尚未存在）

`backend/Procfile` 內容：
```
web: gunicorn image_project.wsgi
```

### 5. 確認 requirements.txt 內容

`backend/requirements.txt` 範例：
```
Django==4.2.0
djangorestframework==3.14.0
django-cors-headers==4.0.0
Pillow==10.2.0
```

### 6. 設定 ALLOWED_HOSTS

`backend/image_project/settings.py` 內：
```python
ALLOWED_HOSTS = [
    '你的 EB 網址',
    'localhost',
    '127.0.0.1',
]
```

### 7. 建立 Elastic Beanstalk 環境（建議 Python 3.11）

```bash
eb create hackathon-backend-env --platform "Python 3.11"
```

### 8. 部署專案

```bash
eb deploy
```

### 9. 取得網址與測試

```bash
eb status
```
- 取得 CNAME，瀏覽器訪問測試

---

## 常見錯誤排除

- **DisallowedHost**：請將 EB 網址加入 ALLOWED_HOSTS
- **502 Bad Gateway / ModuleNotFoundError: No module named 'application'**：請確認 Procfile 存在且內容正確
- **requirements.txt 安裝失敗**：請確認所有套件支援 EB 選用的 Python 版本
- **Health: Red**：請用 `eb logs` 查看詳細錯誤

---

## 進階建議
- 若需靜態檔案支援，請設定 `STATIC_ROOT` 並執行 `python manage.py collectstatic`
- 若需資料庫遷移，請用 `eb ssh` 進入主機後執行 `python manage.py migrate`
- 建議 production 關閉 DEBUG，並設定 SECRET_KEY 為環境變數

---

## 參考
- [AWS EB 官方文件](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)
- [Django 官方文件](https://docs.djangoproject.com/zh-hans/4.2/howto/deployment/checklist/) 