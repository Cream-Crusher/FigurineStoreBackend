import httpx

from jinja2 import Template

from utils.base.config import AppSettings


class SMTP:
    def __init__(self):
        super().__init__(base_api="https://api.unisender.com/ru/api")
        self.session = httpx.AsyncClient()
        self.key = AppSettings.unisender.token

    @staticmethod
    async def init_template(action: str) -> any:
        path = "services/email_service/template/"

        match action:
            case "Activate2FA":
                path += "Activate2FA.html"
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
            return await response.json()
        except Exception as e:
            print(f"An error occurred: {e}")

    async def activate_two_factor_authentication(self, email: str, token: str) -> dict:
        subject = "Двухфакторная защита успешно подключена"
        data = {"email": email, "code": token}
        return await self.send(recipients=email, subject=subject, action='Activate2FA', data=data)


smtp = SMTP()
