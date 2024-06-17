from sqlalchemy.testing.pickleable import User

from .BaseRepository import BaseRepository, session_handler
from ..models.Users import Users


class UserRepository(BaseRepository):
    model = Users

    @session_handler
    async def get_user_by_phone(self, session, phone: str) -> User:
        user = session.query(Users).filter(Users.phone == phone).first()

        return user

    @session_handler
    async def get_user_by_email(self, session, email: str) -> User:
        user = session.query(Users).filter(Users.email == email).first()

        return user


UserRep = UserRepository()
