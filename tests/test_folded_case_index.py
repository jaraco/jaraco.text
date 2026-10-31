from __future__ import annotations

from typing import SupportsIndex

import pytest

from jaraco.text import FoldedCase


@pytest.mark.parametrize(
    ('text', 'sub', 'start', 'end', 'expected'),
    [
        ('Straße', 'E', None, None, 5),
        ('İx', 'X', None, None, 1),
        ('ﬃx', 'X', None, None, 1),
        ('Straße', 'E', 5, 6, 5),
        ('ßxy', 'Y', -1, None, 2),
        ('ßx', 'SS', 0, 1, 0),
        ('Straße', 'SS', None, None, 4),
        ('Straße', '', 6, None, 6),
        ('', '', None, None, 0),
        ('Hello World', 'O', 5, -1, 7),
    ],
)
def test_index_original_positions(
    text: str, sub: str, start: int | None, end: int | None, expected: int
) -> None:
    assert FoldedCase(text).index(sub, start, end) == expected


@pytest.mark.parametrize(
    ('text', 'sub', 'start', 'end'),
    [
        ('ßx', 'S', 1, None),
        ('ßx', 'X', 0, 1),
        ('Straße', '', 7, None),
        ('Hello', 'H', 3, 1),
        ('Hello', 'missing', None, None),
    ],
)
def test_index_outside_original_bounds(
    text: str, sub: str, start: int | None, end: int | None
) -> None:
    with pytest.raises(ValueError, match='substring not found'):
        FoldedCase(text).index(sub, start, end)


@pytest.mark.parametrize('text', ['Hello', 'Straße', 'Äpfel'])
def test_index_resolves_bounds_once(text: str) -> None:
    class Bound:
        calls = 0

        def __init__(self, value: int) -> None:
            self.value = value

        def __index__(self) -> int:
            self.calls += 1
            assert self.calls == 1
            return self.value

    assert (
        FoldedCase(text).index(text[-1], Bound(-1), Bound(len(text))) == len(text) - 1
    )


@pytest.mark.parametrize(
    ('character', 'limit'),
    [
        pytest.param('A', 4_000_000, id='ascii'),
        pytest.param('ß', 16_000_000, id='unicode'),
    ],
)
def test_index_immediate_match_memory(character: str, limit: int) -> None:
    try:
        import tracemalloc
    except ImportError:
        pytest.skip('tracemalloc is unavailable')

    value = FoldedCase('A' + character * 999_999)
    tracemalloc.start()
    try:
        assert value.index('a') == 0
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    # Allow str.casefold's temporary Unicode buffer and compact metadata, but
    # not one Python int per source character. No timing threshold.
    assert peak < limit


@pytest.mark.parametrize('character', ['A', 'ß'])
def test_index_advancing_search_has_bounded_slice_work(character: str) -> None:
    class CountingCase(FoldedCase):
        sliced = 0

        def __getitem__(self, key: slice | SupportsIndex) -> str:
            result = super().__getitem__(key)
            if isinstance(key, slice):
                self.sliced += len(result)
            return result

    value = CountingCase(character * 20_000)
    for start in range(0, len(value), 20):
        assert value.index(character, start) == start
    # A generous linear budget allows fixed-size block work per query, but
    # rejects repeatedly copying the entire remaining suffix (10M characters).
    assert value.sliced < 4_000_000


@pytest.mark.parametrize('position', [1022, 1023, 1024, 1025, 2047, 2048, 2049])
def test_index_expansions_across_blocks(position: int) -> None:
    text = 'ß' * position + 'İﬃZ' + 'ß' * 1100
    value = FoldedCase(text)
    assert value.index('i\u0307ffiZ', position, position + 3) == position
    assert value.index('FF', position + 1, position + 2) == position + 1
    assert value.index('Z', -1101, -1100) == position + 2
    assert value.index('', position + 3, position + 3) == position + 3
    with pytest.raises(ValueError, match='substring not found'):
        value.index('Z', 0, position + 2)


@pytest.mark.parametrize('text', ['Hello', 'Straße', 'Äpfel'])
@pytest.mark.parametrize('start,end', [(10**100, None), (2, 1), (1, -(10**100))])
def test_index_invalid_empty_bounds(text: str, start: int, end: int | None) -> None:
    with pytest.raises(ValueError, match='substring not found'):
        FoldedCase(text).index('', start, end)
