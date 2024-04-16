from typing import List, Optional

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
    date: Optional[str] = Query(
        None, description="Дата в формате (гггг-мм-дд)"
    ),
    start_date: Optional[str] = Query(
        None,
        description="Начальная дата в формате (гггг-мм-дд)",
    ),
    end_date: Optional[str] = Query(
        None,
        description="Конечная дата в формате (гггг-мм-дд)",
    ),
    task_service: TaskService = Depends(),
):
    try:
        tasks = []
        if date is not None and (
            start_date is not None or end_date is not None
        ):
            raise HTTPException(
                status_code=400,
                detail="Запрос не может одновременно содержать 'date' и 'start_date'/'end_date'. "
                "Пожалуйста, укажите только один из этих параметров.",
            )
        if date is not None:
            tasks = await task_service.get_tasks_by_date(
                date
            )
        elif (
            start_date is not None and end_date is not None
        ):
            tasks = await task_service.get_tasks_by_period(
                start_date, end_date
            )
        else:
            tasks = await task_service.get_tasks_by_date(
                None
            )

        return tasks
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail={"msg": "Некорректный формат даты."},
        )


@task_router.put(
    "/{task_id}",
    response_model=TaskPutRequestSchema,
    status_code=status.HTTP_200_OK,
)
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
