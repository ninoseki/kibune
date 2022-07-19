from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from kibune import crud, schemas
from kibune.api.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Emitter, status_code=201)
def create_emitter(
    payload: schemas.EmitterCreate, *, db: Session = Depends(get_db)
) -> schemas.Emitter:
    rule = crud.rule.get(db, id=payload.rule_id)
    if rule is None:
        raise HTTPException(status_code=400, detail=f"Rule:{payload.rule_id} not found")

    emitter = crud.emitter.create(db, obj_in=payload)
    return schemas.Emitter.from_orm(emitter)


@router.get("/{id}", response_model=schemas.Emitter)
def get_emitter(id: str, *, db: Session = Depends(get_db)) -> schemas.Emitter:
    emitter = crud.emitter.get(db, id)
    if emitter is None:
        raise HTTPException(status_code=404, detail="Not found")

    return schemas.Emitter.from_orm(emitter)


@router.get("/", response_model=list[schemas.Emitter])
def get_emitters(
    limit: int = 100,
    search_after: Optional[str] = None,
    *,
    db: Session = Depends(get_db),
) -> list[schemas.Emitter]:
    emitters = crud.emitter.get_multi(db, limit=limit, search_after=search_after)
    return [schemas.Emitter.from_orm(emitter) for emitter in emitters]


@router.delete("/{id}", status_code=204)
def remove_emitter(id: str, *, db: Session = Depends(get_db)):
    emitter = crud.emitter.get(db, id)
    if emitter is None:
        raise HTTPException(status_code=400, detail="Not found")

    crud.emitter.remove(db, id=id)

    return {}
