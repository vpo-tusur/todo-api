from sqlalchemy import (
    Column,
    Date,
    Integer,
    PrimaryKeyConstraint,
    String,
)

from models.base_model import BaseModel


class Task(BaseModel):
    __tablename__ = "task"

    id = Column(Integer)
    title = Column(String(256), nullable=False)
    description = Column(String(256))
    due_date = Column(Date, nullable=False)

    PrimaryKeyConstraint(id)
