import json

import pytest
from pytest_httpserver import HTTPServer

from kibune import models, schemas
from kibune.services.emitter import Emitter


@pytest.mark.asyncio
async def test_emitter(httpserver: HTTPServer):
    httpserver.expect_request("/foo").respond_with_json({"foo": "bar"})

    fake_rule = models.Rule(id="dummy", yaml="dummy", sha256="dummy", parsed={})

    create_payload = schemas.EmitterCreate(
        url=httpserver.url_for("/foo"), rule_id="dummy"
    )

    emitter = Emitter(
        url=create_payload.url,
        method=create_payload.method,
        headers=create_payload.headers,
        template=create_payload.template,
    )
    await emitter.emit(event={"foo": "bar"}, rule=fake_rule)

    assert len(httpserver.log) == 1

    last_request, _ = httpserver.log[0]

    assert last_request.method == "POST"
    assert last_request.headers.get("content-type") == "application/json"

    data = json.loads(last_request.data.decode())
    assert data.get("event") == {"foo": "bar"}
