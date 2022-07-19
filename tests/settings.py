from starlette.config import Config

from kibune.core.datastructures import DatabaseURL

config = Config(".env")

SQLALCHEMY_DATABASE_URL: DatabaseURL = config(
    "TESTING_SQLALCHEMY_DATABASE_URL", cast=DatabaseURL, default="sqlite:///:memory:"
)
