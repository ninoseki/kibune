from typing import Any

from pydantic import Field

from .api_model import APIModel
from .rule import Rule


class Log(APIModel):
    id: str = Field(...)
    rule: Rule = Field(...)
    event: dict[Any, Any] = Field(...)


class LogCreate(APIModel):
    rule_id: str = Field(...)
    event: dict[Any, Any] = Field(...)


class LogUpdate(LogCreate):
    pass
