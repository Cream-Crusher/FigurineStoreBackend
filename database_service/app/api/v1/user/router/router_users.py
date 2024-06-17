from typing import Union

from fastapi import APIRouter, HTTPException

from app.api.v1.user.schemas.schemas_users import UpdateUserData
from app.database.models.Users import Users
from app.database.repositories.UserRepository import UserRep

router = APIRouter(prefix='/api/v1/users', tags=['User|Users'])


@router.get('/', response_model=Users)
async def update_user_by_id(user_id: str, update_user: UpdateUserData) -> Union[Users, HTTPException]:
    try:
        user = await UserRep.update(user_id, update_user)

        if user is None:
            return HTTPException(404, 'User not found')

        return user

    except Exception as e:
        raise HTTPException(400, str(e))


@router.get('/email/{email}', name='Get User By Email', response_model=Users)
async def get_user_by_id(email: str) -> Union[Users, HTTPException]:
    try:
        user = await UserRep.get_user_by_phone(email)

        if user is None:
            return HTTPException(404, 'User not found')

        return user

    except Exception as e:
        raise HTTPException(400, str(e))


@router.get('/phone/{phone}', name='Get User By Phone', response_model=Users)
async def get_user_by_id(phone: str) -> Union[Users, HTTPException]:
    try:
        user = await UserRep.get_user_by_phone(phone)

        if user is None:
            return HTTPException(404, 'User not found')

        return user

    except Exception as e:
        raise HTTPException(400, str(e))


@router.get('/{user_id}', name='Get User By Id', response_model=Users)
async def get_user_by_id(user_id: str) -> Union[Users, HTTPException]:
    try:
        user = await UserRep.id(user_id)

        if user is None:
            return HTTPException(404, 'User not found')

        return user

    except Exception as e:
        raise HTTPException(400, str(e))


@router.get('/{user_id}', name='Delete User By Id')
async def delete_user_by_id(user_id: str) -> Union[int, HTTPException]:
    try:
        status = await UserRep.delete(user_id)

        if status is None:
            return HTTPException(404, 'User not found')

        return status

    except Exception as e:
        raise HTTPException(400, str(e))
