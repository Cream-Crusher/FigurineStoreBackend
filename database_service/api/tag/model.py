import uuid

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.base.BaseModel import Base


class Tags(Base):
    __tablename__ = 'tags'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    tag_name: Mapped[str] = mapped_column(default=None, nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    post = relationship('PostsTags', secondary=Posts.__tablename__, back_populates='posts')


class PostsTags(Base):
    __tablename__ = 'posts_tags'
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)

    posts_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('posts.id'), nullable=False)  # ondelete='SET NULL'
    tags_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tags.id'), nullable=False)  # ondelete='SET NULL'
