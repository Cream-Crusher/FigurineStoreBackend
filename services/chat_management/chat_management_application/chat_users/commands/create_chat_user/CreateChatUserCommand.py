from services.chat_management.chat_management_core.entities.chat_user.ChatUser import ChatUser


class CreateChatUserCommand:

    def __init__(self):
        self.chat_user = ChatUser
