import uuid

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.BaseModel import Base
from app.database.models.Posts import Posts


class Tags(Base):
    __tablename__ = 'tags'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    tag_name: Mapped[str] = mapped_column(default=None, nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    post = relationship('PostsTags', secondary=Posts.__tablename__, back_populates='posts')
