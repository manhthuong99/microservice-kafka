import redis

from core.modules.redis_module.redis_module import RedisModule


class RedisModuleSingleton(RedisModule):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def init(self, redis_host='localhost', redis_port=6379, redis_db=0):
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db)
        self.redis_client = redis.Redis(connection_pool=pool)
