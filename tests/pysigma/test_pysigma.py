from kibune.pysigma import PySigma


def test_with_win_system_exe_anomaly():
    with open("tests/fixtures/win_system_exe_anomaly.yml") as f:
        sigma = PySigma(f.read())

    assert sigma.rule is not None
