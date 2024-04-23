import redis
import json


class RedisModule:

    def __init__(self):
        self.redis_client = None

    async def set_cache(self, key, data):
        json_data = json.dumps(data)
        self.redis_client.set(key, json_data)

    async def get_cache(self, key):
        data = self.redis_client.get(key)
        if data is None:
            return {}
        json_data = data.decode('utf-8')
        return json.loads(json_data)
