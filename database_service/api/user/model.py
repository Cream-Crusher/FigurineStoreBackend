import uuid
from datetime import datetime
from typing import List

import bcrypt
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.blog.model import BlogsUsers, Blogs
from api.comment.model import Comments
from api.post.model import Posts
from utils.base.BaseModel import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    fullname: Mapped[str] = mapped_column(default=None, nullable=False)
    username: Mapped[str] = mapped_column(default=None, nullable=False)
    phone: Mapped[str] = mapped_column(default=None, nullable=False)
    email: Mapped[str] = mapped_column(default=None, nullable=False)
    role: Mapped[str] = mapped_column(default='user', nullable=False)  # user, employee, admin
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    latest_auth: Mapped[datetime] = mapped_column(nullable=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    owned_blogs: Mapped[List[Blogs]] = relationship('Blogs', back_populates='owner')
    author_posts: Mapped[List[Posts]] = relationship('Posts', back_populates='author')
    comments: Mapped[List[Posts]] = relationship(Comments, back_populates='author')

    blogs = relationship(Blogs, secondary=BlogsUsers.__tablename__, back_populates='author')

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
