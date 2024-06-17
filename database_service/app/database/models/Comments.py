import uuid

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.dto.comment_dto import CommentDTO
from app.database.models.BaseModel import Base


class Comments(Base):
    __tablename__ = 'comments'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    body: Mapped[str] = mapped_column(default='', nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)  # ondelete='CASCADE'
    author = relationship('Users', back_populates='comments')

    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('posts.id'), nullable=False)  # ondelete='CASCADE'
    post = relationship('Posts', back_populates='comments')

    @classmethod
    def from_dto(cls, dto: CommentDTO) -> 'Comments':
        return cls(
            body=dto.body,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            active=dto.active,
            author_id=dto.author_id,
            post_id=dto.post_id,
        )

    def to_dto(self) -> CommentDTO:
        return CommentDTO(
            id=self.id,
            body=self.body,
            created_at=self.created_at,
            updated_at=self.updated_at,
            active=self.active,
            author_id=self.author_id,
            post_id=self.post_id,
        )
