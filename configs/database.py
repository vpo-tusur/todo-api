from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import configs.environment as environment
import configs.settings as settings

engine = create_engine(
    settings.db_conn_string,
    future=True,
    echo=environment.debug,
)

session_local = sessionmaker(autoflush=False, bind=engine)


def get_db_connection():
    """
    Получить сессию БД.
    """
    db = scoped_session(session_local)
    try:
        yield db
    finally:
        db.close()
