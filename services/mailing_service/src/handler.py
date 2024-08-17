import json

from services.mailing_service.src.email.SMTP import smtp


class HandlerMQBroker:

    @staticmethod
    async def handler_email_queue(data: str):
        try:
            data = json.loads(data)
            action = data.get('action')

            match action:
                case "Activate2FA":
                    await smtp.activate_two_factor_authentication(data=data, action=action)
                case "Login2FA":
                    await smtp.send_login_code_to_email(data, action)
                case _:
                    raise "Action not supported"

        except Exception as e:
            print(e)  # todo залогировать ошибки


Handlerbroker: HandlerMQBroker = HandlerMQBroker()
