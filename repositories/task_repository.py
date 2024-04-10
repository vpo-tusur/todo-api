from datetime import date
from typing import List

from fastapi import Depends, status
from sqlalchemy.orm import Session

from configs.database import get_db_connection
from models.task_model import Task
from schemas.pydantic.task_schema import ServiceResponse


class TaskRepository:
    __db_context: Session

    def __init__(
        self,
        db_context: Session = Depends(get_db_connection),
    ) -> None:
        self.__db_context = db_context

    def create(self, task: Task) -> Task:
        self.__db_context.add(task)
        self.__db_context.commit()
        self.__db_context.refresh(task)
        return task

    def get_by_period(
        self, start_date: date, end_date: date
    ) -> List[Task]:
        return (
            self.__db_context.query(Task)
            .filter(
                Task.due_date >= start_date,
                Task.due_date <= end_date,
            )
            .all()
        )

    def update(self, task: Task) -> ServiceResponse:
        content = {
            "msg": f"Задача по идентификатору '{task.id}' не найдена"
        }

        db_tasks = self.__db_context.query(Task).all()
        for task_item in db_tasks:
            if task_item.id != task.id:
                continue
            task_item.title = task.title
            task_item.description = task.description
            task_item.due_date = task.due_date
            self.__db_context.commit()
            self.__db_context.refresh(task_item)
            content = {
                "id": str(task_item.id),
                "title": str(task_item.title),
                "description": str(task_item.description),
                "due_date": str(task_item.due_date),
            }
            return ServiceResponse(
                status=status.HTTP_200_OK, content=content
            )

        return ServiceResponse(
            status=status.HTTP_404_NOT_FOUND,
            content=content,
        )
