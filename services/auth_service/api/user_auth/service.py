import bcrypt

from datetime import datetime

import pyotp
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func

from api.user_auth.model import Users
from utils.Auth.OTP import OTP
from utils.Auth.authentication import create_access_token, create_refresh_token
from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase
from utils.cache.redis import RedisRep


class UserService(BaseRepository):
    model = Users

    @staticmethod
    async def password_validate(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    async def get_two_factor_authentication_data(user: Users) -> dict:
        return {
            'user_id': user.id,
            'email': user.email,
            'secret': user.secret,
            'details': '2FA: send code by email'
        }

    async def get(self, by: str, value: str | int) -> Users:
        match by:
            case 'username':
                query = func.lower(Users.username) == value.lower()
            case 'refresh_token':
                query = func.lower(Users.refresh_token) == value.lower()
            case 'email':
                query = func.lower(Users.email) == value.lower()
            case _:
                raise HTTPException(404, detail=f'{by} not valid')

        result = await self.filter(query)

        return result.first()

    async def create_user(self, user_data: dict) -> Users:
        user_data['password'] = await self.password_validate(user_data['password'])
        secret = await OTP.generate_random_secrets()

        user_data.update({'secret': secret})

        user = Users(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def activate_two_factor_authentication(self, email: str) -> Users:
        user = await self.get('email', email)

        if not user:
            raise HTTPException(404, detail='user not valid')

        user.email = email
        user.two_factor_authentication = True
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def build_assess_token(self, user: Users) -> dict:
        to_encode = {
            "user_id": str(user.id),
            "username": user.username,
            "fullname": user.fullname,
        }
        access_token = await create_access_token(data=to_encode)
        refresh_token = await create_refresh_token(data=to_encode)

        user.refresh_token = refresh_token
        user.latest_auth = datetime.utcnow()
        await self.session.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def login(self, login: OAuth2PasswordRequestForm = Depends(), ignore_2fa: bool = False) -> dict:
        username, password = login.username, login.password

        user = await self.get(by='username', value=username)

        if not user:
            raise HTTPException(404, detail='user not valid')

        if user.active is False:
            raise HTTPException(404, detail='user deactivated')

        if not user.verify_password(password, user.password):
            raise HTTPException(404, detail='user not valid')

        if user.two_factor_authentication or ignore_2fa:
            base_user_info = await self.get_two_factor_authentication_data(user)
            return {
                **base_user_info,
                '2fa': True
            }
        assess_token = await self.build_assess_token(user)

        return {
            **assess_token,
            '2fa': False
        }

    async def refresh(self, refresh_token):
        user = await self.get(by='refresh_token', value=refresh_token)

        if not user:
            raise HTTPException(404, detail='user not valid')

        to_encode = {
            "user_id": str(user.id),
            "username": user.username
        }
        access_token = await create_access_token(data=to_encode)

        return {"access_token": access_token, "token_type": "bearer"}

    async def delete_refresh_token(self, user_id: str):
        user = await self.session.get(Users, user_id)
        user.refresh_token = ''

        await self.session.commit()

    async def verifying_confirmation_code(self, user_id: str, code: str) -> bool:
        login_attempts = await RedisRep.get(f'login_attempts_{user_id}')

        if login_attempts is None:
            raise HTTPException(
                status_code=403,
                detail="Code has expired"
            )

        if int(login_attempts) >= 5:
            raise HTTPException(
                status_code=403,
                detail="The number of login attempts has been exceeded, please try again later"
            )

        user = await self.id(user_id)
        secret = user.secret

        if not await OTP.verify_one_time_password(secret, code):
            await RedisRep.update(f'login_attempts_{user_id}', login_attempts+1)
            raise HTTPException(status_code=403, detail="Code is invalid")

        return True


async def get_user_service(session=Depends(AsyncDatabase.get_session)):
    return UserService(session)


user_service: UserService = Depends(get_user_service)
