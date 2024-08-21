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

    async def build_key(self, key: str) -> str:
        return f'{self.model}_{key}'

    async def valid_data(self, data: any) -> str:
        if isinstance(data, dict):
            model = await self.model(**data)
            model = json.dumps(model.dict())

        elif isinstance(data, object):
            model = json.dumps(data.dict())
        else:
            model = str(data)

        return model

    async def is_key_exit(self, key: str):
        if not self.redis.exists(key):
            raise HTTPException(status_code=404, detail="Key not found")

    async def create(self, key: str, data: any) -> bool:
        try:
            key = await self.build_key(key)
            valid_data = await self.valid_data(data)
            self.redis.set(key, valid_data, self.expire)
            return True
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    async def get(self, key: str) -> model:
        try:
            key = await self.build_key(key)
            data = self.redis.get(key)
            json_data = json.loads(data)
            return self.model(**json_data)
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    async def update(self, key: str, update_data: dict) -> bool:
        try:
            model = await self.get(key)
            redis_key = await self.build_key(key)

            for key, value in update_data.items():
                if value is not None:
                    attr_value = getattr(model, key)
                    attr_value = attr_value.lower() if isinstance(attr_value, str) else attr_value
                    validate_value = value.lower() if isinstance(value, str) else value
                    if attr_value == validate_value:
                        continue
                    else:
                        setattr(model, key, value)

            valid_data = await self.valid_data(model)

            self.redis.set(redis_key, valid_data, self.expire)
            return True

        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    async def delete(self, key: str) -> bool:
        try:
            key = await self.build_key(key)
            await self.is_key_exit(key)
            return self.redis.delete(key)
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))


RedisRep = RedisRepository()
