import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.BaseModel import Base


class CompaniesUsers(Base):
    __tablename__ = 'companies_users'
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)

    users_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)  # ondelete='SET NULL'
    blogs_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('blogs.id'), nullable=False)  # ondelete='SET NULL'
