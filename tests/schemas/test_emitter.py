import pytest

from kibune import schemas


def test_emitter_create_with_invalid_j2_format():
    with pytest.raises(ValueError):
        schemas.EmitterCreate(
            rule_id="dummy",
            url="http://example.com",
            template="{% for row in search %}",
        )
