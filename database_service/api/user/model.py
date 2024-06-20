import uuid

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from utils.base.BaseModel import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    fullname: Mapped[str] = mapped_column(default=None, nullable=False)
    username: Mapped[str] = mapped_column(default=None, nullable=False)
    phone: Mapped[str] = mapped_column(default=None, nullable=False)
    email: Mapped[str] = mapped_column(default=None, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # owned_blogs = relationship(Blogs, back_populates='owner')
    # author_posts = relationship(Posts, back_populates='author')
    # comments = relationship(Comments, back_populates='user')
    # blogs = relationship('Blogs', secondary=CompaniesUsers.__tablename__, back_populates='users')