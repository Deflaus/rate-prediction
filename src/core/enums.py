from enum import Enum


class RedisDBs(Enum):
    user_states = 2
    prediction = 3


class TelegramApiMethods(Enum):
    set_web_hook_method = "setWebhook"
    delete_web_hook_method = "deleteWebhook"
    send_message = "sendMessage"
