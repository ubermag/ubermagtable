"""Manipulation of tabular data."""

import importlib.metadata
import os

import matplotlib.pyplot as plt
import pytest

from .interact import interact as interact
from .table import Table as Table

# Enable default plotting style.
dirname = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(dirname, "util", "plotting-style.mplstyle")
plt.style.use(path)

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
