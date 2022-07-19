from collections.abc import Generator
from typing import Optional

from sqlalchemy import select
from sqlmodel import Session, desc

from kibune import models, schemas

from .base import CRUDBase


class CRUDEmitter(
    CRUDBase[models.Emitter, schemas.EmitterCreate, schemas.EmitterUpdate]
):
    def get_multi(
        self,
        db: Session,
        *,
        limit: int = 100,
        search_after: Optional[str] = None,
        rule_id: Optional[str] = None
    ) -> list[models.Emitter]:
        query = select(self.model)

        if search_after is not None:
            query = query.filter(self.model.id > search_after)

        if rule_id is not None:
            query = query.filter(self.model.rule_id == rule_id)

        query = query.order_by(desc(self.model.created_at)).limit(limit)
        return [row[0] for row in db.exec(query)]

    def get_multi_with_pagination(
        self, db: Session, *, limit: int = 100, rule_id: Optional[str] = None
    ) -> Generator[list[models.Emitter], None, None]:
        search_after: Optional[str] = None
        has_more = True

        while has_more:
            objs = self.get_multi(
                db, limit=limit, search_after=search_after, rule_id=rule_id
            )

            if len(objs) != 0:
                yield objs

            if len(objs) < limit:
                has_more = False

    def get_all(
        self, db: Session, *, rule_id: Optional[str] = None
    ) -> list[models.Emitter]:
        query = select(self.model)

        if rule_id is not None:
            query = query.filter(self.model.rule_id == rule_id)

        query = query.order_by(desc(self.model.created_at))
        return [row[0] for row in db.exec(query)]


emitter = CRUDEmitter(models.Emitter)
