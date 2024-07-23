import bcrypt

from datetime import datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, update

from api.user_auth.model import Users
from utils.Auth.authentication import create_access_token, create_refresh_token
from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase


class UserService(BaseRepository):
    model = Users

    @staticmethod
    async def password_validate(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    async def get(self, by: str, value: str | int) -> Users:
        match by:
            case 'username':
                query = func.lower(Users.username) == value.lower()
            case _:
                raise HTTPException(404, detail=f'{by} not valid')

        result = await self.filter(query)

        return result.first()

    async def create_user(self, user_data: dict) -> Users:
        user_data['password'] = await self.password_validate(user_data['password'])
        user = Users(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def login(self, login: OAuth2PasswordRequestForm = Depends()):
        username, password = login.username, login.password

        user = await self.get(by='username', value=username)

        if not user:
            raise HTTPException(404, detail='user not valid')

        if user.active is False:
            raise HTTPException(404, detail='user deactivated')

        if not user.verify_password(password, user.password):
            raise HTTPException(404, detail='user not valid')

        to_encode = {
            "user_id": str(user.id),
            "username": user.username,
            "fullname": user.fullname
        }
        access_token = await create_access_token(data=to_encode)
        refresh_token = await create_refresh_token(data=to_encode)

        user.refresh_token = refresh_token
        user.latest_auth = datetime.utcnow()
        await self.session.commit()

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    async def delete_refresh_token(self, user_id: str):
        user = await self.session.get(Users, user_id)
        user.refresh_token = ''

        await self.session.commit()


async def get_user_service(session=Depends(AsyncDatabase.get_session)):
    return UserService(session)


user_service: UserService = Depends(get_user_service)
