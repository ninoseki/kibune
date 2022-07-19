from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field, SQLModel


class CreatedAtMixin(BaseModel):
    created_at: datetime = Field(
        sa_column=Column(DateTime), default_factory=datetime.utcnow
    )


class Base(CreatedAtMixin, SQLModel):
    id: str
