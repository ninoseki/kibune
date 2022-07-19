from collections.abc import Sequence
from typing import Any, Optional, Union

from arq.connections import RedisSettings
from arq.typing import StartupShutdown, WorkerCoroutine
from arq.worker import Function, func

from kibune.core import settings
from kibune.database.setup import setup

from . import constants, tasks
from .settings import get_redis_settings


async def startup(_: dict[Any, Any]) -> None:
    setup()


async def shutdown(_: dict[Any, Any]) -> None:
    pass


class ArqWorkerSettings:
    redis_settings: RedisSettings = get_redis_settings()

    max_jobs: int = settings.ARQ_MAX_JOBS

    on_startup: Optional[StartupShutdown] = startup
    on_shutdown: Optional[StartupShutdown] = shutdown

    functions: Sequence[Union[Function, WorkerCoroutine]] = [
        func(tasks.check_events, name=constants.CHECK_EVENTS),
        func(tasks.trigger_emitters, name=constants.TRIGGER_EMITTERS),
        func(tasks.emit_alert, name=constants.EMIT_ALERT),
    ]
