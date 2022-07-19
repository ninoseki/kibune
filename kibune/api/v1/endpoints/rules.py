from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from kibune import crud, schemas
from kibune.api.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Rule, status_code=201)
def create_rule(
    payload: schemas.RuleCreate, *, db: Session = Depends(get_db)
) -> schemas.Rule:
    try:
        rule = crud.rule.create(db, obj_in=payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="There is already the same rule registered"
        )

    return schemas.Rule.from_orm(rule)


@router.get("/{id}", response_model=schemas.Rule)
def get_rule(id: str, *, db: Session = Depends(get_db)) -> schemas.Rule:
    rule = crud.rule.get(db, id)
    if rule is None:
        raise HTTPException(status_code=404, detail="Not found")

    return schemas.Rule.from_orm(rule)


@router.get("/", response_model=list[schemas.Rule])
def get_rules(
    limit: int = 100,
    search_after: Optional[str] = None,
    *,
    db: Session = Depends(get_db)
) -> list[schemas.Rule]:
    rules = crud.rule.get_multi(db, limit=limit, search_after=search_after)
    return [schemas.Rule.from_orm(rule) for rule in rules]


@router.delete("/{id}", status_code=204)
def remove_rule(id: str, *, db: Session = Depends(get_db)):
    rule = crud.rule.get(db, id)
    if rule is None:
        raise HTTPException(status_code=400, detail="Not found")

    crud.rule.remove(db, id=id)

    return {}
