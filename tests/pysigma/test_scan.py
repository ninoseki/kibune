import pytest

from kibune.pysigma import PySigma
from kibune.pysigma.utils import sigma_string_to_regex

event = {
    "cats": "good",
    "dogs": "good",
    "dog_count": 2,
    "birds": "many",
    "user": {"name": "foo"},
}


base_signature = """
title: sample signature
detection:
    true_expected: # dogs or dog_count
        - go?d
        - 2
    true_also_expected: # (dogs good or dogs ok) and cats good
        dogs:
            - good
            - ok
        cats: good
    true_cats_expected:
        cats: go*
    true_still_expected: # cats good or birds few
        - cats: good
        - birds: few
    false_expected: # frogs or trees
        - frogs
        - trees
    false_also_expected: # cats good and birds none
        cats: good
        birds: none
"""

complicated_condition = (
    base_signature
    + """
    condition: (all of true_*) and (1 of *_expected) and (1 of true_*) and not all of them and (all of them or true_expected)
"""
)


def test_or_search():
    # Test a signature where the search block is just a list (or operation)
    # Also has an example of the ? wildcard embedded
    sigma = PySigma(base_signature + "    condition: true_expected")
    assert len(sigma.check_events([event])) == 1


def test_value_or_search():
    # Test a signature where the search block has a list of values (or across those values)

    sigma = PySigma(base_signature + "    condition: true_also_expected")
    assert len(sigma.check_events([event])) == 1


def test_value_wildcard_search():
    # has an example of the * wildcard embedded
    sigma = PySigma(base_signature + "    condition: true_cats_expected")
    assert len(sigma.check_events([event])) == 1


def test_and_search():
    # Test a signature where the search block is just a map (and operation)
    sigma = PySigma(base_signature + "    condition: true_still_expected")
    assert len(sigma.check_events([event])) == 1


def test_complicated_condition():
    sigma = PySigma(complicated_condition)
    assert len(sigma.check_events([event])) == 1


def test_null_and_not_null():
    sigma = PySigma(
        """
        title: sample signature
        detection:
            forbid:
                x: null
            filter:
                y: null
            condition: forbid and not filter
    """
    )

    assert len(sigma.check_events([{"y": "found"}])) == 1
    assert (
        len(
            sigma.check_events(
                [
                    {
                        "z": "found",
                    }
                ]
            )
        )
        == 0
    )
    assert len(sigma.check_events([{"y": "found", "x": "also"}])) == 0


def test_substrings():
    # Is this what that part of the standard meant about list of strings anywhere?
    sigma = PySigma(
        """
        title: sample signature
        detection:
            signs:
                - "red things"
                - "blue things"
            condition: signs
    """
    )

    assert (
        len(
            sigma.check_events(
                [
                    {
                        "log": "all sorts of red things and blue things were there",
                    }
                ]
            )
        )
        == 1
    )


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"x": "a*ba"}, False),
        ({"x": "aba"}, False),
        ({"x": "a?a"}, False),
        ({"x": "a*a"}, True),
    ],
)
def test_escaped_wildcards_with_literal_starts(event, expected):
    sigma = PySigma(
        r"""
        title: literal_star
        id: 1
        detection:
            field:
                x: a\*a
            condition: field
    """
    )
    sigma.check_events([event])
    assert sigma.has_hits() is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"x": "a*ba"}, False),
        ({"x": "aba"}, False),
        ({"x": "a?a"}, True),
        ({"x": "a*a"}, False),
    ],
)
def test_escaped_wildcards_with_literal_question(event, expected):
    sigma = PySigma(
        r"""
        title: literal_question
        id: 2
        detection:
            field:
                x: a\?a
            condition: field
    """
    )
    sigma.check_events([event])
    assert sigma.has_hits() is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"x": "a*ba"}, True),
        ({"x": "aba"}, True),
        ({"x": "a?a"}, True),
        ({"x": "a*a"}, True),
    ],
)
def test_escaped_wildcards_with_star(event, expected):
    sigma = PySigma(
        """
        title: star
        id: 3
        detection:
            field:
                x: a*a
            condition: field
    """
    )
    sigma.check_events([event])
    assert sigma.has_hits() is expected


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"x": "a*ba"}, False),
        ({"x": "aba"}, True),
        ({"x": "a?a"}, True),
        ({"x": "a*a"}, True),
    ],
)
def test_escaped_wildcards_with_question(event, expected):
    sigma = PySigma(
        """
        title: question
        id: 4
        detection:
            field:
                x: a?a
            condition: field
    """
    )
    sigma.check_events([event])
    assert sigma.has_hits() is expected


def test_regex_transform():
    import regex as re

    assert sigma_string_to_regex(r".") == r"\."
    assert sigma_string_to_regex(r"*") == r".*"
    assert sigma_string_to_regex(r"?") == r"."
    assert sigma_string_to_regex(r".\*") == r"\.\*"
    assert sigma_string_to_regex(r".\?") == r"\.\?"
    assert sigma_string_to_regex(r".\*abc") == r"\.\*abc"
    assert sigma_string_to_regex(r".\*abc*") == r"\.\*abc.*"
    assert sigma_string_to_regex(r".\*abc?") == r"\.\*abc."
    assert sigma_string_to_regex(r".\*abc\?") == r"\.\*abc\?"
    assert sigma_string_to_regex(r".\*abc\\?") == r"\.\*abc\\."
    assert sigma_string_to_regex(r".\*abc\\\?") == r"\.\*abc\\\\."
    # assert sigma_string_to_regex(r'*\abc\*')  == r'.*\abc\.*'
    assert re.compile(sigma_string_to_regex(r"a\a")).fullmatch(r"a\a")
    assert re.compile(sigma_string_to_regex(r"a\\a")).fullmatch(r"a\\a")
    assert re.compile(sigma_string_to_regex(r"a\*a")).fullmatch(r"a*a")
    assert re.compile(sigma_string_to_regex(r"a*a")).fullmatch(
        r"a a bunch of garbage a"
    )


def test_1_of_them():
    # Make sure 1
    sigma = PySigma(
        """
        title: sample signature
        detection:
            a: ["a"]
            b: ["b"]
            condition: 1 of them
    """
    )

    assert len(sigma.check_events([{"log": "a"}])) == 1
    assert len(sigma.check_events([{"log": "b"}])) == 1
    assert len(sigma.check_events([{"log": "ab"}])) == 1
    assert len(sigma.check_events([{"log": "c"}])) == 0


def test_1_of_x():
    # Make sure 1
    sigma = PySigma(
        """
        title: sample signature
        detection:
            aa: ["aa"]
            ab: ["ab"]
            ba: ["ba"]
            bb: ["bb"]
            condition: 1 of a*
    """
    )

    assert len(sigma.check_events([{"log": "aa"}])) == 1
    assert len(sigma.check_events([{"log": "1ab ba ca"}])) == 1
    assert len(sigma.check_events([{"log": "ba"}])) == 0
    assert len(sigma.check_events([{"log": "aabb"}])) == 1


def test_all_of_them():
    # Make sure 1
    sigma = PySigma(
        """
        title: sample signature
        detection:
            a: ["a"]
            b: ["b"]
            condition: all of them
    """
    )

    assert len(sigma.check_events([{"log": "a"}])) == 0
    assert len(sigma.check_events([{"log": "b"}])) == 0
    assert len(sigma.check_events([{"log": "ab"}])) == 1
    assert len(sigma.check_events([{"log": "bac"}])) == 1
    assert len(sigma.check_events([{"log": "c"}])) == 0


def test_all_of_x():
    # Make sure 1
    sigma = PySigma(
        """
        title: sample signature
        detection:
            aa: ["aa"]
            ab: ["ab"]
            ba: ["ba"]
            bb: ["bb"]
            condition: all of a*
    """
    )

    assert len(sigma.check_events([{"log": "aa"}])) == 0
    assert len(sigma.check_events([{"log": "1ab ba ca"}])) == 0
    assert len(sigma.check_events([{"log": "ba"}])) == 0
    assert len(sigma.check_events([{"log": "aabb"}])) == 1


def test_nested_dict():
    sigma = PySigma(
        """
        title: sample signature
        detection:
            field:
                foo:
                    bar: a
            condition: field
    """
    )

    assert len(sigma.check_events([{"foo": {"bar": "a"}}])) == 1
    assert len(sigma.check_events([{"foo": {"bar": "b"}}])) == 0
    assert len(sigma.check_events([{"foo": "bar"}])) == 0
    assert len(sigma.check_events([{"log": "a"}])) == 0


def test_nested_dict_with_wildcard():
    sigma = PySigma(
        """
        title: sample signature
        detection:
            field:
                foo:
                    bar*: a
            condition: field
    """
    )

    assert len(sigma.check_events([{"foo": {"bar": "a"}}])) == 1
    assert len(sigma.check_events([{"foo": {"bar1": "a"}}])) == 1
    assert len(sigma.check_events([{"foo": {"bar2": "a"}}])) == 1
    assert len(sigma.check_events([{"foo": {"bar": "b"}}])) == 0
    assert len(sigma.check_events([{"foo": "bar"}])) == 0
    assert len(sigma.check_events([{"log": "a"}])) == 0
