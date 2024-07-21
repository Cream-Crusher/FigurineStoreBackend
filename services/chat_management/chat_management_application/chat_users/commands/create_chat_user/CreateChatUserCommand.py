from dataclasses import dataclass

from services.chat_management.chat_management_core.entities.chat_user.ChatUser import ChatUser


@dataclass
class CreateChatUserCommand:
    chat_user: ChatUser

