from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg2(),
    echo=True,
    pool_size=5,
    max_overflow=10,
)


session_maker = sessionmaker(bind=engine, expire_on_commit=False)


def connection(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        with session_maker() as session:
            try:
                return method(*args, session=session, **kwargs)
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()  # Закрываем сессию

    return wrapper
