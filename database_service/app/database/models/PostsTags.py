import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.BaseModel import Base


class PostsTags(Base):
    __tablename__ = 'posts_tags'
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)

    posts_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('posts.id'), nullable=False)  # ondelete='SET NULL'
    tags_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tags.id'), nullable=False)  # ondelete='SET NULL'
