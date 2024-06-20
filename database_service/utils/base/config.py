from dataclasses import dataclass

from environs import Env
from pydantic import BaseModel

dev = True
env_file = "deploy/env/dev.env" if dev else "deploy/env/.env"

env = Env()
env.read_env(env_file)


@dataclass
class APISettings:
    environment = env.str('ENVIRONMENT')
    title = env.str('TITLE')
    domain = env.str('DOMAIN')
    docs_user = env.str('DOCS_USER')
    docs_password = env.str('DOCS_PASSWORD')

    class Config:
        env_prefix = "API_"


@dataclass
class DatabaseSettings:
    host = env.str('POSTGRES_HOST'),
    password = env.str('POSTGRES_PASSWORD'),
    user = env.str('POSTGRES_USER'),
    database = env.str('POSTGRES_DB'),
    port = env.str('POSTGRES_PORT'),
    # ssl_path: env.str('SSL_PATH')
    url = f"postgresql+asyncpg://{env.str('POSTGRES_USER')}:{env.str('POSTGRES_PASSWORD')}@{env.str('POSTGRES_HOST')}:{env.str('POSTGRES_PORT')}/{env.str('POSTGRES_DB')}",

    class Config:
        env_prefix = "DB_"


class AppSettings(BaseModel):
    database: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()


settings = AppSettings()
