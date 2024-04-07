from unittest import TestCase
from unittest.mock import create_autospec, patch

from sqlalchemy.orm import Session

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
