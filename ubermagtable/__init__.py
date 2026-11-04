"""Manipulation of tabular data."""

import importlib.metadata

import pytest

from .interact import interact as interact
from .table import Table as Table
from .table import sample_data as sample_data

__version__ = importlib.metadata.version(__package__)


def test():
    """Run all package tests.

    Examples
    --------
    1. Run all tests.

    >>> import ubermagtable as ut
    ...
    >>> # ut.test()

    """
    return pytest.main(["-v", "--pyargs", "ubermagtable", "-l"])  # pragma: no cover
