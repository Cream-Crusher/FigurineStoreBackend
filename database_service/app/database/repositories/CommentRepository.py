from .BaseRepository import BaseRepository, session_handler
from ..models.Comments import Comments


class CommentRepository(BaseRepository):
    model = Comments

    # логика запросов обернутая в декоратор


CommentRep = CommentRepository()
