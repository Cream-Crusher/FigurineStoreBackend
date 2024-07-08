import uuid
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.base.BaseModel import Base


class BlogsUsers(Base):
    __tablename__ = 'blogs_users'
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)

    users_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)  # ondelete='SET NULL'
    blogs_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('blogs.id'), nullable=False)  # ondelete='SET NULL'


class Blogs(Base):
    __tablename__ = 'blogs'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(default=None, nullable=False)
    description: Mapped[str] = mapped_column(default=None, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)  # ondelete='CASCADE'
    owner: Mapped['Users'] = relationship('Users', back_populates='owned_blogs', uselist=False)

    author: Mapped[List['Users']] = relationship('Users', secondary='blogs_users', back_populates='blogs', uselist=True)
