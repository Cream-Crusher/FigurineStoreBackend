from .BaseRepository import BaseRepository, session_handler
from ..models.Blogs import Blogs


class BlogRepository(BaseRepository):
    model = Blogs

    # логика запросов обернутая в декоратор


BlogRep = BlogRepository()
