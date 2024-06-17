import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc",
              openapi_url="/api/openapi.json")


app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], max_age=3600)


# app.include_router(router=router)


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8006, reload=False)
