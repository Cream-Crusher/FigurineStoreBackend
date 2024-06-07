from pathlib import Path

from dataclasses import dataclass

from environs import Env

dev = True

env = Env()
env.read_env('dev.env' if dev else '.env')
WORK_PATH: Path = Path(__file__).parent.parent


@dataclass
class Database:
    port = env.str("POSTGRES_PORT")
    host = env.str("POSTGRES_HOST")
    db = env.str("POSTGRES_DB")
    user = env.str("POSTGRES_USER")
    password = env.str("POSTGRES_PASSWORD")
    ssl = env.str("SSL_PATH", None)
    url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
