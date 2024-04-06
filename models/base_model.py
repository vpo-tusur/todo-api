from sqlalchemy.orm import declarative_base

from configs.database import engine

# Базовая модель сущности предметной области.
BaseModel = declarative_base()
