from typing import List, Optional

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
    week: Optional[bool] = Query(
        None,
        description="Если True, возвращает задачи за неделю начиная с указанной date.",
    ),
    task_service: TaskService = Depends(),
):
    try:
        # Проверка на наличие одновременно 'date' и 'start_date'/'end_date'
        if date is not None and (
            start_date is not None or end_date is not None
        ):
            raise HTTPException(
                status_code=400,
                detail="Запрос не может одновременно содержать 'date' и 'start_date'/'end_date'. "
                "Пожалуйста, укажите только один из этих параметров.",
            )

        # Проверка на наличие одновременно 'week' и 'start_date'/'end_date'
        if week and (
            start_date is not None or end_date is not None
        ):
            raise HTTPException(
                status_code=400,
                detail="Запрос не может одновременно содержать 'week' и 'start_date'/'end_date'. "
                "Пожалуйста, укажите только один из этих параметров.",
            )

        # Проверка, что 'end_date' не может быть передан без 'start_date'
        if end_date and not start_date:
            raise HTTPException(
                status_code=422,
                detail="Поле 'start_date' обязательно при наличии 'end_date'.",
            )

        # Проверка, что 'start_date' не может быть передан без 'end_date'
        if start_date and not end_date:
            raise HTTPException(
                status_code=422,
                detail="Поле 'end_date' обязательно при наличии 'start_date'.",
            )

        # Логика обработки запросов
        if week and date:
            return await task_service.get_tasks_for_week(
                date
            )
        elif week and date is None:
            return await task_service.get_tasks_for_week(
                None
            )
        elif date:
            return await task_service.get_tasks_by_date(
                date
            )
        elif start_date and end_date:
            return await task_service.get_tasks_by_period(
                start_date, end_date
            )
        else:
            return await task_service.get_tasks_by_date(
                None
            )
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
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@task_router.delete(
    "/{task_id}", status_code=status.HTTP_200_OK
)
async def delete(
    task_id: int, task_service: TaskService = Depends()
) -> None:
    task_service.delete(task_id)
