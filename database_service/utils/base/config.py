from pydantic import BaseModel
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

dev = True
env_file = "deploy/env/dev.env" if dev else "deploy/env/prod.env"

load_dotenv(env_file)


class APISettings(BaseSettings):
    environment: str
    title: str
    domain: str
    docs_user: str
    docs_password: str

    class Config:
        env_prefix = "API_"


class DatabaseSettings(BaseSettings):
    postgres_port: int
    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    # ssl_path: str

    url: str = ""

    class Config:
        env_prefix = "DB_"

    def __init__(self, **values):
        super().__init__(**values)
        self.url = self._assemble_database_url()

    def _assemble_database_url(self):
        ssl_part = "?ssl=verify-full" if not dev else ""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}{ssl_part}"
        )


class AppSettings(BaseModel):
    database: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()


settings = AppSettings()
