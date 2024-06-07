from sqlalchemy import exc
import sqlalchemy.engine.url as SQURL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from database_service.app.config import Database


class AsyncDatabaseSessions:
    def __init__(self):
        self.URL = SQURL.URL.create(
            drivername="postgresql+asyncpg",
            username=Database.user,
            password=Database.password,
            host=Database.host,
            port=Database.port,
            database=Database.db,
        )

        self.engine = create_async_engine(self.URL, pool_size=50, max_overflow=-1)
        self.factory = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def get_url(self):
        return str(self.URL)

    def get_session_maker(self) -> async_sessionmaker:
        return self.factory

    async def get_session(self) -> AsyncSession:
        async with self.factory() as session:
            try:
                yield session
            except exc.SQLAlchemyError as error:
                await session.rollback()
                raise

    async def return_session(self) -> AsyncSession:
        return self.factory()


AsyncDatabase = AsyncDatabaseSessions()
