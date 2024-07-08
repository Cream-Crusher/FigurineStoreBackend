from fastapi import Depends

from api.tag.model import Tags
from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase


class TagService(BaseRepository):
    model = Tags


async def get_tag_service(session=Depends(AsyncDatabase.get_session)):
    return TagService(session)


tag_service: TagService = Depends(get_tag_service)
