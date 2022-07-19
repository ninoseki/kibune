from collections.abc import Coroutine
from typing import Any, Callable

from fastapi import FastAPI

from kibune.database.setup import setup


def create_start_app_handler(
    _: FastAPI,
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def start_app() -> None:
        setup()

    return start_app


def create_stop_app_handler(
    _: FastAPI,
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def stop_app() -> None:
        pass

    return stop_app
