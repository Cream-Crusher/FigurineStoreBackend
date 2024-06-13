import uuid

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    post = relationship('Users', back_populates='posts')
