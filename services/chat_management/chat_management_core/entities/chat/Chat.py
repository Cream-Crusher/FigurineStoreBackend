import uuid
from dataclasses import dataclass, field
from typing import List

from services.chat_management.chat_management_core.entities.BaseEntity import BaseEntity


@dataclass
class Chat(BaseEntity):
    first_user_id: uuid.UUID
    second_user_id: uuid.UUID
    message_id: List[uuid.UUID] = field(default_factory=list)
