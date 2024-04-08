from datetime import datetime, timezone

from fastapi import Depends

from models.task_model import Task
from repositories.task_repository import TaskRepository
from schemas.pydantic.task_schema import (
    TaskPostRequestSchema,
)

MIN_TIMESTAMP = datetime(
    1970, 1, 2, tzinfo=timezone.utc
).timestamp()
MAX_TIMESTAMP = datetime(
    2038, 1, 18, tzinfo=timezone.utc
).timestamp()


class TaskService:
    __task_repository: TaskRepository

    def __init__(
        self, task_repository: TaskRepository = Depends()
    ) -> None:
        self.__task_repository = task_repository

    def create(
        self, task_content: TaskPostRequestSchema
    ) -> Task:
        return self.__task_repository.create(
            Task(
                title=task_content.title,
                description=task_content.description,
                due_date=task_content.due_date,
            )
        )

    async def get_tasks_by_period(
        self, start_date: int, end_date: int
    ):
        if (
            start_date < MIN_TIMESTAMP
            or start_date > MAX_TIMESTAMP
        ):
            raise ValueError(
                "start_date вне допустимого диапазона"
            )
        if (
            end_date < MIN_TIMESTAMP
            or end_date > MAX_TIMESTAMP
        ):
            raise ValueError(
                "end_date вне допустимого диапазона"
            )
        start_date_converted = datetime.fromtimestamp(
            start_date, timezone.utc
        )
        end_date_converted = datetime.fromtimestamp(
            end_date, timezone.utc
        )
        if start_date_converted >= end_date_converted:
            raise ValueError(
                "start_date должна быть меньше end_date"
            )

        return self.__task_repository.get_by_period(
            start_date_converted, end_date_converted
        )
