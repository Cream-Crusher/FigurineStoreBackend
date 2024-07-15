from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.blog.schema import BlogCreate, BlogRead, BlogUpdate
from api.blog.service import blog_service
from utils.Auth.authentication import get_me
from utils.base.pagination import Pagination

router = APIRouter(prefix='/blog', tags=['Blog|Blogs'])


@router.get('/', name='Get All Blog', response_model=List[BlogRead])
async def get_all_blogs(blogs=blog_service, paging=Depends(Pagination)):
    return await blogs.all(paging)


@router.get('/{blog_id}', name='Get Blog By Id', response_model=BlogRead)
async def blog_by_id(blog_id: str, blogs=blog_service, me=Depends(get_me)):
    return await blogs.id(blog_id)


@router.post('/', name='Create Blog', status_code=201)
async def create_blog(blog: BlogCreate, blogs=blog_service, me=Depends(get_me)):
    if me.role not in ["admin", "user"]:
        raise HTTPException(403, "forbidden")

    return await blogs.create(blog.__dict__)


@router.delete('/{blog_id}', name='Delete Blog By Id')
async def del_blog(blog_id: str, blogs=blog_service, me=Depends(get_me)):
    blog_owner_id = (await blogs.id(blog_id)).owner_id

    if not (me.role in ["admin"] or blog_owner_id in me.roles):
        raise HTTPException(403, "forbidden")

    return await blogs.delete(blog_id)


@router.patch('/', name='Update Blog By Id', response_model=BlogRead)
async def update_blog(blog_id: str, blog: BlogUpdate, blogs=blog_service, me=Depends(get_me)):
    blog_owner_id = (await blogs.id(blog_id)).owner_id

    if not (me.role in ["admin"] or blog_owner_id in me.roles):
        raise HTTPException(403, "forbidden")

    return await blogs.update(blog_id, blog.__dict__)
