from __future__ import annotations

import pytest

from jaraco.text import join_continuation


def test_join_continuation_typing() -> None:
    """
    Ensures that the type annotation for join_continuation matches what we expect at runtime,
    since checkers seem to give a false-positive on supporting ``__iter__`` and ``__next__``.
    """

    good: list[str] = ['foo \\', 'bar', 'baz']
    expected: list[str] = ['foobar', 'baz']

    # Ensure consistency at runtime for different iterables and no type error
    assert list(join_continuation(good)) == expected
    assert list(join_continuation(tuple(good))) == expected
    assert list(join_continuation(map(lambda string: string, good))) == expected
    assert list(join_continuation(iter(good))) == expected
    assert list(join_continuation({string: None for string in good})) == expected

    # NOTE: str isn't an expected use-case
    # but unfortunately a str is an iterable of str, so we can't validate

    # iter supports SupportsGetItem[int, str], but we don't !
    bad: dict[int, str] = {i: string for (i, string) in enumerate(good)}
    with pytest.raises(AttributeError):
        list(join_continuation(bad))  # type: ignore[arg-type] # Testing for type error here!


def test_join_continuation_edge_cases() -> None:
    """Edge cases for join_continuation."""
    assert list(join_continuation([])) == []
    assert list(join_continuation(['\\'])) == []
    assert list(join_continuation(['foo \\', 'bar \\'])) == []
