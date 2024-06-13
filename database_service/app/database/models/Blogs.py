import uuid

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.BaseModel import Base
from app.database.models.BlogsUsers import CompaniesUsers


class Blogs(Base):
    __tablename__ = 'blogs'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(default=None, nullable=False)
    description: Mapped[str] = mapped_column(default=None, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)  # ondelete='CASCADE'
    owner = relationship('Users', back_populates='blogs')

    author = relationship('Users', secondary=CompaniesUsers.__tablename__, back_populates='blogs')
