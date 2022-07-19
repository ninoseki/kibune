from typing import cast

from fastapi.testclient import TestClient


def test_rule(client: TestClient, reset_rules):
    with open("tests/fixtures/win_system_exe_anomaly.yml") as f:
        yaml = f.read()

    # create rule
    payload = {"yaml": yaml}
    res = client.post("/api/v1/rules/", json=payload)
    res.raise_for_status()

    id = res.json().get("id")
    assert id is not None

    # get rule
    res = client.get(f"/api/v1/rules/{id}")
    assert res.json().get("id") == id

    # get rules
    res = client.get("/api/v1/rules/")
    rules = cast(list[dict], res.json())
    assert id in [rule.get("id") for rule in rules]

    # delete rule
    res = client.delete(f"/api/v1/rules/{id}")
    assert res.status_code == 204
