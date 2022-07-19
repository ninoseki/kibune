from typing import Any

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from kibune import crud, models, schemas


class LogFactory:
    @staticmethod
    def from_event_and_rule(db: Session, *, rule: models.Rule, event: dict[Any, Any]):
        try:
            return crud.log.create(
                db, obj_in=schemas.LogCreate(rule_id=rule.id, event=event)
            )
        except SQLAlchemyError as e:
            logger.exception(e)
            db.rollback()

        return None
