from datetime import date
from typing import Optional

from typing_extensions import Annotated

from pydantic import (
    BaseModel,
    Field,
    StringConstraints,
    field_validator,
)


class TaskPostRequestSchema(BaseModel):
    title: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, min_length=1
        ),
    ] = Field(description="Название задачи")
    description: Annotated[
        Optional[str],
        StringConstraints(strip_whitespace=True),
    ] = Field(description="Описание задачи", default=None)
    due_date: Optional[date] = Field(
        description="День задачи", default=date.today()
    )

    @field_validator("due_date")
    @classmethod
    def validate_dob(cls, v: date) -> date:
        if v < date.today():
            raise ValueError(
                f"Date should be greater or equal than {date.today()}"
            )
        return v


class TaskSchema(TaskPostRequestSchema):
    id: int
