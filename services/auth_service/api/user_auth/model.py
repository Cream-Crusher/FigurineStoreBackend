import uuid
import bcrypt

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
    role: Mapped[str] = mapped_column(default='user', nullable=False)  # user, employee, admin
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    latest_auth: Mapped[datetime] = mapped_column(nullable=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
