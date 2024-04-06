from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from configs import settings
from models.tags import tags
from routers.v1.task_router import task_router

# Инициализация веб-сервиса.
app = FastAPI(
    title=settings.app_title,
    version=settings.api_version,
    openapi_tags=tags,
)

# Подключение маршрутов.
app.include_router(task_router)


@app.exception_handler(HTTPException)
async def unicorn_exception_handler(
    request: Request, exc: HTTPException
):
    return JSONResponse(
        status_code=500,
        content={
            "msg": f"Произошла ошибка на стороне сервера. Пожалуйста, попробуйте еще раз позже."
        },
    )
