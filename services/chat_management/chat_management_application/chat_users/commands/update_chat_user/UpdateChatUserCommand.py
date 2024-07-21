from datetime import datetime


class UpdateChatUserCommand:
    def __init__(self):
        self.username: str

        self.last_visit: datetime
        self.is_onlain: bool | None
