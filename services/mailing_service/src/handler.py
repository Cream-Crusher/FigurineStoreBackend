from src.services.email_service.SMTP import smtp
from utils.broker.MQBroker import MQBroker


class HandlerMQBroker:

    @staticmethod
    async def handler_email_queue(data: dict):
        email = data.get('email')
        token = data.get('token')

        test = await smtp.activate_two_factor_authentication(email=email, token=token)
        print(test)
        # "Login2FA"Activate2FA


Handlerbroker: HandlerMQBroker = HandlerMQBroker()
