from pydantic import BaseModel

from services.chat_service.chat_management_core.entities.chat_user.ChatUser import ChatUser


class CreateChatUserCommand(BaseModel):
    chat_user: ChatUser
