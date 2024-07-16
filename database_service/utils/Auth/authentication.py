import jose

from jose import jwt

from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select

from api.user.model import Users
from utils.base.config import settings
from utils.base.session import AsyncDatabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.OAuth2.token_url, scheme_name=settings.OAuth2.scheme_name)
KEY = settings.OAuth2.salt
ALGORITHM = settings.OAuth2.algorithm


async def get_me(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")
    try:
        payload = jwt.decode(token=token, key=KEY, algorithms=[ALGORITHM])

    except jose.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token: " + str(e))

    if payload.get("exp") and payload["exp"] < datetime.timestamp(datetime.utcnow()):
        raise HTTPException(status_code=401, detail="Token expired")

    session = await AsyncDatabase.return_session()

    try:
        query = await session.scalars(select(Users).where(Users.id == payload.get('user_id')))
        user = query.first()

        if user.active is False:
            raise HTTPException(status_code=401, detail="User deactivate")

        return user
    finally:
        await session.close()
