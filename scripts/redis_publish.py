import redis

class RedisPublish:
    def __init__(self, host, port):
        # Kết nối tới Redis với thông tin host, port, password
        self.r = redis.Redis(
            host=host,
            port=port,
        )

    def publish(self, channel, message):
        # Gửi (publish) message lên kênh (channel) đã định nghĩa
        self.r.publish(channel, message)
        print(f"Đã gửi tin nhắn '{message}' lên kênh '{channel}'")