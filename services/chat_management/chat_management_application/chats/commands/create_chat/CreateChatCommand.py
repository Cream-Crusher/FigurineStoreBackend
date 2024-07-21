from dataclasses import dataclass

from services.chat_management.chat_management_core.entities.chat.Chat import Chat


@dataclass
class CreateChatCommand:
    chat: Chat
