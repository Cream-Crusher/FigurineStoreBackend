import uuid
from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class Tag(BaseModel):
    tag_name: Optional[str]


class PostBase(BaseModel):
    title: str = Field(max_length=100)
    body: str = Field(default=None)
    is_published: bool = Field(default=False)
    active: bool


class PostRead(PostBase):
    id: uuid.UUID
    author_id: uuid.UUID
    blog_id: uuid.UUID
    tags: List[Tag]
    likes: int = Field(default=None)
    views: int = Field(default=None)
    created_at: datetime
    updated_at: datetime
    active: bool


class PostCreate(PostBase):
    author_id: uuid.UUID
    blog_id: uuid.UUID
    tags_ids: Optional[List[uuid.UUID]] = Field(default=None)


class PostUpdate(PostBase):
    tags_ids: Optional[List[uuid.UUID]] = Field(default=None)
