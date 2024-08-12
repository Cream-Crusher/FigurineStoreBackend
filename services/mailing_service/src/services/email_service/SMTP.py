import httpx

from jinja2 import Template

from utils.base.config import settings


class SMTP:
    def __init__(self):
        self.base_api = "https://api.unisender.com/ru/api"
        self.session = httpx.AsyncClient()
        self.key = settings.unisender.token

    @staticmethod
    async def init_template(action: str) -> any:
        path = "src/services/email_service/template/"

        match action:
            case "Activate2FA":
                path += "Activate2FA.html"
            case "Login2FA":
                path += "Login2FA.html"
            case _:
                raise "Action not supported"

        with open(path, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()
            return Template(template_content)

    async def get_html_message(self, action: str, data: dict) -> any:
        template = await self.init_template(action)

        match action:
            case "Activate2FA":
                return template.render(
                    email=data.get('email'),
                    token=data.get('token')
                )
            case "Login2FA":
                return template.render(
                    code=data.get('code'),
                )
            case _:
                raise "Action not supported"

    async def send(self, data: dict, recipients: str, subject: str, action: str) -> dict:
        url = "https://api.unisender.com/ru/api/sendEmail"
        html_message = await self.get_html_message(action, data)
        form_data = {
            'api_key': self.key,
            'email': recipients,
            'sender_name': 'ESBlog',
            'sender_email': 'arkasaporo@gmail.com',
            'subject': subject,
            'body': html_message,
            'list_id': '1'
        }
        try:
            response = await self.session.post(url, data=form_data)
            return response.json()
        except Exception as e:
            print(f"An error occurred: {e}")

    async def activate_two_factor_authentication(self, data: dict, action: str) -> dict:
        subject = "Активация двухфакторной аунтификации"
        email = data.get('email')

        data = {
            "token": data.get('jwt_token')
        }
        return await self.send(recipients=email, subject=subject, action=action, data=data)

    async def send_login_code_to_email(self, data: dict, action: str) -> dict:
        subject = "Код подтверждения"
        email = data.get("email")

        data = {
            "code": data.get('code'),
        }
        return await self.send(recipients=email, subject=subject, action=action, data=data)


smtp = SMTP()
