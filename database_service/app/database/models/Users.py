import uuid

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.BaseModel import Base
from app.database.models.Posts import Posts
from app.database.models.Blogs import Blogs
from app.database.models.BlogsUsers import CompaniesUsers


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(default=None, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    owned_companies = relationship('Companies', back_populates='owner', foreign_keys=[Blogs.owner_id])
    author_posts = relationship('Posts', back_populates='author', foreign_keys=[Posts.author_id])

    companies = relationship('Companies', secondary=CompaniesUsers.__tablename__, back_populates='users')
