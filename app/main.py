from fastapi import FastAPI

from .healthcheck import healthcheck_router
from .posts.routers import post_router
from .users.routers import user_router

app = FastAPI(title="Weblog - Back-end")

app.include_router(router=healthcheck_router,prefix="/healthcheck", include_in_schema=False)
app.include_router(router=user_router, prefix="/users", include_in_schema=True)
app.include_router(router=post_router, prefix="/posts", include_in_schema=True)
