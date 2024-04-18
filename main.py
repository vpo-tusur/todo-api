from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from configs import settings
from models.tags import tags
from repositories.task_repository import (
    TaskNotFoundException,
)
from routers.v1.task_router import task_router

# Инициализация веб-сервиса.
app = FastAPI(
    title=settings.app_title,
    version=settings.api_version,
    openapi_tags=tags,
)

# Подключение маршрутов.
app.include_router(task_router)


@app.exception_handler(TaskNotFoundException)
async def task_not_found_exception_handler(
    request: Request, exc: TaskNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=({"msg": exc.message}),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request, exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=(
            {"msg": exc.detail}
            if exc.detail
            else {
                "msg": "Произошла ошибка на стороне сервера. Пожалуйста, попробуйте еще раз позже."
            }
        ),
    )
