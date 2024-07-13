from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends

from api.post.schema import PostCreate, PostRead, PostUpdate
from api.post.service import post_service
from utils.Auth.authentication import get_me
from utils.base.pagination import Pagination

router = APIRouter(prefix='/post', tags=['Post|Posts'])


@router.get('/', name='Get All Post', response_model=List[PostRead])
async def get_all_posts(posts=post_service, paging=Depends(Pagination)):
    return await posts.all(paging)


@router.get('/{post_id}', name='Get Post By Id', response_model=PostRead)
async def post_by_id(post_id: str, posts=post_service, me=Depends(get_me)):
    return await posts.id(post_id)


@router.post('/', name='Create Post', status_code=201)
async def create_post(post: PostCreate, posts=post_service, me=Depends(get_me)):
    if me.role not in ["admin"]:
        raise HTTPException(403, "forbidden")

    return posts.create_post(post.__dict__)


@router.delete('/{post_id}', name='Delete Post By Id')
async def del_post(post_id: str, posts=post_service, me=Depends(get_me)):
    if me.role not in ["admin"]:
        raise HTTPException(403, "forbidden")

    return await posts.delete(post_id)


@router.patch('/', name='Update Post By Id', response_model=PostRead)
async def update_post(post_id: str, post: PostUpdate, posts=post_service, me=Depends(get_me)):
    if me.role not in ["admin"]:
        raise HTTPException(403, "forbidden")

    return await posts.update(post_id, post.__dict__)
