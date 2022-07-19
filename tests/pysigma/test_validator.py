from kibune.pysigma.validator import run_sigma_validator


def test_run_sigma_validator():
    with open("tests/fixtures/win_system_exe_anomaly.yml") as f:
        validator = run_sigma_validator(f.read())
        assert len(validator.file_errors) == 0
