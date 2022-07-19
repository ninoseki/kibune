from fastapi.testclient import TestClient


def test_emitter_with_invalid_rule(client: TestClient):
    payload = {
        "method": "POST",
        "url": "http://example.com",
        "headers": {"foo": "bar"},
        "ruleId": "404",
    }
    res = client.post("/api/v1/emitters/", json=payload)
    assert res.status_code == 400
