from contextlib import contextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from kibune import models
from kibune.api.dependencies import get_db
from kibune.database.session import create_engine
from kibune.main import create_app

from . import settings


@contextmanager
def get_db_with_context():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    SQLModel.metadata.create_all(bind=engine)

    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def db():
    with get_db_with_context() as db:
        yield db


def override_get_db():
    with get_db_with_context() as db:
        yield db


@pytest.fixture
def app():
    app = create_app(add_event_handlers=False)

    app.dependency_overrides[get_db] = override_get_db

    yield app


@pytest.fixture
def client(app: FastAPI):
    with TestClient(app=app) as client:
        yield client


@pytest.fixture
def reset_rules(db: Session):
    with db.begin():
        db.query(models.Rule).delete()


@pytest.fixture
def reset_logs(db: Session):
    with db.begin():
        db.query(models.Log).delete()


@pytest.fixture
def reset_emitters(db: Session):
    with db.begin():
        db.query(models.Emitter).delete()
