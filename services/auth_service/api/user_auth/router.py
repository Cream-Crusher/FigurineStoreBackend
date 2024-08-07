import random

import pyotp
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from api.user_auth.schema import UserRead, UserCreate, UserAdminCreate
from api.user_auth.service import user_service
from utils.Auth.OTP import OTP
from utils.Auth.authentication import get_me
from utils.cache.redis import RedisRep

router = APIRouter(prefix='/auth', tags=['User|Authentication'])


@router.post('/register', name='Register User', response_model=UserRead, status_code=201)
async def register_user(user: UserCreate, users=user_service):
    return await users.create_user(user.__dict__)


@router.post('/register-admin', name='Register Admin', response_model=UserRead, status_code=201)
async def create_user_admin(user: UserAdminCreate, users=user_service, me=Depends(get_me)):
    if me.role != "admin":
        raise HTTPException(status_code=403, detail="You are not admin")

    return await users.create_user({**user.__dict__, "role": "admin"})


@router.post('/login', name='login', status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), users=user_service):
    data = await users.login(form_data)
    two_factor_authentication = data.pop('2fa')

    if two_factor_authentication:
        return data

    access_info = data
    response = JSONResponse(content=access_info)
    response.set_cookie(key="refresh_token", value=access_info.get('refresh_token'), secure=True, samesite="none")
    response.set_cookie(key="access_token", value=access_info.get('access_token'), secure=True, samesite="none")
    response.headers["Authorization"] = f"Bearer {access_info.get('access_token')}"
    return response


@router.post('/logout', name='logout', status_code=200)
async def logout(response: JSONResponse, users=user_service, me=Depends(get_me)):
    await users.delete_refresh_token(me.id)
    response.delete_cookie(key="refresh_token", secure=True, samesite="none")
    response.delete_cookie(key="access_token", secure=True, samesite="none")

    return JSONResponse(content={"message": "Logout successful"})


@router.post('/refresh')
async def refresh(refresh_token: str = None, me=Depends(get_me), users=user_service):
    access_info = await users.refresh(refresh_token)
    response = JSONResponse(content=access_info)
    response.set_cookie(key="access_token", value=access_info.get('access_token'), secure=True, samesite="none")
    response.headers["Authorization"] = f"Bearer {access_info.get('access_token')}"
    return response


@router.post('/verifying_confirmation_code_for_login', name='verifying confirmation code', status_code=200)
async def verifying_confirmation_code_for_login(user_id: str, code: str, users=user_service):
    await users.verifying_confirmation_code(user_id, code)

    user = await users.id(user_id)
    access_info = await users.build_assess_token(user)
    response = JSONResponse(content=access_info)
    response.set_cookie(key="refresh_token", value=access_info.get('refresh_token'), secure=True, samesite="none")
    response.set_cookie(key="access_token", value=access_info.get('access_token'), secure=True, samesite="none")
    response.headers["Authorization"] = f"Bearer {access_info.get('access_token')}"
    return response


@router.post('/send_code_by_email', name='send confirmation code by email', status_code=200)
async def send_confirmation_code_by_email(user_id: str, users=user_service):
    user = await users.id(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    opt_code = await OTP.create_one_time_password(user.secret)
    await RedisRep.create(f'login_attempts_{user_id}', 0)
    print(opt_code)
    # todo тут метод отправки кода по rabbimq к сервису рассылок
    return {
        'details': 'code sent successfully'
    }


#  todo ендпоинт подтверждения 2fa
