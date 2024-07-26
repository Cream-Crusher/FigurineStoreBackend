from pydantic import BaseModel
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

dev = True
service_env_directory = 'services/database_service/deploy/env/'
env_file = f"{service_env_directory}dev.env" if dev else f"{service_env_directory}prod.env"

load_dotenv(env_file)


class OAuth2Settings(BaseSettings):
    token_url: str
    scheme_name: str
    algorithm: str
    salt: str

    class Config:
        env_prefix = "OAUTHTWO_"


class APISettings(BaseSettings):
    environment: str
    title: str
    domain: str
    docs_user: str  # отключил мидлвейры
    docs_password: str  # отключил мидлвейры

    class Config:
        env_prefix = "API_"


class DatabaseSettings(BaseSettings):
    port: int
    host: str
    db: str
    user: str
    password: str
    # ssl_path: str

    url: str = ""

    class Config:
        env_prefix = "POSTGRES_"

    def __init__(self, **values):
        super().__init__(**values)
        self.url = self._assemble_database_url()

    def _assemble_database_url(self):
        ssl_part = "?ssl=verify-full" if not dev else ""
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}{ssl_part}"
        )


class AppSettings(BaseModel):
    database: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()
    OAuth2: OAuth2Settings = OAuth2Settings()


settings = AppSettings()
