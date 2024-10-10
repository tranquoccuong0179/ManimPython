import firebase_admin
from firebase_admin import credentials, storage
from datetime import timedelta
from config import settings  # Import các cấu hình từ file settings.py

# Khởi tạo Firebase và Storage Bucket toàn cục
firebase_initialized = False
bucket = None

def initialize_firebase():
    global bucket, firebase_initialized
    if not firebase_initialized:
        # Khởi tạo Firebase
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred, {
            'storageBucket': settings.STORAGE_BUCKET_ID
        })

        # Khởi tạo Firebase Storage
        bucket = storage.bucket()
        firebase_initialized = True
        print("Firebase initialized with bucket:", bucket.name)

def upload_video(file_path):
    # Khởi tạo Firebase Storage nếu chưa khởi tạo
    initialize_firebase()

    # Tạo tên file duy nhất bằng cách lấy tên file từ đường dẫn
    file_name = file_path.split("/")[-1]
    blob = bucket.blob(f'videos/{file_name}')

    # Upload file lên Firebase Storage
    blob.upload_from_filename(file_path)

    # Tạo URL có chữ ký cho file vừa upload, thời gian hết hạn là 365 ngày
    url = blob.generate_signed_url(expiration=timedelta(days=365))

    print(f'File uploaded successfully. URL: {url}')
    return url