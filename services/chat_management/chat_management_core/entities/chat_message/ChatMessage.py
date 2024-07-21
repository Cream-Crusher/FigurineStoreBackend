import uuid

from services.chat_management.chat_management_core.entities.BaseEntity import BaseEntity


class ChatMessage(BaseEntity):
    def __init__(self):
        super().__init__()
        self.message_text: str
        self.chat_id: uuid.UUID
        self.user_id: uuid.UUID
