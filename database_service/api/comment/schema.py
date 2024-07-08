import uuid

from dataclasses import dataclass

from typing import Optional

from datetime import datetime

from pydantic import BaseModel, field_validator, Field, EmailStr


class CommentBase(BaseModel):
    body: str = Field(default=None, max_length=5000)
    is_published: bool = Field(default=False)
    active: bool


class CommentRead(CommentBase):
    id: uuid.UUID
    author_id: uuid.UUID
    post_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CommentCreate(CommentBase):
    author_id: uuid.UUID
    post_id: uuid.UUID


class CommentUpdate(CommentBase):
    pass
