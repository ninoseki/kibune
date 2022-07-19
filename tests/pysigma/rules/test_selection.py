import pytest

from kibune.pysigma import PySigma


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"Foo": "bar"}, True),
        ({"foo": "bar"}, False),
        ({"a": "bar", "b": "foo"}, False),
    ],
)
def test_selection(event: dict, expected: bool):
    with open("tests/fixtures/selection.yml") as f:
        sigma = PySigma(rule=f.read())

    sigma.check_events([event])

    assert sigma.has_hits() is expected
