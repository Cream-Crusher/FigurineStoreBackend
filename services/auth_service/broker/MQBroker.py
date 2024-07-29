import asyncio
from aio_pika import connect, Message

from utils.base.config import settings


class MQBroker:
    def __init__(self):
        rabbit_setting = settings.rabbit_mq

        self.url = rabbit_setting.url
        self.connection = None
        self.channel = None
        # self.queues = {}

    async def connect(self):
        self.connection = await connect(self.url)
        self.channel = await self.connection.channel()

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def send_message(self, routing_key: str, message: str):
        if not self.channel:
            await self.connect()

        # await self.create_queue(routing_key)

        await self.channel.default_exchange.publish(Message(body=message.encode('utf-8')), routing_key=routing_key)

    async def create_queue(self, queue_name: str):
        if not self.channel:
            await self.connect()

        return await self.channel.declare_queue(queue_name, durable=True)

        # if queue_name not in self.queues:
        #     queue = await self.channel.declare_queue(queue_name, durable=True)
        #     self.queues[queue_name] = queue
        #     return queue
        # else:
        #     return self.queues[queue_name]

    async def consume_messages(self, queue_name: str, callback):
        queue = await self.create_queue(queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = message.body.decode()
                    await callback(data)
