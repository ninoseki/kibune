from typing import cast

from arq.connections import ArqRedis
from fastapi import APIRouter, Depends, Query

from kibune import models, schemas
from kibune.api.dependencies import get_arq_redis
from kibune.arq import constants

router = APIRouter()


@router.post(
    "/",
    description="Returns an empty array if background is set as true",
    response_model=list[schemas.Log],
)
async def feed_event(
    payload: schemas.EventCreate,
    background: bool = Query(
        default=False, description="Whether to run Sigma matching in background or not"
    ),
    *,
    arq_redis: ArqRedis = Depends(get_arq_redis)
) -> list[schemas.Log]:
    job = await arq_redis.enqueue_job(constants.CHECK_EVENTS, events=[payload.event])

    if background is True:
        return []

    logs = cast(list[models.Log], await job.result())
    return [schemas.Log.from_orm(log) for log in logs]


@router.post("/bulk")
async def feed_events(
    payload: schemas.EventsCreate, *, arq_redis: ArqRedis = Depends(get_arq_redis)
):
    await arq_redis.enqueue_job(constants.CHECK_EVENTS, events=payload.events)
    return {}
