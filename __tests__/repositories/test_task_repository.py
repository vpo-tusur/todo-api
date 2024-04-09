from datetime import date
from unittest import TestCase
from unittest.mock import create_autospec, patch

from sqlalchemy.orm import Session

from models import Task
from repositories.task_repository import TaskRepository


class TestTaskRepository(TestCase):
    __session: Session
    __task_repository: TaskRepository

    def setUp(self):
        super().setUp()
        self.__session = create_autospec(Session)
        self.__task_repository = TaskRepository(
            self.__session
        )

    @patch("models.task_model.Task", autospec=True)
    def test_create(self, Task):
        # arrange
        task = Task(title="title")

        # act
        self.__task_repository.create(task)

        # assert - должен вызваться метод add в Session с переданным task
        self.__session.add.assert_called_once_with(task)

    @patch("models.task_model.Task", autospec=True)
    def test_get_by_period(self, mock_task):
        # arrange
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 31)
        tasks = [
            mock_task(
                id=1,
                title="Задача 1",
                description="Описание задачи 1",
                due_date=date(2023, 1, 15),
            ),
            mock_task(
                id=2,
                title="Задача 2",
                description="Описание задачи 2",
                due_date=date(2023, 1, 20),
            ),
        ]
        self.__session.query.return_value.filter.return_value.all.return_value = (
            tasks
        )

        # act
        result = self.__task_repository.get_by_period(
            start_date, end_date
        )

        # assert
        self.__session.query.assert_called_once_with(Task)
        self.assertEqual(result, tasks)
