import uuid
from datetime import datetime

from pydantic import BaseModel


class UserRead(BaseModel):
    id: uuid.UUID
    fullname: str
    username: str
    phone_number: str
    email: str
    is_admin: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    active: bool


class UpdateUserData(BaseModel):
    fullname: str
    username: str
    phone: str
    email: str
