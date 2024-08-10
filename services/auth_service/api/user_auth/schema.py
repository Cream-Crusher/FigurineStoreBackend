import uuid

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator, Field, EmailStr

from api.user_auth.utils import check_phone


class Roles(str, Enum):
    user = "user"
    employee = "employee"


class UserBase(BaseModel):
    fullname: str = Field(max_length=40)
    username: Optional[str] = Field(default=None, max_length=40)
    phone: Optional[str] = Field(default=None, max_length=20)

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


class UserCreate(UserBase):
    role: Roles
    password: str = Field(max_length=40)
    active: Optional[bool]


class UserAdminCreate(UserBase):
    password: str = Field(max_length=40)


class TwoFactorAuthentication(BaseModel):
    email: EmailStr


class TwoFactorAuthenticationConfirm(BaseModel):
    token: str
