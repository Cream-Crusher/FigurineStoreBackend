import asyncio

from services.mailing_service.src.handler import Handlerbroker
from services.mailing_service.utils.broker.MQBroker import MQBroker


async def main():
    queue_email = asyncio.create_task(MQBroker.consume_messages('email', Handlerbroker.handler_email_queue))

    await asyncio.gather(queue_email)

if __name__ == '__main__':
    asyncio.run(main())
