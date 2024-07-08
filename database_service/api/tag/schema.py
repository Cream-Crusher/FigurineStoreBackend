import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    tag_name: str = Field(max_length=20)
    active: bool


class TagRead(TagBase):
    id: uuid.UUID
    role: str
    created_at: datetime
    updated_at: datetime


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass
