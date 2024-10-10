import redis
from config import settings


# Kết nối đến Redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_POST,
)

# Tên kênh mới
channel_name = settings.REDIS_CHANEL_SUB

# Gửi thông điệp đến kênh mới
r.publish(channel_name, '1;Spring Pendulum;1,2,3;5')