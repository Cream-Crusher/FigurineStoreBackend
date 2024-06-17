from .BaseRepository import BaseRepository, session_handler
from ..models.Posts import Posts


class PostRepository(BaseRepository):
    model = Posts

    # логика запросов обернутая в декоратор


PostRep = PostRepository()
