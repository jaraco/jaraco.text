from __future__ import annotations

import io
import subprocess
import sys
from collections.abc import Iterable

import pytest

from jaraco.text import Stripper


@pytest.mark.parametrize('lines', [[], (), iter(()), io.StringIO('')])
def test_empty_input(lines: Iterable[str]) -> None:
    result = Stripper.strip_prefix(lines)
    assert result.prefix == ''
    assert list(result.lines) == []


@pytest.mark.parametrize(
    ('source', 'expected'),
    [
        ('', ''),
        ('abcdef\nabc123\n', 'def\n123\n'),
        ('alpha\nbravo\n', 'alpha\nbravo\n'),
    ],
)
def test_strip_prefix_command(source: str, expected: str) -> None:
    result = subprocess.run(
        [sys.executable, '-m', 'jaraco.text.strip-prefix'],
        input=source,
        text=True,
        encoding='utf-8',
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == expected
    assert result.stderr == ''
