import sys

from starlette.config import Config

from .datastructures import DatabaseURL

config = Config(".env")

PROJECT_NAME: str = config("PROJECT_NAME", default="kibune")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING: bool = config("TESTING", cast=bool, default=False)

LOG_FILE = config("LOG_FILE", default=sys.stderr)
LOG_LEVEL: str = config("LOG_LEVEL", cast=str, default="DEBUG")
LOG_BACKTRACE: bool = config("LOG_BACKTRACE", cast=bool, default=True)

# SQL Model (SQLAlchemy) settings
SQLALCHEMY_DATABASE_URL: DatabaseURL = config(
    "SQLALCHEMY_DATABASE_URL", cast=DatabaseURL, default="sqlite:///:memory:"
)

# Redis & ARQ settings
REDIS_URL: DatabaseURL = config(
    "REDIS_URL",
    cast=DatabaseURL,
    default="redis://localhost:6379",
)

ARQ_MAX_JOBS: int = config("ARQ_MAX_JOBS", cast=int, default=50)
ARQ_REDIS_CONN_TIMEOUT: int = config("ARQ_REDIS_CONN_TIMEOUT", cast=int, default=10)
ARQ_REDIS_CONN_RETRIES: int = config("ARQ_REDIS_CONN_RETRIES", cast=int, default=5)
ARQ_REDIS_CONN_RETRY_DELAY: int = config(
    "ARQ_REDIS_CONN_RETRY_DELAY", cast=int, default=1
)

# In-memory LRU cache settings
SIGMA_RULE_CACHE_SIZE: int = config("SIGMA_RULE_CACHE_SIZE", cast=int, default=128)
