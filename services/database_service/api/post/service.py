import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import delete

from sqlalchemy.exc import IntegrityError
from api.post.model import Posts, PostsTags
from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase


class PostService(BaseRepository):
    model = Posts

    async def delete_post_tags(self, post_id: str):
        query = delete(PostsTags).where(PostsTags.post_id == post_id)
        await self.session.execute(query)
        await self.session.commit()

    async def update_post_tags(self, tags_ids: list, post_id: str | uuid.UUID):
        try:
            await self.delete_post_tags(post_id)

            for tag_id in tags_ids:
                self.session.add(PostsTags(post_id=post_id, tag_id=tag_id))

            await self.session.commit()

        except IntegrityError as error:
            raise HTTPException(status_code=400, detail=f'{error}')

    async def create_post(self, post: dict) -> object:
        tags_ids = post.pop('tags_ids', [])
        post = await self.create(post)

        if not tags_ids:
            return post

        await self.update_post_tags(tags_ids, post.id)
        await self.session.refresh(post)

        return post

    async def update_post(self, post_id: str, post: dict) -> object:
        tags_ids = post.pop('tags_ids', [])
        post = await self.update(post_id, post)

        if not tags_ids:
            return post

        await self.update_post_tags(tags_ids, post.id)
        await self.session.refresh(post)

        return post


async def get_post_service(session=Depends(AsyncDatabase.get_session)):
    return PostService(session)


post_service: PostService = Depends(get_post_service)
