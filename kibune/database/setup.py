from kibune import models  # noqa: F401

from sqlmodel import SQLModel
from .session import engine


def setup():
    SQLModel.metadata.create_all(engine)
