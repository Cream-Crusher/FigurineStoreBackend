import uuid

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.dto.tag_dto import TagDTO
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

    @classmethod
    def from_dto(cls, dto: TagDTO) -> 'Tags':
        return cls(
            tag_name=dto.tag_name,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            active=dto.active,
        )

    def to_dto(self) -> TagDTO:
        return TagDTO(
            id=self.id,
            tag_name=self.tag_name,
            created_at=self.created_at,
            updated_at=self.updated_at,
            active=self.active,
        )
