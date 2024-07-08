from fastapi import Depends

from api.blog.model import Blogs
from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase


class BlogService(BaseRepository):
    model = Blogs


async def get_blog_service(session=Depends(AsyncDatabase.get_session)):
    return BlogService(session)


blog_service: BlogService = Depends(get_blog_service)
