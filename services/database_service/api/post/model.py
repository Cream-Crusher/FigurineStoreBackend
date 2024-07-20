import uuid
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.comment.model import Comments
from api.tag.model import Tags
from utils.base.BaseModel import Base


class PostsTags(Base):
    __tablename__ = 'posts_tags'
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)

    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('posts.id'), nullable=False)  # ondelete='SET NULL'
    tag_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tags.id'), nullable=False)  # ondelete='SET NULL'


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
    author: Mapped['Users'] = relationship('Users', back_populates='author_posts')

    blog_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('blogs.id'), nullable=True)  # ondelete='CASCADE'
    blog: Mapped['Blogs'] = relationship('Blogs', back_populates='blog_posts')

    comments: Mapped[List[Comments]] = relationship('Comments', back_populates='post')

    tags: Mapped[List[Tags]] = relationship("Tags", secondary=PostsTags.__tablename__, back_populates="posts", uselist=True, lazy='selectin')
