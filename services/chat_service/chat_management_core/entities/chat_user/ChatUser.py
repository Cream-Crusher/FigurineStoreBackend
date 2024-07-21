from dataclasses import dataclass
from datetime import datetime

from services.chat_service.chat_management_core.entities.BaseEntity import BaseEntity


@dataclass
class ChatUser(BaseEntity):
    username: str
    last_seen: datetime
    is_online: bool
