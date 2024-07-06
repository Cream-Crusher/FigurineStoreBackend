from fastapi import HTTPException, Depends

from api.tag.model import Tag
from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase


class TagService(BaseRepository):
    model = Tag


async def get_tag_service(session=Depends(AsyncDatabase.get_session)):
    return TagService(session)


tag_service: TagService = Depends(get_tag_service)
