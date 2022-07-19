from typing import TYPE_CHECKING, Any

from sqlalchemy.orm import RelationshipProperty
from sqlmodel import JSON, Column, Field, ForeignKey, Relationship, String

from .base import Base
from .utils import get_ulid

if TYPE_CHECKING:
    from .rule import Rule


class Log(Base, table=True):
    __tablename__ = "logs"

    id: str = Field(
        sa_column=Column(String(26), primary_key=True), default_factory=get_ulid
    )
    event: dict[Any, Any] = Field(sa_column=Column(JSON, nullable=False))

    rule: "Rule" = Relationship(
        sa_relationship=RelationshipProperty(
            "Rule", back_populates="logs", lazy="joined", uselist=False
        )
    )
    rule_id: str = Field(
        sa_column=Column(String(26), ForeignKey("rules.id"), nullable=False)
    )
