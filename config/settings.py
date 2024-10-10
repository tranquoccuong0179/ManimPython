import os

# settings.py
GOOGLE_DRIVE_API_CREDENTIALS = os.path.join(os.path.dirname(__file__), 'credentials.json')  # Đường dẫn tới tệp JSON của API credentials
GOOGLE_DRIVE_FOLDER_ID = '1SCDzLjXNxPjPfrbnxVaN42AiPJE-ATm9'  # ID của thư mục trên Google Drive
FIREBASE_CREDENTIALS = os.path.join(os.path.dirname(__file__), 'physic-manim-firebase-adminsdk.json')  # Đường dẫn tới tệp JSON của API credentials
STORAGE_BUCKET_ID = 'physic-manim.appspot.com' # Storage bucket trên firebase

REDIS_POST = 6379
REDIS_HOST = '127.0.0.1'
# REDIS_PASSWORD = 'ExqMLLIww8XVYKaN5GP8zHNEcdtkpx56'
REDIS_CHANEL_SUB = 'Channel1'
REDIS_CHANEL_PUB = 'Channel2'