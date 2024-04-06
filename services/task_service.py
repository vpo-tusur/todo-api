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
