from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UpdateChatUserCommand:
    username: str

    last_visit: datetime = field(default=None)
    is_onlain: bool = field(default=None)
