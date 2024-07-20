import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, Field, EmailStr

from api.user.utils import check_phone


class UserBase(BaseModel):
    fullname: str = Field(max_length=40)
    username: Optional[str] = Field(default=None, max_length=40)
    email: Optional[EmailStr] = Field(default=None, max_length=60)
    phone: Optional[str] = Field(default=None, max_length=20)

    @field_validator("email")
    def email_to_lower(cls, email):
        return email.lower()

    @field_validator("phone")
    def check_phone(cls, number):
        return check_phone(number)

    @field_validator("username")
    def validate_name(cls, username):
        return username.strip()


class UserRead(UserBase):
    id: uuid.UUID
    role: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    latest_auth: Optional[datetime] = None
    active: Optional[bool]


class UserUpdate(UserBase):
    pass
