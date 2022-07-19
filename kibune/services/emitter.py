from typing import Any

import httpx

from kibune import models
from kibune.schemas import Rule
from kibune.utils import get_j2_template


class Emitter:
    def __init__(
        self, *, url: str, headers: dict[str, Any], method: str, template: str
    ) -> None:
        self.url = url
        self.headers = headers
        self.method = method
        self.template = template

    async def emit(self, *, event: dict[Any, Any], rule: models.Rule):
        # convert rule as a camelCase key dict
        # also convert datetime object as a str
        rule_model = Rule.from_orm(rule)
        rule_dict = rule_model.dict(by_alias=True)
        if "createdAt" in rule_dict:
            rule_dict["createdAt"] = rule.created_at.isoformat()

        j2_template = get_j2_template(self.template)
        rendered = j2_template.render(event=event, rule=rule_dict)

        request = httpx.Request(
            url=self.url, method=self.method, headers=self.headers, data=rendered
        )
        async with httpx.AsyncClient() as client:
            res = await client.send(request)
            res.raise_for_status()
