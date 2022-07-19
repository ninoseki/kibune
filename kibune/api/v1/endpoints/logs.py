from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from kibune import crud, schemas
from kibune.api.dependencies import get_db

router = APIRouter()


@router.get("/{id}", response_model=schemas.Log)
def get_log(id: str, *, db: Session = Depends(get_db)) -> schemas.Log:
    log = crud.log.get(db, id)
    if log is None:
        raise HTTPException(status_code=400, detail="Not found")

    return schemas.Log.from_orm(log)


@router.get("/", response_model=list[schemas.Log])
def get_logs(
    limit: int = 100,
    search_after: Optional[str] = None,
    *,
    db: Session = Depends(get_db)
) -> list[schemas.Log]:
    logs = crud.log.get_multi(db, limit=limit, search_after=search_after)
    return [schemas.Log.from_orm(log) for log in logs]


@router.delete("/{id}", status_code=204)
def remove_log(id: str, *, db: Session = Depends(get_db)):
    log = crud.log.get(db, id)
    if log is None:
        raise HTTPException(status_code=400, detail="Not found")

    crud.log.remove(db, id=id)

    return {}
