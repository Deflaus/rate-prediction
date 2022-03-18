from enum import Enum, IntEnum


class RedisDBs(IntEnum):
    celery_broker = 0
    prediction_results = 1
    user_states = 2


class TelegramApiMethods(str, Enum):
    set_web_hook_method = "setWebhook"
    delete_web_hook_method = "deleteWebhook"
    send_message = "sendMessage"
