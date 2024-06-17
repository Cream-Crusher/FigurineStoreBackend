import uuid

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.dto.blog_dto import BlogDTO
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

    @classmethod
    def from_dto(cls, dto: BlogDTO) -> 'Comments':
        return cls(
            title=dto.title,
            description=dto.description,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            active=dto.active,
            owner_id=dto.owner_id,
        )

    def to_dto(self) -> BlogDTO:
        return BlogDTO(
            id=self.id,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            active=self.active,
            owner_id=self.owner_id,
        )
