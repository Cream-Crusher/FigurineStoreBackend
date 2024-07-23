import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from api.user_auth.router import router as auth_router
from utils.base.config import settings

service_title = settings.api.title

app = FastAPI(
    title=service_title,
    docs_url=f'/{service_title}/api/docs',
    openapi_url=f'/{service_title}/api/openapi.json',
    redoc_url=f'/{service_title}/api/redoc',
    swagger_ui_parameters={
        'docExpansion': 'none',
        'persistAuthorization': 'true',
        'defaultModelRendering': 'model'
    }
)

if settings.api.environment == 'prod':
    origins = ['https://title_company.auth.ru']

else:
    origins = ["http://localhost"]

# app.add_middleware(ApiDocBasicAuthMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*", "OPTIONS"],
                   allow_headers=["*"], max_age=3600)

router = APIRouter(prefix=f'/{service_title}/api/v1', tags=[''])

router.include_router(auth_router)


@router.get("/ping", tags=["Server"])
async def ping_server():
    return "pong"


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)
