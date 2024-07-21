from pydantic import BaseModel

from services.chat_service.chat_management_core.entities.chat_message.ChatMessage import ChatMessage


class CreateChatMessage(BaseModel):
    chat_message = ChatMessage
