from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from arq import ArqRedis, create_pool

from kibune.arq.settings import get_redis_settings
from kibune.database.session import get_db as _get_db


@asynccontextmanager
async def get_arq_redis_with_context() -> AsyncGenerator[ArqRedis, None]:
    try:
        redis = await create_pool(settings_=get_redis_settings())
        yield redis
    finally:
        redis.close()
        await redis.wait_closed()


async def get_arq_redis():
    async with get_arq_redis_with_context() as arq_redis:
        yield arq_redis


def get_db():
    with _get_db() as db:
        yield db
