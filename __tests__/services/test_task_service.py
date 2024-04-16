from datetime import date, timedelta
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import create_autospec, patch

import pytest

from models import Task
from pydantic import ValidationError
from repositories.task_repository import TaskRepository
from schemas.pydantic.task_schema import (
    TaskPostRequestSchema,
)
from services.task_service import TaskService


class TestTaskService(TestCase):
    __task_repository: TaskRepository
    __task_service: TaskService

    def setUp(self):
        super().setUp()
        self.__task_repository = create_autospec(
            TaskRepository
        )
        self.__task_service = TaskService(
            self.__task_repository
        )

    @patch(
        "schemas.pydantic.task_schema.TaskPostRequestSchema",
        autospec=True,
    )
    def test_create(self, TaskPostRequestSchema):
        # arrange
        task = TaskPostRequestSchema()
        task.title = "title"
        task.description = "description"
        task.due_date = date.today()

        # act
        self.__task_service.create(task)

        # assert - должно инициализироваться создание task репозиторием
        self.__task_repository.create.assert_called_once()

    @patch(
        "schemas.pydantic.task_schema.TaskPostRequestSchema",
        autospec=True,
    )
    def test_update(self, TaskPostRequestSchema):
        # arrange
        task = TaskPostRequestSchema()
        task.title = "title"
        task.description = "description"
        task.due_date = date.today()

        # act
        self.__task_service.update(1, task)

        # assert - должно инициализироваться создание task репозиторием
        self.__task_repository.update.assert_called_once()

    def test_update__no_title__should_validation_error(
        self,
    ):
        # act
        with pytest.raises(ValidationError):
            TaskPostRequestSchema()

    def test_update__empty_title__should_validation_error(
        self,
    ):
        # act
        with pytest.raises(ValidationError):
            TaskPostRequestSchema(title="")

    def test_update__empty_description__should_validation_error(
        self,
    ):
        # act
        with pytest.raises(ValidationError):
            TaskPostRequestSchema(description="")

    def test_update__empty_date__should_validation_error(
        self,
    ):
        # act
        with pytest.raises(ValidationError):
            TaskPostRequestSchema(due_date="")

    def test_create__no_title__should_validation_error(
        self,
    ):
        # act
        with pytest.raises(ValidationError):
            TaskPostRequestSchema()

    def test_create__empty_title__should_validation_error(
        self,
    ):
        # act
        with pytest.raises(ValidationError):
            TaskPostRequestSchema(title="")

    def test_create__title_typo__should_validation_error(
        self,
    ):
        # act, assert
        with pytest.raises(ValidationError):
            TaskPostRequestSchema(title=123)

    def test_create__no_due_date__should_today(self):
        # arrange
        task = TaskPostRequestSchema(title="title")

        # act
        self.__task_service.create(task)

        # assert - due_date = today по умолчанию
        assert task.due_date == date.today()

    def test_create__due_date_yesterday__should_value_error(
        self,
    ):
        # arrange
        yesterday = date.today() - timedelta(days=1)

        # act, assert
        with pytest.raises(ValueError):
            TaskPostRequestSchema(
                title="title", due_date=yesterday
            )

    def test_create__due_date_typo__should_value_error(
        self,
    ):
        # act, assert
        with pytest.raises(ValidationError):
            TaskPostRequestSchema(
                title="title", due_date=123
            )

    def test_create__no_description__should_none_description(
        self,
    ):
        # arrange
        task = TaskPostRequestSchema(title="title")

        # act
        self.__task_service.create(task)

        # assert
        assert task.description == None

    def test_create__empty_description__should_empty_description(
        self,
    ):
        # arrange
        task = TaskPostRequestSchema(
            title="title", description=""
        )

        # act
        self.__task_service.create(task)

        # assert
        assert task.description == ""

    def test_create__description_typo__should_value_error(
        self,
    ):
        # act, assert
        with pytest.raises(ValidationError):
            TaskPostRequestSchema(
                title="title", description=123
            )


class TestTaskGetService(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.task_repository = create_autospec(
            TaskRepository, instance=True
        )
        self.task_service = TaskService(
            task_repository=self.task_repository
        )

    async def test_get_tasks_by_period_valid(self):
        # arrange
        start_date = "2020-01-01"
        end_date = "2020-01-31"
        tasks = [
            Task(
                id=1,
                title="Task 1",
                description="Description 1",
                due_date=date(2020, 1, 15),
            ),
            Task(
                id=2,
                title="Task 2",
                description="Description 2",
                due_date=date(2020, 1, 20),
            ),
        ]
        self.task_repository.get_by_period.return_value = (
            tasks
        )

        # act
        result = (
            await self.task_service.get_tasks_by_period(
                start_date, end_date
            )
        )

        # assert
        self.task_repository.get_by_period.assert_called_once_with(
            date(2020, 1, 1), date(2020, 1, 31)
        )
        self.assertEqual(result, tasks)

    async def test_get_tasks_by_period_incorrect_format(
        self,
    ):
        # arrange
        start_date = "не дата"  # Некорректный формат
        end_date = "2020-01-31"

        # act & assert
        with self.assertRaises(ValueError):
            await self.task_service.get_tasks_by_period(
                start_date, end_date
            )

    async def test_get_tasks_by_period_start_date_greater_than_end_date(
        self,
    ):
        # arrange
        start_date = "2020-02-01"
        end_date = "2020-01-01"

        # act & assert
        with self.assertRaises(ValueError):
            await self.task_service.get_tasks_by_period(
                start_date, end_date
            )

    async def test_get_tasks_by_period_empty_range(self):
        # arrange
        start_date = "2020-01-01"
        end_date = (
            "2020-01-01"  # Та же дата, что и start_date
        )

        self.task_repository.get_by_period.return_value = []

        # act
        result = (
            await self.task_service.get_tasks_by_period(
                start_date, end_date
            )
        )

        # assert
        self.task_repository.get_by_period.assert_called_once_with(
            date(2020, 1, 1), date(2020, 1, 1)
        )
        self.assertEqual(result, [])

    async def test_get_tasks_by_period_invalid_date(self):
        # arrange
        start_date = "2020-02-30"  # Невалидная дата
        end_date = "2020-03-01"

        # act & assert
        with self.assertRaises(ValueError):
            await self.task_service.get_tasks_by_period(
                start_date, end_date
            )

    async def test_get_tasks_by_period_no_tasks_found(self):
        # arrange
        start_date = "1984-01-01"
        end_date = "1984-01-31"
        self.task_repository.get_by_period.return_value = []

        # act
        result = (
            await self.task_service.get_tasks_by_period(
                start_date, end_date
            )
        )

        # assert
        self.task_repository.get_by_period.assert_called_once_with(
            date(1984, 1, 1), date(1984, 1, 31)
        )
        self.assertEqual(result, [])

    async def test_get_tasks_by_date_valid(self):
        # arrange
        test_date = date.today().isoformat()
        tasks = [
            Task(
                id=1,
                title="Task 1",
                description="Description 1",
                due_date=date.today(),
            ),
            Task(
                id=2,
                title="Task 2",
                description="Description 2",
                due_date=date.today(),
            ),
        ]
        self.task_repository.get_by_period.return_value = (
            tasks
        )

        # act
        result = await self.task_service.get_tasks_by_date(
            test_date
        )

        # assert
        self.task_repository.get_by_period.assert_called_once_with(
            date.today(), date.today()
        )
        self.assertEqual(result, tasks)

    async def test_get_tasks_by_date_incorrect_format(self):
        # arrange
        incorrect_date = "не дата"  # Некорректный формат

        # act & assert
        with self.assertRaises(ValueError):
            await self.task_service.get_tasks_by_date(
                incorrect_date
            )

    async def test_get_tasks_by_date_no_date_provided_uses_today(
        self,
    ):
        # arrange
        tasks = [
            Task(
                id=1,
                title="Task Today 1",
                description="Description Today 1",
                due_date=date.today(),
            ),
        ]
        self.task_repository.get_by_period.return_value = (
            tasks
        )

        # act
        result = await self.task_service.get_tasks_by_date(
            None
        )

        # assert
        self.task_repository.get_by_period.assert_called_once_with(
            date.today(), date.today()
        )
        self.assertEqual(result, tasks)

    async def test_get_tasks_by_date_no_tasks_found(self):
        # arrange
        test_date = "1984-01-01"
        self.task_repository.get_by_period.return_value = []

        # act
        result = await self.task_service.get_tasks_by_date(
            test_date
        )

        # assert
        self.task_repository.get_by_period.assert_called_once_with(
            date(1984, 1, 1), date(1984, 1, 1)
        )
        self.assertEqual(result, [])
