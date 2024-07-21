from datetime import datetime

from pydantic import BaseModel


class GetChatUserResponses(BaseModel):
    id: str
    username: str
    last_seen: datetime
    is_online: bool
