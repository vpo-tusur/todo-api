from datetime import date
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from configs.database import get_db_connection
from models.task_model import Task


class TaskNotFoundException(Exception):
    pass


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

    def update(self, task: Task) -> Task:
        db_tasks = (
            self.__db_context.query(Task)
            .filter(Task.id == task.id)
            .all()
        )

        if len(db_tasks) < 1:
            raise TaskNotFoundException(
                f"Задача по идентификатору '{task.id}' не найдена"
            )

        db_task = db_tasks[0]
        db_task.title = task.title
        db_task.description = task.description
        db_task.due_date = task.due_date
        self.__db_context.commit()
        self.__db_context.refresh(db_task)

        return db_task
