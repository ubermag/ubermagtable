"""Fixtures for generic versions of tests.

Adapter modules must implement the same set of fixtures. Unsupported tests
can be skipped by calling `pytest.skip(...)` in the fixtures."""

import numpy as np
import pandas as pd
import pytest

import ubermagtable as ut


def _table_energy_minimisation_factory(*, table_kwargs=None, **kwargs):
    """Create sample tables for energy minimisation.

    Parameters
    ----------
    table_kwargs : dict
        Keyword arguments passed to Table.__init__, e.g. to set Table.x
    kwargs
        Keyword arguments to control the table reading function in the adapter class,
        e.g. to control column renaming. Passing keyword arguments has no effect in
        this implementation.
    """
    if table_kwargs is None:
        table_kwargs = {}
    data = pd.DataFrame(
        {"E": 1e-19, "mx": 0, "my": 0, "mz": 1, "iteration": 1}, index=[0]
    )
    units = {"E": "J", "mx": "", "my": "", "mz": "", "iteration": ""}
    return ut.Table(data, units, **table_kwargs)


# TODO: setting tmin = 0 breaks the lshift test; is this a real problem or unrealistic
# data?
def _table_llg_factory(*, table_kwargs=None, **kwargs):
    if table_kwargs is None:
        table_kwargs = {}
    n = 20
    ts = np.linspace(1e-9 / n, 1e-9, n)
    data = pd.DataFrame(
        {
            "t": ts,
            "E": np.linspace(-2e-18, -3e-18, n),
            "mx": np.sin(ts),
            "my": np.cos(ts),
            "mz": np.zeros_like(ts),
        }
    )
    units = {"t": "s", "E": "J", "mx": "", "my": "", "mz": ""}
    return ut.Table(data, units, **table_kwargs)


@pytest.fixture
def table_llg_factory():
    """LLG tables."""
    return _table_llg_factory


@pytest.fixture
def table_minimisation_factory():
    return _table_energy_minimisation_factory


@pytest.fixture
def table_hysteresis_factory():
    pytest.skip("Hysteresis not implemented.")


@pytest.fixture(params=[_table_energy_minimisation_factory, _table_llg_factory])
def table_factory(request):
    """Energy minimisation or LLG tables."""
    return request.param


@pytest.fixture
def table_llg_25ps():
    """LLG data with tmax=25ps."""
    data = pd.DataFrame(
        {
            "t": [25e-12],
            "mx": [1],
        }
    )
    units = {"t": "s", "mx": ""}
    return ut.Table(data, units, x="t")
