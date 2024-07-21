import uuid
from dataclasses import dataclass

from services.chat_management.chat_management_core.entities.BaseEntity import BaseEntity


@dataclass
class ChatMessage(BaseEntity):
    message_text: str
    chat_id: uuid.UUID
    user_id: uuid.UUID
