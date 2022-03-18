from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]
    can_join_groups: Optional[bool]
    can_read_all_group_messages: Optional[bool]
    supports_inline_queries: Optional[bool]


class Chat(BaseModel):
    id: int
    type: str
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class MessageEntityType(str, Enum):
    MENTION = "mention"
    HASHTAG = "hashtag"
    CASHTAG = "cashtag"
    BOT_COMMAND = "bot_command"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    PRE = "pre"
    TEXT_LINK = "text_link"
    TEXT_MENTION = "text_mention"


class MessageEntity(BaseModel):
    type: "MessageEntityType"
    offset: int
    length: int
    url: Optional[str]
    user: Optional["User"]
    language: Optional[str]


class Message(BaseModel):
    message_id: int
    from_user: User = Field(..., alias="from")
    chat: "Chat"
    text: Optional[str]
    entities: Optional[List["MessageEntity"]]


class Update(BaseModel):
    update_id: int
    message: Optional["Message"]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]


class SendMessage(BaseModel):
    chat_id: Union[int, str]
    text: str
    parse_mode: Optional[str]
    entities: Optional[List[dict]]
    disable_web_page_preview: Optional[bool]
    disable_notification: Optional[bool]
    protect_content: Optional[bool]
    reply_to_message_id: Optional[int]
    allow_sending_without_reply: Optional[bool]
    reply_markup: Optional[dict]
