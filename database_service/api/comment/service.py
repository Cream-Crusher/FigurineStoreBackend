from fastapi import Depends

from api.comment.model import Comments

from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase


class CommentService(BaseRepository):
    model = Comments


async def get_comment_service(session=Depends(AsyncDatabase.get_session)):
    return CommentService(session)


comment_service: CommentService = Depends(get_comment_service)
