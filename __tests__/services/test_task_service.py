from datetime import date, timedelta
from unittest import TestCase
from unittest.mock import create_autospec, patch

import pytest

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
