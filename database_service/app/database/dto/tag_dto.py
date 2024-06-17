from datetime import datetime
from uuid import UUID


class TagDTO:

    def __init__(
            self,
            tag_name: str,
            created_at: datetime = None,
            updated_at: datetime = None,
            active: bool = None,
            id: UUID = None
    ):
        self.tag_name = tag_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active
        self.id = id

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)
