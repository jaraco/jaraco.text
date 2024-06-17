import sys

import pytest

if sys.version_info < (3, 10):
    import pathlib2 as pathlib  # pragma: nocover
else:
    import pathlib  # pragma: nocover


@pytest.fixture
def tmp_path(tmp_path):
    """
    Override tmp_path to wrap in a more modern interface.
    """
    return pathlib.Path(tmp_path)
