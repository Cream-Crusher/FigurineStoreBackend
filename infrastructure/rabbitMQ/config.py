from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

dev = True
env_file = "deploy/env/dev.env" if dev else "deploy/env/prod.env"

load_dotenv(env_file)


class RabbitMQSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: str

    class Config:
        env_prefix = "RABBITMQ"

    def __init__(self, **values):
        super().__init__(**values)
        self.url = self._assemble_rabbit_url()

    def _assemble_rabbit_url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}/{self.port}"


class RabbitSettings(BaseModel):
    rabbit_mq: RabbitMQSettings = RabbitMQSettings()


settings = RabbitSettings()
