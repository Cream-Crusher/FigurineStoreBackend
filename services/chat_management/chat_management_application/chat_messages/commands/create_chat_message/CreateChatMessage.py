from dataclasses import dataclass

from services.chat_management.chat_management_core.entities.chat_message.ChatMessage import ChatMessage


@dataclass
class CreateChatMessage:
    chat_message = ChatMessage
