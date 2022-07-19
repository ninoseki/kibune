from kibune import schemas


def test_rule_create():
    with open("tests/fixtures/win_system_exe_anomaly.yml") as f:
        text = f.read()
        obj = schemas.RuleCreate(yaml=text)

    assert obj.yaml == text
    assert (
        obj.sha256 == "34f22389a0f48d0f8c05744c5348852376313d60650c605c8c453ecac4086355"
    )
