from fastapi import APIRouter, Depends, status

from schemas.pydantic.task_schema import (
    TaskPostRequestSchema,
    TaskSchema,
)
from services.task_service import TaskService

task_router = APIRouter(prefix="/v1/tasks", tags=["task"])
"""
Эндпроинты для управления задачами
"""


@task_router.post(
    "/",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    task: TaskPostRequestSchema,
    task_service: TaskService = Depends(),
):
    return task_service.create(task)
