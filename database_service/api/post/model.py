import uuid

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.tag.model import PostsTags
from utils.base.BaseModel import Base


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
