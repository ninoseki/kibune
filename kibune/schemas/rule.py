from typing import Any

from dict_hash import sha256
from loguru import logger
from pydantic import Field, validator

from kibune import models
from kibune.pysigma.validator import run_sigma_validator

from .api_model import APIModel
from .utils import is_yaml, parse_yaml


class Rule(APIModel, models.Rule):
    pass


class RuleCreate(APIModel):
    yaml: str = Field(...)

    @validator("yaml")
    def validate_by_pysigma(cls, v: str):
        if not is_yaml(v):
            raise ValueError("Invalid YAML format")

        validator = run_sigma_validator(v)
        if len(validator.file_errors) > 0:
            for error in validator.file_errors:
                logger.error(error)

            raise ValueError(
                "Invalid Sigma format. See the application logs for the details."
            )

        return v

    @property
    def parsed(self) -> dict[Any, Any]:
        return parse_yaml(self.yaml)

    @property
    def sha256(self) -> str:
        return sha256(self.parsed)


class RuleUpdate(RuleCreate):
    pass
