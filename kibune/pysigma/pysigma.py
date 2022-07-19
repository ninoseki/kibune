import copy
from typing import Any, Callable, Optional

from . import parser, rules, schemas

Callback = Optional[Callable[[schemas.Alert, dict[Any, Any]], None]]


class PySigma:
    def __init__(self, rule: str, *, callback: Callback = None):
        self.rule = rules.load_rule(rule)
        self.hits: dict[str, list[dict[Any, Any]]] = {}
        self.callback = callback or self.default_callback

    def check_events(self, events: list[dict[Any, Any]]):
        all_alerts: list[schemas.Alert] = []
        for event in events:
            alerts = parser.check_event(event, rule=self.rule)

            for alert in alerts:
                self.default_callback(alert, event)
                all_alerts.append(alert)

        return all_alerts

    def default_callback(self, alert: schemas.Alert, event: dict[Any, Any]) -> None:
        id = alert.rule.id or alert.rule.title
        copied_event = copy.deepcopy(event)

        if id not in self.hits:
            self.hits[id] = [copied_event]
        else:
            self.hits[id].append(copied_event)

    def has_hits(self) -> bool:
        return len(self.hits.keys()) > 0
