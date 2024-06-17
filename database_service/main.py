import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.user.router.router_users import router as router_users

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc",
              openapi_url="/api/openapi.json")


app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], max_age=3600)


app.include_router(router=router_users)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8006, reload=True)
