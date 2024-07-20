import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from api.blog.router import router as blog_router
from api.comment.router import router as comment_router
from api.post.router import router as post_router
from api.tag.router import router as tag_router
from api.user.router import router as user_router
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
    origins = ['https://title_company.database.ru']

else:
    origins = ["localhost", "127.0.0.1", "0.0.0.0"]

# app.add_middleware(ApiDocBasicAuthMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*", "OPTIONS"],
                   allow_headers=["*"], max_age=3600)

router = APIRouter(prefix=f'/{service_title}/api/v1', tags=[''])

router.include_router(user_router)
router.include_router(blog_router)
router.include_router(tag_router)
router.include_router(post_router)
router.include_router(comment_router)


@router.get("/ping", tags=["Server"])
async def ping_server():
    return "pong"


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8001, reload=True)
