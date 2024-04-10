from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from repositories.task_repository import (
    TaskNotFoundException,
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


@task_router.put(
    "/{task_id}",
    response_model=TaskPutRequestSchema,
    status_code=status.HTTP_200_OK,
)
@task_router.put("/{task_id}")
async def update(
    task_id: int,
    task: TaskPutRequestSchema,
    task_service: TaskService = Depends(),
):
    try:
        return task_service.update(task_id, task)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
