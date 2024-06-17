from datetime import datetime
from uuid import UUID


class CommentDTO:

    def __init__(
            self,
            body: str,
            author_id: UUID,
            post_id: UUID,
            created_at: datetime = None,
            updated_at: datetime = None,
            active: bool = None,
            id: UUID = None
    ):
        self.body = body
        self.author_id = author_id
        self.post_id = post_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active
        self.id = id

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)
