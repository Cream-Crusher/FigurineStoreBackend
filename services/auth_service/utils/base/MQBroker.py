import asyncio
from aio_pika import connect, Message


class MQBroker:
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect(self.url)
        self.channel = await self.connection.channel()

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def send_message(self, routing_key: str, message: str):
        if not self.channel:
            await self.connect()

        await self.channel.default_exchange.publish(Message(body=message.encode('utf-8')), routing_key=routing_key)

    async def create_queue(self, queue_name: str):
        if not self.channel:
            await self.connect()

        return await self.channel.declare_queue(queue_name, durable=True)
