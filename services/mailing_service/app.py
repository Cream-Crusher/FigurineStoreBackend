import asyncio

from services.mailing_service.src.broker_handler import Handlerbroker
from infrastructure.rabbitMQ.MQBroker import MQBroker


async def main():
    queue_email = asyncio.create_task(MQBroker.consume_messages('email', Handlerbroker.handler_email_queue))

    await asyncio.gather(queue_email)

if __name__ == '__main__':
    asyncio.run(main())
