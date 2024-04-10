from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from schemas.pydantic.task_schema import (
    TaskPostRequestSchema,
    TaskPutRequestSchema,
    TaskResponseSchema,
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


@task_router.get(
    "/",
    response_model=List[TaskResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    start_date: str = Query(
        ...,
        description="Начальная дата в формате даты (гггг-мм-дд)",
    ),
    end_date: str = Query(
        ...,
        description="Конечная дата в формате даты (гггг-мм-дд)",
    ),
    task_service: TaskService = Depends(),
):
    try:
        tasks = await task_service.get_tasks_by_period(
            start_date, end_date
        )
        return tasks
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@task_router.put("/{task_id}")
async def update(
    task_id: int,
    task: TaskPutRequestSchema,
    task_service: TaskService = Depends(),
):
    try:
        upd_task = task_service.update(task_id, task)
        if not upd_task:
            raise HTTPException(
                status_code=404,
                detail=f"Задача по идентификатору '{task_id}' не найдена",
            )
        return upd_task
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
