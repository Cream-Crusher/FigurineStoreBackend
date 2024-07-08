import uuid


from datetime import datetime

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(max_length=100)
    body: str = Field(default=None)
    is_published: bool = Field(default=False)
    active: bool


class PostRead(PostBase):
    id: uuid.UUID
    author_id: uuid.UUID
    likes: int = Field(default=None)
    views: int = Field(default=None)
    created_at: datetime
    updated_at: datetime
    active: bool


class PostCreate(PostBase):
    author_id: uuid.UUID
    pass


class PostUpdate(PostBase):
    pass
