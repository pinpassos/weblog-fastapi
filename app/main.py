from fastapi import FastAPI

from .routers.healthcheck import router

app = FastAPI()
app.include_router(router=router, prefix="/healthcheck", include_in_schema=False)
