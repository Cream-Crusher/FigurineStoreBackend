import uuid

from services.chat_management.chat_management_core.entities.BaseEntity import BaseEntity


class Chat(BaseEntity):

    def __init__(self):
        super().__init__()
        first_user_id: uuid.UUID
        second_user_id: uuid.UUID
        # message_ids: list[uuid.UUID]
