from fastapi import Depends, HTTPException

from sqlalchemy.exc import IntegrityError
from api.post.model import Posts, PostsTags
from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase


class PostService(BaseRepository):
    model = Posts

    async def create_post(self, post: dict) -> object:
        tags_ids = post.pop('tags_ids', [])
        post = await self.create(post)

        if not tags_ids:
            return post

        try:
            for tag_id in tags_ids:
                self.session.add(PostsTags(post_id=post.id, tag_id=tag_id))

            await self.session.commit()
            await self.session.refresh(post)

            return post

        except IntegrityError as error:
            raise HTTPException(status_code=400, detail=f'{error}')


async def get_post_service(session=Depends(AsyncDatabase.get_session)):
    return PostService(session)


post_service: PostService = Depends(get_post_service)
