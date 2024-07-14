from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.post.schema import PostCreate, PostRead, PostUpdate
from api.post.service import post_service
from utils.Auth.authentication import get_me
from utils.base.pagination import Pagination

router = APIRouter(prefix='/post', tags=['Post|Posts'])


@router.get('/', name='Get All Post', response_model=List[PostRead], status_code=200)
async def get_all_posts(posts=post_service, paging=Depends(Pagination)):
    return await posts.all(paging)


@router.get('/{post_id}', name='Get Post By Id', response_model=PostRead, status_code=200)
async def post_by_id(post_id: str, posts=post_service, me=Depends(get_me)):
    return await posts.id(post_id)


@router.post('/', name='Create Post', status_code=201)
async def create_post(post: PostCreate, posts=post_service, me=Depends(get_me)):
    if me.role not in ["admin", "user"]:
        raise HTTPException(403, "forbidden")

    return await posts.create_post(post.__dict__)


@router.delete('/{post_id}', name='Delete Post By Id', status_code=200)
async def del_post(post_id: str, posts=post_service, me=Depends(get_me)):
    post = await posts.id(post_id)

    if not (me.role in ["admin"] or post.author_id == me.id):
        raise HTTPException(403, "forbidden")

    return await posts.delete(post_id)


@router.patch('/', name='Update Post By Id', response_model=PostUpdate, status_code=200)
async def update_post(post_id: str, posts=post_service, me=Depends(get_me)):
    post = await posts.id(post_id)

    if not (me.role in ["admin"] or post.author_id == me.id):
        raise HTTPException(403, "forbidden")

    return await posts.update(post_id, post.__dict__)
