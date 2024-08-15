from beanie import WriteRules
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient


class BaseRepository:
    model = None

    def __init__(self, client):
        self.client: AsyncIOMotorClient = client

    async def all(self):
        models = await self.model.all().to_list()

        if not models:
            return []

        return models

    async def id(self, model_id: str) -> model:
        model = await self.model.get(model_id)

        if model is not None:
            return model

        raise HTTPException(status_code=404, detail=f'object not found')

    async def create(self, data: dict) -> model:
        try:
            model = self.model(**data)
            model = await model.insert(link_rule=WriteRules.WRITE)
            return model

        except Exception as error:
            raise HTTPException(status_code=400, detail=f'{error}')

    async def delete(self, model_id: str) -> int:
        try:
            model = await self.model.get(model_id)

            if not model:
                raise HTTPException(404, "not found")

            await model.delete()
            return 200

        except Exception as error:
            raise HTTPException(500, f"{error}")

    async def update(self, model_id: str, update_data: dict) -> model:
        model = await self.id(model_id)

        for key, value in update_data.items():
            if value is not None:
                attr_value = getattr(model, key)
                attr_value = attr_value.lower() if isinstance(attr_value, str) else attr_value
                validate_value = value.lower() if isinstance(value, str) else value
                if attr_value == validate_value:
                    continue
                else:
                    setattr(model, key, value)

        await model.save()
        return model
