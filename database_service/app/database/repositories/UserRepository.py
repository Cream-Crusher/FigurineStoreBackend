from sqlalchemy.testing.pickleable import User
from sqlalchemy import select

from .BaseRepository import BaseRepository, session_handler
from ..models.Users import Users


class UserRepository(BaseRepository):
    model = Users

    @session_handler
    async def get_user_by_phone(self, session, phone: str) -> User:
        user = (await session.scalars(select(Users).where(Users.phone == phone))).fist()

        return user

    @session_handler
    async def get_user_by_email(self, session, email: str) -> User:
        user = (await session.scalars(select(Users).where(Users.email == email))).fist()

        return user


UserRep = UserRepository()
