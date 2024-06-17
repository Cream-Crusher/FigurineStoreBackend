from datetime import datetime
from uuid import UUID


class PostDTO:

    def __init__(
            self,
            title: str,
            author_id: UUID,
            body: str = None,
            is_published: bool = None,
            likes: int = None,
            views: int = None,
            created_at: datetime = None,
            updated_at: datetime = None,
            active: bool = None,
            id: UUID = None
    ):
        self.title = title
        self.author_id = author_id
        self.body = body
        self.is_published = is_published
        self.likes = likes
        self.views = views
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active
        self.id = id

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)
