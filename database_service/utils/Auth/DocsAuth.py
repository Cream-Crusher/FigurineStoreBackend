import base64

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from utils.base.config import settings


class ApiDocBasicAuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path in ['/api/v1/auth/login']:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                try:
                    scheme, credentials = auth_header.split()
                    if scheme.lower() == 'basic':
                        decoded = base64.b64decode(credentials).decode('ascii')
                        username, password = decoded.split(':')
                        correct_username = settings.api.docs_user == username
                        correct_password = settings.api.docs_password == password

                        if correct_username and correct_password:
                            return await call_next(request)
                except Exception:
                    raise HTTPException(401, "Unauthorized")

            response = Response(content='Unauthorized', status_code=401)
            response.headers['WWW-Authenticate'] = 'Basic'
            return response

        return await call_next(request)
