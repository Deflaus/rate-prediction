from typing import List

from dao.base import PredictionsDaoBase
from dao.redis.synchronous.base import RedisDaoBase


class PredictionsDaoRedis(PredictionsDaoBase, RedisDaoBase):
    def insert(self, current_value: str, predictions: List[str]) -> None:
        if old_predictions := self.redis_client.lrange(self.key_schema.prediction_result(), 0, -1):
            for _ in old_predictions:
                self.redis_client.rpop(self.key_schema.prediction_result())
        self.redis_client.rpush(self.key_schema.prediction_result(), current_value)
        for prediction in predictions:
            self.redis_client.rpush(self.key_schema.prediction_result(), prediction)

    def get_recent(self) -> List[str]:
        pass
