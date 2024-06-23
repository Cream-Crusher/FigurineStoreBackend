from typing import Optional, List

from fastapi import APIRouter, Depends

from api.user.schema import UserRead, UserUpdate
from api.user.service import user_service
from utils.base.Pagination import Pagination

router = APIRouter(prefix='/api/v1/users', tags=['User|Users'])


@router.get('/', name='Get All User', response_model=List[UserRead])
async def get_user_by_id(users=user_service,  paging=Depends(Pagination)):
    return await users.all(paging)


@router.patch('/', name='Update User By Id', response_model=Optional[UserRead])
async def update_user_by_id(user: UserUpdate, user_id: str, users=user_service):
    return await users.update(user_id, user.__dict__)


@router.get('/email/{email}', name='Get User By Email', response_model=Optional[UserRead])
async def get_user_by_id(email: str, users=user_service):
    return await users.get_user_by_email(email)


@router.get('/phone/{phone}', name='Get User By Phone', response_model=Optional[UserRead])
async def user_by_phone(phone: str, users=user_service):
    return await users.get_user_by_phone(phone)


@router.get('/{user_id}', name='Get User By Id', response_model=Optional[UserRead])
async def get_user_by_id(user_id: str, users=user_service):
    return await users.id(user_id)


@router.delete('/{user_id}', name='Delete User By Id')
async def delete_user_by_id(user_id: str, users=user_service):
    return await users.delete(user_id)
