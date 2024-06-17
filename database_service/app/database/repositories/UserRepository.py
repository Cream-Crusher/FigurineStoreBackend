from .BaseRepository import BaseRepository, session_handler
from ..models.Users import Users


class UserRepository(BaseRepository):
    model = Users

    # логика запросов обернутая в декоратор


UserRep = UserRepository()
