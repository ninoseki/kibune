from fastapi import APIRouter

from .endpoints import emitters, events, logs, rules

api_router = APIRouter()

api_router.include_router(events.router, prefix="/events", tags=["event"])
api_router.include_router(logs.router, prefix="/logs", tags=["log"])
api_router.include_router(rules.router, prefix="/rules", tags=["rule"])
api_router.include_router(emitters.router, prefix="/emitters", tags=["emitter"])
