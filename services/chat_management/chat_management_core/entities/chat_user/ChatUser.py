from datetime import datetime

from services.chat_management.chat_management_core.entities.BaseEntity import BaseEntity


class ChatUser(BaseEntity):
    def __init__(self):
        super().__init__()
        self.username: str
        self.last_visit: datetime
        self.is_onlain: bool
