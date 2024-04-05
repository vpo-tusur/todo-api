from fastapi import FastAPI
from models.tags import tags

from configs import settings
from routers.v1.task_router import task_router

# Core Application Instance
app = FastAPI(
    title=settings.app_title,
    version=settings.api_version,
    openapi_tags=tags,
)


# Add Routers
app.include_router(task_router)
