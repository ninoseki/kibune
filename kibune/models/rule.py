from typing import TYPE_CHECKING, Any

from sqlalchemy.orm import RelationshipProperty
from sqlmodel import JSON, Column, Field, Relationship, String, Text

from .base import Base
from .utils import get_ulid

if TYPE_CHECKING:
    from .emitter import Emitter
    from .log import Log


class Rule(Base, table=True):
    __tablename__ = "rules"

    id: str = Field(
        sa_column=Column(String(26), primary_key=True), default_factory=get_ulid
    )
    yaml: str = Field(sa_column=Column(Text, nullable=False))
    parsed: dict[Any, Any] = Field(sa_column=Column(JSON, nullable=False))
    sha256: str = Field(sa_column=Column(String(64), nullable=False, unique=True))

    logs: list["Log"] = Relationship(
        sa_relationship=RelationshipProperty(
            "Log",
            back_populates="rule",
            uselist=True,
            cascade="all,delete",
        )
    )
    emitters: list["Emitter"] = Relationship(
        sa_relationship=RelationshipProperty(
            "Emitter",
            back_populates="rule",
            uselist=True,
            cascade="all,delete",
        )
    )
