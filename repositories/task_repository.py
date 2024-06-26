from datetime import date
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from configs.database import get_db_connection
from models.task_model import Task


class TaskNotFoundException(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        self.message = f"Задача по идентификатору '{task_id}' не найдена"
        super().__init__(self.message)


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

    def delete(self, task_id: int) -> Task:
        task = self.__db_context.query(Task).get(task_id)

        if task is None:
            raise TaskNotFoundException(task_id)

        self.__db_context.delete(task)
        self.__db_context.commit()
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
        db_task = self.__db_context.query(Task).get(task.id)

        if db_task is None:
            raise TaskNotFoundException(task.id)

        db_task.title = task.title
        db_task.description = task.description
        db_task.due_date = task.due_date
        self.__db_context.commit()
        self.__db_context.refresh(db_task)

        return db_task
