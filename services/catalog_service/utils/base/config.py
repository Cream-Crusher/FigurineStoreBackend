from pydantic import BaseModel
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

dev = True
deploy_path = 'services/catalog_service/deploy/env/'
env_file = f"{deploy_path}dev.env" if dev else f"{deploy_path}prod.env"

load_dotenv(env_file)


class APISettings(BaseSettings):
    environment: str
    title: str
    domain: str
    docs_user: str  # отключил мидлвейры
    docs_password: str  # отключил мидлвейры

    class Config:
        env_prefix = "API_"


class DatabaseSettings(BaseSettings):
    host: str
    post: str
    username: str
    password: str

    url: str = ''

    class Config:
        env_prefix = "MONGO_"

    def __init__(self, **values):
        super().__init__(**values)
        self.url = self._assemble_database_url()

    def _assemble_database_url(self):
        return (
            f"mongodb://{self.username}:{self.password}@{self.host}:{self.post}"
        )


class AppSettings(BaseModel):
    database: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()


settings = AppSettings()
