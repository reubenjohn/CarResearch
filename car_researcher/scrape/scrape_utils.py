import re
from re import Match
from typing import Any, Iterable

from bs4 import ResultSet, Tag

WHITESPACES = re.compile('\s+')


def assert_unique(l: ResultSet) -> Tag:
    assert len(l) == 1, "Expected a unique result, but found: " + str(l)
    return l[0]


def assert_matches(match: Match) -> str:
    assert match, "Expected a successful regex match, but was: " + str(match)
    return match


def first_non_none(iter: Iterable) -> Any:
    result = next(filter(lambda x: x is not None, iter), None)
    assert result is not None, "Iterable did not contain any non None elements"
    return result


def parse_int(miles: str) -> int:
    return int(miles.replace(',', ''))


def remove_redundant_whitespace(s: str) -> str:
    return WHITESPACES.sub(' ', s).strip()
