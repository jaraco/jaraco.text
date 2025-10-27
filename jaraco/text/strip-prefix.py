import sys

from jaraco.text import Stripper


def strip_prefix() -> None:
    r"""
    Strip any common prefix from stdin.

    >>> import io, pytest
    >>> getfixture('monkeypatch').setattr('sys.stdin', io.StringIO('abcdef\nabc123'))
    >>> strip_prefix()
    def
    123
    """
    sys.stdout.writelines(Stripper.strip_prefix(sys.stdin).lines)


try:
    import autocommand

    autocommand.autocommand(__name__)(strip_prefix)
except ModuleNotFoundError as error:  # pragma: nocover
    print(f"{error}. Did you forget to install it or `jaraco.text[autocommand]` ?")
