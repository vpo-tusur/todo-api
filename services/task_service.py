from datetime import date
from typing import List

from dateutil import parser, tz
from fastapi import Depends

from models.task_model import Task
from repositories.task_repository import TaskRepository
from schemas.pydantic.task_schema import (
    TaskPostRequestSchema,
)


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
        self, start_date_str: str, end_date_str: str
    ) -> List[Task]:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
        validate_dates(start_date, end_date)

        return self.__task_repository.get_by_period(
            start_date, end_date
        )


def parse_date(date_str: str) -> date:
    try:
        parsed_datetime = parser.parse(date_str)
        if parsed_datetime.tzinfo is None:
            parsed_datetime = parsed_datetime.replace(
                tzinfo=tz.UTC
            )
        return parsed_datetime.date()
    except ValueError as e:
        raise ValueError(
            f"Некорректный формат даты: {date_str}"
        ) from e


def validate_dates(start_date: date, end_date: date):
    if start_date > end_date:
        raise ValueError(
            "start_date должна быть меньше или равна end_date"
        )
