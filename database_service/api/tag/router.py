from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends

from api.tag.schema import TagCreate, TagRead, TagUpdate
from api.tag.service import tag_service
from utils.Auth.authentication import get_me
from utils.base.pagination import Pagination

router = APIRouter(prefix='/tags', tags=['Tag|Tags'])


@router.get('/', name='Get All Tag', response_model=List[TagRead])
async def get_all_tags(tags=tag_service, paging=Depends(Pagination)):
    return await tags.all(paging)


@router.get('/{tag_id}', name='Get Tag By Id', response_model=TagRead)
async def tag_by_id(tag_id: str, tags=tag_service, me=Depends(get_me)):
    return await tags.id(tag_id)


@router.post('/', name='Create Tag', status_code=201)
async def create_tag(tag: TagCreate, tags=tag_service, me=Depends(get_me)):
    if me.role not in ["admin"]:
        raise HTTPException(403, "forbidden")

    return await tags.create(tag.__dict__)


@router.delete('/{tag_id}', name='Delete Tag By Id')
async def del_tag(tag_id: str, tags=tag_service, me=Depends(get_me)):
    if me.role not in ["admin"]:
        raise HTTPException(403, "forbidden")

    return await tags.delete(tag_id)


@router.patch('/', name='Update Tag By Id', response_model=TagRead)
async def update_tag(tag_id: str, tag: TagUpdate, tags=tag_service, me=Depends(get_me)):
    if me.role not in ["admin"]:
        raise HTTPException(403, "forbidden")

    return await tags.update(tag_id, tag.__dict__)
