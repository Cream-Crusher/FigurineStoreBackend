from app.database.session import AsyncDatabase
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from datetime import datetime

from functools import wraps


def session_handler(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if "session" in kwargs:
            session = kwargs["session"]
        else:
            session: AsyncSession = await AsyncDatabase.return_session()
        try:
            result = await func(self, session, *args, **kwargs)
        except DBAPIError as e:
            result = await func(self, session, *args, **kwargs)
        finally:
            if "session" not in kwargs:
                await session.close()
        return result

    return wrapper


class BaseRepository:
    model = None

    @session_handler
    async def all(self, session):
        result = await session.scalars(select(self.model).where(self.model.active.is_(True)))
        if not result:
            return []
        return result.all()

    @session_handler
    async def id(self, session, model_id: str) -> object:
        model = await session.get(self.model, model_id)
        if model is not None:
            return model

    @session_handler
    async def create(self, session, data: dict):
        try:
            model = self.model(**data)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model
        except IntegrityError as error:
            pass

    @session_handler
    async def delete(self, session, model_id: str):
        model = await self.id(model_id)
        await session.delete(model)
        await session.commit()
        return 200

    @session_handler
    async def update(self, session, model_id: str, update_data: dict):
        model = await self.id(model_id)
        for key, value in update_data.items():
            if value is not None:
                setattr(model, key, value)
        model.updated_at = datetime.utcnow()
        await session.commit()
        return model
