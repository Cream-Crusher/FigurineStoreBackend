from .BaseRepository import BaseRepository, session_handler
from ..models.tags import Tags


class TagRepository(BaseRepository):
    model = Tags

    # логика запросов обернутая в декоратор


TagRep = TagRepository()
