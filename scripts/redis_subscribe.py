import redis

class RedisSubscribe:
    def __init__(self, host, port):
        self.r = redis.Redis(
            host=host,
            port=port,
        )

    def subscribe(self, channel):
        pubsub = self.r.pubsub()
        pubsub.subscribe(channel)
        print(f"Đang lắng nghe từ kênh '{channel}'...")

        # Vòng lặp để lắng nghe các message và trả về string
        for message in pubsub.listen():
            if message['type'] == 'message':
                return message['data'].decode('utf-8')