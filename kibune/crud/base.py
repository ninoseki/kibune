from collections.abc import Generator
from typing import Any, Generic, Optional, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlmodel import Session

from kibune.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLModel model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, limit: int = 100, search_after: Optional[str] = None
    ) -> list[ModelType]:
        query = select(self.model)

        if search_after is not None:
            query = query.filter(self.model.id > search_after)

        query = query.order_by(desc(self.model.created_at)).limit(limit)
        return [row[0] for row in db.exec(query)]

    def get_multi_with_pagination(
        self, db: Session, *, limit: int = 100
    ) -> Generator[list[ModelType], None, None]:
        search_after: Optional[str] = None
        has_more = True

        while has_more:
            objs = self.get_multi(db, limit=limit, search_after=search_after)

            if len(objs) != 0:
                yield objs

            if len(objs) < limit:
                has_more = False

    def get_all(self, db: Session) -> list[ModelType]:
        query = select(self.model)

        query = query.order_by(desc(self.model.created_at))
        return [row[0] for row in db.exec(query)]

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj, by_alias=False)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: str) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
