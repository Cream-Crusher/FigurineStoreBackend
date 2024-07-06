from utils.base.service import BaseRepository
from api.tag.model import Tag


class TagService(BaseRepository):
    model = Tag


async def get_tag_service(session=Depends(AsyncDatabase.get_session)):
    return TagService(session)


tag_service: TagService = Depends(get_tag_service)
