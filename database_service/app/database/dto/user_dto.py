from datetime import datetime
from uuid import UUID


class UserDTO:

    def __init__(
            self,
            fullname: str,
            username: str,
            phone: str,
            is_admin: bool = None,
            is_superuser: bool = None,
            created_at: datetime = None,
            updated_at: datetime = None,
            active: bool = None,
            id: UUID = None
    ):
        self.fullname = fullname
        self.username = username
        self.phone = phone
        self.is_admin = is_admin
        self.is_superuser = is_superuser
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active
        self.id = id

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)
