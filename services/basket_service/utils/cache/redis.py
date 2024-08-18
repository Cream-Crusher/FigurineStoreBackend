import redis
import json

from fastapi import HTTPException


from services.auth_service.utils.base.config import settings


class RedisRepository:
    model = None

    def __init__(self):
        setting = settings.redis
        self.expire = 86400
        self.redis = redis.Redis(
            host=setting.host,
            port=setting.port,
            db=0,
            decode_responses=True
            # protocol=3
        )

    def valid_data(self, data: any) -> str:
        if isinstance(data, dict):
            model = self.model(**data)
            model = json.dumps(model)

        elif isinstance(data, object):
            model = json.dumps(data)

        else:
            model = str(data)

        return model

    async def is_key_exit(self, key):
        if not self.redis.exists(key):
            raise HTTPException(status_code=404, detail="Key not found")

    async def create(self, key: str, data: any) -> bool:
        try:
            valid_data = self.valid_data(data)
            self.redis.set(key, valid_data, self.expire)
            return True
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    async def get(self, key: str) -> any:
        try:
            data = self.redis.get(key)
            return self.model(**data)
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    async def update(self, key: str, data: dict) -> bool:
        try:
            model = self.model(**data)
            model = json.dumps(model)
            self.redis.set(key, model, self.expire)
            return True
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    async def delete(self, key: str) -> bool:
        try:
            await self.is_key_exit(key)
            return self.redis.delete(key)
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))


RedisRep = RedisRepository()
