import pytest

from jaraco.text import FoldedCase


@pytest.mark.parametrize('text', ['', '   ', '  alpha\t beta\n gamma  ', 'a\u2003b'])
def test_split_none_uses_whitespace(text: str) -> None:
    assert FoldedCase(text).split(None) == text.split()


def test_split_none_maxsplit() -> None:
    text = '  alpha\t beta\n gamma  '
    assert FoldedCase(text).split(None, 1) == text.split(None, 1)


def test_split_explicit_separator_is_case_insensitive() -> None:
    assert FoldedCase('oneXtwoxtHree').split('x', 1) == ['one', 'twoxtHree']
