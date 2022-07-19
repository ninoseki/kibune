from fastapi.testclient import TestClient


def test_log(client: TestClient):
    res = client.get("/api/v1/logs/")
    res.raise_for_status()

    assert isinstance(res.json(), list)
