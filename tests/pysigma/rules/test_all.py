import pytest

from kibune.pysigma import PySigma


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foobar"}, True),
        ({"a": "foo"}, False),
        ({"a": "bar"}, False),
    ],
)
def test_all(event: dict, expected: bool):
    with open("tests/fixtures/all.yml") as f:
        sigma = PySigma(rule=f.read())

    sigma.check_events([event])

    assert sigma.has_hits() is expected
