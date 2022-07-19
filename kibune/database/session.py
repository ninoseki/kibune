from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
from sqlmodel import create_engine as _create_engine

from kibune.core import settings
from kibune.core.datastructures import DatabaseURL


def is_sqlite(database_url: DatabaseURL) -> bool:
    return database_url.scheme == "sqlite"


def create_engine(database_url: DatabaseURL = settings.SQLALCHEMY_DATABASE_URL):
    connect_args: dict = {}

    if is_sqlite(database_url):
        connect_args = {"check_same_thread": False}

    return _create_engine(
        str(database_url),
        pool_pre_ping=True,
        connect_args=connect_args,
        echo=settings.DEBUG,
    )


engine = create_engine()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    db = Session(engine)

    try:
        yield db
    except SQLAlchemyError:
        db.rollback()
    finally:
        db.close()
