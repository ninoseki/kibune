from sqlmodel import Session

from kibune import models, schemas

from .base import CRUDBase


class CRUDRule(CRUDBase[models.Rule, schemas.RuleCreate, schemas.RuleUpdate]):
    def create(self, db: Session, *, obj_in: schemas.RuleCreate) -> models.Rule:
        db_obj = models.Rule(
            yaml=obj_in.yaml, parsed=obj_in.parsed, sha256=obj_in.sha256
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_sha256(self, db: Session, sha256: str):
        return db.query(self.model).filter(self.model.sha256 == sha256).first()


rule = CRUDRule(models.Rule)
