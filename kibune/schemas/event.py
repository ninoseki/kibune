from typing import Any

from .api_model import APIModel


class EventCreate(APIModel):
    event: dict[Any, Any]


class EventsCreate(APIModel):
    events: list[dict[Any, Any]]
