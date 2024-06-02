from datetime import date, timedelta
from typing import List, Optional

from dateutil import parser, tz
from fastapi import Depends

from models.task_model import Task
from repositories.task_repository import TaskRepository
from schemas.pydantic.task_schema import (
    TaskPostRequestSchema,
    TaskPutRequestSchema,
    TaskMultipleRequestSchema,
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

    def mass_crete(
            self, tasks: TaskMultipleRequestSchema,
    ) -> list[Task]:
        created = []
        for task in tasks.tasks:
            created.append(self.__task_repository.create(
                Task(
                    title=task.title,
                    description=task.description,
                    due_date=tasks.due_date,
                )
            ))
        return created

    def update(
        self,
        task_id: int,
        task_content: TaskPutRequestSchema,
    ) -> Task:
        return self.__task_repository.update(
            Task(
                id=task_id,
                title=task_content.title,
                description=task_content.description,
                due_date=task_content.due_date,
            )
        )

    def delete(self, task_id: int) -> Task:
        return self.__task_repository.delete(task_id)

    async def get_tasks_by_period(
        self,
        start_date_str: Optional[str],
        end_date_str: Optional[str],
    ) -> List[Task]:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
        validate_dates(start_date, end_date)

        return self.__task_repository.get_by_period(
            start_date, end_date
        )

    async def get_tasks_by_date(
        self, date_str: Optional[str]
    ) -> List[Task]:
        if date_str is None:
            date_str = date.today().isoformat()
        target_date = parse_date(date_str)

        tasks = self.__task_repository.get_by_period(
            target_date, target_date
        )
        return tasks

    async def get_tasks_for_week(
        self, date_str: Optional[str]
    ) -> List[Task]:
        if date_str is None:
            date_str = date.today().isoformat()
        start_date = parse_date(date_str)
        end_date = start_date + timedelta(days=6)

        return await self.get_tasks_by_period(
            start_date.isoformat(), end_date.isoformat()
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
