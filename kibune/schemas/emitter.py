from typing import Any, Literal

import jinja2
from pydantic import AnyHttpUrl, Field, validator

from kibune import models
from kibune.utils import get_j2_template

from .api_model import APIModel

DEFAULT_TEMPLATE = """{
"event": {{ event|tojson }},
"rule": {{ rule|tojson }}
}"""


class Emitter(APIModel, models.Emitter):
    pass


class EmitterCreate(APIModel):
    rule_id: str = Field(...)
    url: AnyHttpUrl = Field(...)
    method: Literal["POST", "PUT"] = Field(default="POST")
    headers: dict[str, Any] = Field(default={"content-type": "application/json"})

    template: str = Field(default=DEFAULT_TEMPLATE)

    @validator("template")
    def validate_template(cls, v: str):
        try:
            get_j2_template(v)
        except jinja2.TemplateError:
            raise ValueError("Invalid Jinja2 template format")

        return v


class EmitterUpdate(EmitterCreate):
    pass
