import re
from typing import Any, Callable, Optional, Union

from pydantic import Field

from .base_model import BaseModel

Query = Optional[Union[str, re.Pattern, Any]]
DetectionMap = list[tuple[str, tuple[list[Query], list[str]]]]
Condition = Callable[["Rule", dict[Any, Any]], Any]


class DetectionField(BaseModel):
    list_search: list[Query] = Field(default_factory=list)
    map_search: list[DetectionMap] = Field(default_factory=list)


class Detection(BaseModel):
    detection: dict[str, DetectionField] = Field(...)
    condition: Optional[Condition] = Field(default=None)


class Rule(BaseModel):
    title: str = Field(...)
    detection: Detection = Field(...)

    author: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    id: Optional[str] = Field(default=None)
    level: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)

    references: Optional[list[str]] = Field(default=None)
    tags: Optional[list[str]] = Field(default=None)

    related: Optional[dict[str, str]] = Field(default=None)
    logsource: Optional[dict[str, str]] = Field(default=None)

    def get_condition(self) -> Optional[Condition]:
        return self.detection.condition

    def get_all_searches(self) -> dict[str, DetectionField]:
        return self.detection.detection

    def get_search_fields(self, search_id) -> Optional[DetectionField]:
        return self.detection.detection.get(search_id)


class Alert(BaseModel):
    event: dict[Any, Any] = Field(...)
    rule: Rule = Field(...)
