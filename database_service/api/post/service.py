from fastapi import Depends

from api.post.model import Post
from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase


class PostService(BaseRepository):
    model = Post


async def get_post_service(session=Depends(AsyncDatabase.get_session)):
    return PostService(session)


post_service: PostService = Depends(get_post_service)
