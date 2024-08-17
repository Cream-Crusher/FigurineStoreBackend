from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from services.catalog_service.utils.base.config import settings


class AsyncDatabaseClient:
    def __init__(self):
        db = settings.database

        self.client = AsyncIOMotorClient(db.url)

    async def init_db(self, db: str, models: list):
        await init_beanie(database=self.client[db], document_models=models)

    def get_client(self):
        return self.client


AsyncDatabase = AsyncDatabaseClient()
