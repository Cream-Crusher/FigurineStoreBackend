from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UpdateChatUserCommand(BaseModel):
    username: Optional[str]
    last_visit: Optional[datetime]
    is_onlain: Optional[bool]
