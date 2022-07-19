from typing import Any, Optional, cast

from arq.connections import ArqRedis

from kibune import crud, models, services
from kibune.database.session import get_db
from kibune.factories import LogFactory
from kibune.pysigma import PySigma

from . import constants


async def emit_alert(
    ctx: dict[Any, Any],
    *,
    emitter: models.Emitter,
    event: dict[Any, Any],
    rule: models.Rule,
) -> None:
    service = services.Emitter(
        url=emitter.url,
        headers=emitter.headers,
        method=emitter.method,
        template=emitter.template,
    )
    from loguru import logger

    logger.info(emitter.template)
    await service.emit(event=event, rule=rule)
    return None


async def trigger_emitters(
    ctx: dict[Any, Any], *, event: dict[Any, Any], rule: models.Rule
) -> None:
    redis = cast(ArqRedis, ctx.get("redis"))

    with get_db() as db:
        for emitters in crud.emitter.get_multi_with_pagination(db, rule_id=rule.id):
            for emitter in emitters:
                await redis.enqueue_job(
                    constants.EMIT_ALERT,
                    emitter=emitter,
                    event=event,
                    rule=rule,
                )

    return None


async def check_events(
    ctx: dict[Any, Any], *, events: list[dict[Any, Any]]
) -> list[models.Log]:
    redis = cast(ArqRedis, ctx.get("redis"))

    logs: list[Optional[models.Log]] = []
    with get_db() as db:
        for rules in crud.rule.get_multi_with_pagination(db):
            for rule in rules:
                sigma = PySigma(rule.yaml)

                alerts = sigma.check_events(events)
                if len(alerts) == 0:
                    continue

                for alert in alerts:
                    log = LogFactory.from_event_and_rule(
                        db, rule=rule, event=alert.event
                    )
                    logs.append(log)

                    await redis.enqueue_job(
                        constants.TRIGGER_EMITTERS, event=alert.event, rule=rule
                    )

    return [log for log in logs if log is not None]
