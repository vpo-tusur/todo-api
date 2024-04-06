from fastapi import Depends
from sqlalchemy.orm import Session

from configs.database import get_db_connection
from models.task_model import Task


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