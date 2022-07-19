import base64

import pytest

from kibune.pysigma import PySigma


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"a": base64.encodebytes(b"foo").decode()}, True),
        ({"a": base64.b64encode(b"foo").decode()}, True),
        ({"a": "foo"}, False),
    ],
)
def test_base64(event, expected):
    with open("tests/fixtures/base64.yml") as f:
        sigma = PySigma(rule=f.read())

    sigma.check_events([event])
    assert sigma.has_hits() is expected

    assert len(sigma.check_events([{"a": base64.b64encode(b"foo").decode()}])) == 1
    assert len(sigma.check_events([{"a": base64.encodebytes(b"foo").decode()}])) == 1
