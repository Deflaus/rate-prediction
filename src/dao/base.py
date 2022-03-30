import abc
from typing import List


class PredictionsDaoBase(abc.ABC):
    @abc.abstractmethod
    def insert(self, current_value: str, predictions: List[str]) -> None:
        pass

    @abc.abstractmethod
    def get_recent(self) -> List[str]:
        pass
