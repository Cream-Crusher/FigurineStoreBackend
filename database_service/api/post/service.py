import copy
import uuid
from typing import List

from fastapi import Depends, HTTPException

from api.post.model import Posts, PostsTags
from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase


class PostService(BaseRepository):
    model = Posts

    async def create_post(self, post: dict) -> object:
        post = post.__dict__

        if post['tags'] is None:
            post.pop('tags')
            return await self.create(post)
        else:
            return await self.create_posts_with_tag(post)

    async def create_posts_with_tag(self, post: dict) -> object:
        tags_ids = copy.deepcopy(post['tags'])
        post.pop('tags')

        post = await self.create(post)
        post_id = post.id

        for tag_id in tags_ids:
            post_tags = PostsTags(post_id=post_id, tag_id=tag_id)
            self.session.add(post_tags)

        await self.session.commit()
        await self.session.refresh(post)

        return await self.id(post_id)


async def get_post_service(session=Depends(AsyncDatabase.get_session)):
    return PostService(session)


post_service: PostService = Depends(get_post_service)
