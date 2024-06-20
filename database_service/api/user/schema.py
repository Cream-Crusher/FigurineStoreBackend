import uuid

from typing import Optional

from datetime import datetime

from pydantic import BaseModel, field_validator, Field

from api.user.utils import check_phone


class UserRead(BaseModel):
    id: uuid.UUID
    fullname: Optional[str]
    username: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    is_admin: Optional[bool]
    is_superuser: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    active: Optional[bool]


class UserUpdate(BaseModel):
    fullname: Optional[str]
    username: Optional[str]
    email: Optional[str]
    phone: Optional[str] = Field(default=None, max_length=20)

    @field_validator("phone")
    async def check_phone(cls, number):
        return await check_phone(number)
