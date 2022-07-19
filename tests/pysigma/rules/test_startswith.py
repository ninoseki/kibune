import pytest

from kibune.pysigma import PySigma


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo", "b": "bar", "c": "baz"}, True),
        ({"a": "foo"}, True),
        ({"a": "foobar"}, True),
        ({"b": "bar"}, False),
        ({"a": "bar", "b": "foo"}, False),
    ],
)
def test_startswith(event: dict, expected: bool):
    with open("tests/fixtures/startswith.yml") as f:
        sigma = PySigma(rule=f.read())

    sigma.check_events([event])

    assert sigma.has_hits() is expected
