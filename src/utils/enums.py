from enum import Enum, IntEnum


class RedisDBs(IntEnum):
    celery_broker = 0
    prediction_results = 1
    user_states = 2


class BotCommands(str, Enum):
    start = "start"
    cancel = "cancel"
    predict = "predict"
