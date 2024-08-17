import json

from aio_pika import connect, Message

from services.auth_service.utils.base.config import settings


class RabbitMQ:
    def __init__(self):
        rabbit_setting = settings.rabbit_mq

        self.url = rabbit_setting.url
        self.connection = None
        self.channel = None

    @staticmethod
    async def valid_data(value: any) -> str:
        if isinstance(value, dict):
            value = json.dumps(value)

        return value

    async def connect(self):
        self.connection = await connect(self.url)
        self.channel = await self.connection.channel()

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def send_message(self, routing_key: str, message: str | dict):
        if not self.channel:
            await self.connect()

        message = await self.valid_data(message)

        await self.channel.default_exchange.publish(Message(body=message.encode('utf-8')), routing_key=routing_key)

    async def create_queue(self, queue_name: str):
        if not self.channel:
            await self.connect()

        return await self.channel.declare_queue(queue_name, durable=True)

    async def consume_messages(self, queue_name: str, callback):
        queue = await self.create_queue(queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = message.body.decode()
                    await callback(data)


MQBroker = RabbitMQ()
