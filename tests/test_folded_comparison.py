import operator
from collections.abc import Callable

import pytest

from jaraco.text import FoldedCase


@pytest.mark.parametrize('compare', [operator.le, operator.ge])
@pytest.mark.parametrize('other', ['hello', FoldedCase('hello'), 'HELLO'])
def test_folded_ordering_equality(
    compare: Callable[[str, str], bool], other: str
) -> None:
    assert compare(FoldedCase('Hello'), other)
    assert compare(other, FoldedCase('Hello'))


def test_folded_ordering_distinct() -> None:
    assert FoldedCase('alpha') <= 'BETA'
    assert FoldedCase('BETA') >= 'alpha'
    assert not FoldedCase('BETA') <= 'alpha'
    assert not FoldedCase('alpha') >= 'BETA'
