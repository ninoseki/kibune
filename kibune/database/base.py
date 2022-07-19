from datetime import datetime

from sqlmodel.main import SQLModelMetaclass


class Base(SQLModelMetaclass):
    id: str
    created_at: datetime
