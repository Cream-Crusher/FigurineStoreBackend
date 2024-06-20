from typing import Optional

from fastapi import APIRouter

from api.user.schema import UserRead, UserUpdate
from api.user.service import user_service

router = APIRouter(prefix='/api/v1/users', tags=['User|Users'])


@router.patch('/', response_model=Optional[UserRead])
async def update_user_by_id(user: UserUpdate, user_id: str, users=user_service):
    return await users.update(user_id, user.__dict__)


@router.get('/email/{email}', name='Get User By Email', response_model=Optional[UserRead])
async def get_user_by_id(email: str, users=user_service):
    return await users.get_user_by_email(email)


@router.get('/phone/{phone}', name='get user by phone', response_model=Optional[UserRead])
async def user_by_phone(phone: str, users=user_service):
    return await users.get_user_by_phone(phone)


@router.get('/{user_id}', name='Get User By Id', response_model=Optional[UserRead])
async def get_user_by_id(user_id: str, users=user_service):
    return await users.id(user_id)


@router.delete('/{user_id}', name='Delete User By Id')
async def delete_user_by_id(user_id: str, users=user_service):
    return await users.delete(user_id)
