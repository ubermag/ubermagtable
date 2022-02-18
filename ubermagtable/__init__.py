"""Manipulation of tabular data."""
import os
import pytest
import pkg_resources
from .table import Table
from .interact import interact
import matplotlib.pyplot as plt

# Enable default plotting style.
dirname = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(dirname, 'util', 'plotting-style.mplstyle')
plt.style.use(path)

__version__ = pkg_resources.get_distribution(__name__).version


def test():
    """Run all package tests.

    Examples
    --------
    1. Run all tests.

    >>> import ubermagtable as ut
    ...
    >>> # ut.test()

    """
    return pytest.main(['-v', '--pyargs',
                        'ubermagtable', '-l'])  # pragma: no cover
