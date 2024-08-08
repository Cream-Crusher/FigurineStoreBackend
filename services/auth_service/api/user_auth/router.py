from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from api.user_auth.schema import UserRead, UserCreate, UserAdminCreate, TwoFactorAuthentication, \
    TwoFactorAuthenticationConfirm
from api.user_auth.service import user_service
from utils.Auth.OTP import OTP
from utils.Auth.authentication import get_me, encode_token, decode_token
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
        user_id = data.get('user_id')
        email = data.get('email')
        secret = data.pop('secret')

        otp_code = await OTP.create_one_time_password(secret)
        await RedisRep.create(f'login_attempts_{user_id}', 0)
        token = await encode_token({"user_id": user_id, "code": otp_code, "email": email, "action": "Login2FA"})
        # todo тут метод отправки jwt токена с кодом по rabbimq к сервису рассылок
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


@router.post('/login_two_factor_authentication/confirm', name='verifying confirmation one time password for login', status_code=200)
async def verifying_confirmation_code_for_login(confirm: TwoFactorAuthenticationConfirm, users=user_service):
    payload = await decode_token(confirm.token)
    user_id = payload.get("user_id")
    code = payload.get("code")
    action = payload.get("action")

    if action != "Login2FA":
        raise HTTPException(status_code=400, detail="Invalid token action")

    await users.verifying_confirmation_code(user_id, code)

    user = await users.id(user_id)
    access_info = await users.build_assess_token(user)
    response = JSONResponse(content=access_info)
    response.set_cookie(key="refresh_token", value=access_info.get('refresh_token'), secure=True, samesite="none")
    response.set_cookie(key="access_token", value=access_info.get('access_token'), secure=True, samesite="none")
    response.headers["Authorization"] = f"Bearer {access_info.get('access_token')}"
    return response


@router.post('/activate_2fa', name='activate 2fa', status_code=200)
async def activate_2fa(activate: TwoFactorAuthentication, users=user_service):
    email = activate.email

    users = await users.get('email', email)
    if not users:
        raise HTTPException(status_code=404, detail="Email not found")

    token = await encode_token({"email": email, "action": "Activate2FA"})
    # todo тут метод отправки jwt токена с кодом по rabbimq к сервису рассылок
    return 201


@router.post('/activate_2fa/confirm', name='activate 2fa', status_code=200)
async def activate_2fa_confirm(activate: TwoFactorAuthenticationConfirm, users=user_service):
    payload = await decode_token(activate.token)
    email = payload.get('email')
    action = payload.get("action")

    if action != "Activate2FA":
        raise HTTPException(status_code=400, detail="Invalid token action")

    return users.activate_two_factor_authentication(email)
