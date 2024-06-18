import uuid

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.dto.post_dto import PostDTO
from app.database.models.BaseModel import Base
from app.database.models.Comments import Comments
from app.database.models.PostsTags import PostsTags


class Posts(Base):
    __tablename__ = 'posts'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(default=None, nullable=False)
    body: Mapped[str] = mapped_column(default='', nullable=False)
    is_published: Mapped[bool] = mapped_column(default=False, nullable=False)
    likes: Mapped[int] = mapped_column(default=0, nullable=False)
    views: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)  # ondelete='CASCADE'
    author = relationship('Users', back_populates='posts')

    comments = relationship('Comments', back_populates='posts')

    tags = relationship('PostsTags', secondary=PostsTags.__tablename__, back_populates='posts')

    @classmethod
    def from_dto(cls, dto: PostDTO) -> 'Posts':
        return cls(
            title=dto.title,
            body=dto.body,
            is_published=dto.is_published,
            likes=dto.likes,
            views=dto.views,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            active=dto.active,
            author_id=dto.author_id,
        )

    def to_dto(self) -> PostDTO:
        return PostDTO(
            id=self.id,
            title=self.title,
            body=self.body,
            is_published=self.is_published,
            likes=self.likes,
            views=self.views,
            created_at=self.created_at,
            updated_at=self.updated_at,
            active=self.active,
            author_id=self.author_id,
        )
