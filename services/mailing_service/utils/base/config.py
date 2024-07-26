from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

dev = True
service_env_directory = 'services/mailing_service/deploy/env/'
env_file = f"{service_env_directory}dev.env" if dev else f"{service_env_directory}prod.env"

load_dotenv(env_file)


class APISettings(BaseSettings):
    environment: str
    title: str
    domain: str
    docs_user: str
    docs_password: str

    class Config:
        env_prefix = "API_"


class AppSettings(BaseModel):
    api: APISettings = APISettings()


settings = AppSettings()
