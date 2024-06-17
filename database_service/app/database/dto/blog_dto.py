from datetime import datetime
from uuid import UUID


class BlogDTO:

    def __init__(
            self,
            title: str,
            owner_id: UUID,
            description: str = None,
            created_at: datetime = None,
            updated_at: datetime = None,
            active: bool = None,
            id: UUID = None
    ):
        self.title = title
        self.owner_id = owner_id
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active
        self.id = id

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)
