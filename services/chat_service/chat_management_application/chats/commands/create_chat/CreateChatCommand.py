from pydantic import BaseModel

from services.chat_service.chat_management_core.entities.chat.Chat import Chat


class CreateChatCommand(BaseModel):
    chat: Chat
