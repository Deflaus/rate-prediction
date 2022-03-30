from typing import List

from dao.base import PredictionsDaoBase
from dao.redis.asynchronous.base import RedisDaoBase


class PredictionsDaoRedis(PredictionsDaoBase, RedisDaoBase):
    async def insert(self, current_value: str, predictions: List[str]) -> None:
        pass

    async def get_recent(self) -> List[str]:
        predictions = await self.redis_client.lrange(self.key_schema.prediction_result(), 0, -1)
        return predictions
