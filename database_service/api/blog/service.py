from api.blog.model import Blog


class BlogService(BaseRepository):
    model = Comments


async def get_blog_service(session=Depends(AsyncDatabase.get_session)):
    return BlogService(session)


blog_service: BlogService = Depends(get_blog_service)
