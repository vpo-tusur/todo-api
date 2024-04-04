from fastapi import FastAPI
from metadata.tags import tags
from routers.v1.task_router import task_router
from configs import settings

# Core Application Instance
app = FastAPI(
    title=settings.app_title,
    version=settings.api_version,
    openapi_tags=tags,
)

# Add Routers
app.include_router(task_router)
