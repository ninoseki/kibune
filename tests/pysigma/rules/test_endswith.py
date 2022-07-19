import pytest

from kibune.pysigma import PySigma


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": "foo", "b": "bar", "c": "baz"}, True),
        ({"a": "foo"}, True),
        ({"a": "bar_foo"}, True),
        ({"a": "foobar"}, False),
        ({"b": "bar"}, False),
        ({"a": "bar", "b": "foo"}, False),
    ],
)
def test_endswith(event: dict, expected: bool):
    with open("tests/fixtures/endswith.yml") as f:
        sigma = PySigma(rule=f.read())

    sigma.check_events([event])

    assert sigma.has_hits() is expected
