import uuid

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.dto.user_dto import UserDTO
from app.database.models.BaseModel import Base
from app.database.models.Posts import Posts
from app.database.models.Blogs import Blogs
from app.database.models.BlogsUsers import CompaniesUsers


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    fullname: Mapped[str] = mapped_column(default=None, nullable=False)
    username: Mapped[str] = mapped_column(default=None, nullable=False)
    phone: Mapped[str] = mapped_column(default=None, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    owned_companies = relationship('Companies', back_populates='owner', foreign_keys=[Blogs.owner_id])
    author_posts = relationship('Posts', back_populates='author', foreign_keys=[Posts.author_id])

    companies = relationship('Companies', secondary=CompaniesUsers.__tablename__, back_populates='users')

    @classmethod
    def from_dto(cls, dto: UserDTO) -> 'Users':
        return cls(
            fullname=dto.fullname,
            username=dto.username,
            phone=dto.phone,
            is_admin=dto.is_admin,
            is_superuser=dto.is_superuser,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            active=dto.active,
        )

    def to_dto(self) -> UserDTO:
        return UserDTO(
            id=self.id,
            fullname=self.fullname,
            username=self.username,
            phone=self.phone,
            is_admin=self.is_admin,
            is_superuser=self.is_superuser,
            created_at=self.created_at,
            updated_at=self.updated_at,
            active=self.active,
        )
