from redis import Redis
from dao.redis.key_schema import KeySchema


class RedisDaoBase:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.key_schema = KeySchema()
