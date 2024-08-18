from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

dev = True
deploy_path = 'services/basket_service/deploy/env/'
env_file = f"{deploy_path}dev.env" if dev else f"{deploy_path}prod.env"

load_dotenv(env_file)


class APISettings(BaseSettings):
    environment: str
    title: str
    domain: str
    docs_user: str
    docs_password: str

    class Config:
        env_prefix = "API_"


class RabbitMQSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: str

    url: str = ""

    class Config:
        env_prefix = "RABBITMQ_"

    def __init__(self, **values):
        super().__init__(**values)
        self.url = self._assemble_rabbit_url()

    def _assemble_rabbit_url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}/"  # {self.port}


class RedisSettings(BaseSettings):
    host: str
    password: str
    port: str

    class Config:
        env_prefix = "REDIS_"


class AppSettings(BaseModel):
    api: APISettings = APISettings()
    rabbit_mq: RabbitMQSettings = RabbitMQSettings()
    redis: RedisSettings = RedisSettings()


settings = AppSettings()
