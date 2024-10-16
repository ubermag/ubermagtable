import numbers
import os
import tempfile

import ipywidgets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

import ubermagtable as ut

# TODO This file still contains a few assumptions about how data will look like,
# e.g. we use the strings "t", "mx", "iteration", etc.
# Think about how to generalise this/move it to some fixtures so that adapters
# can overwrite it


def check_table(table):
    assert isinstance(table, ut.Table)
    assert isinstance(table.data, pd.DataFrame)
    assert isinstance(table.units, dict)

    assert isinstance(table.y, list)
    assert all(isinstance(i, str) for i in table.y)

    assert isinstance(repr(table), str)

    if table.x is not None:
        assert isinstance(table.x, str)
        assert table.x in ["t", "iteration", "B"]

        assert isinstance(table.xmax, numbers.Real)
        assert table.xmax > 0

        res = table << table
        assert isinstance(res, ut.Table)
        assert res.xmax == 2 * table.xmax

        assert isinstance(table.slider(), ipywidgets.SelectionRangeSlider)
        assert isinstance(table.selector(), ipywidgets.SelectMultiple)


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
    data = pd.DataFrame({"E": 1e-19, "mx": 0, "my": 0, "mz": 1}, index=[0])
    units = {"E": "J", "mx": "", "my": "", "mz": ""}
    return ut.Table(data, units, **table_kwargs)


# TODO: setting tmin = 0 breaks some tests; is this a real problem or unrealistic data?
def _table_llg_factory(*, table_kwargs=None, **kwargs):
    if table_kwargs is None:
        table_kwargs = {}
    n = 20
    ts = np.linspace(1e-9 / 20, 1e-9, n)
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
    return _table_llg_factory


@pytest.fixture(params=[_table_energy_minimisation_factory, _table_llg_factory])
def table_factory(request):
    return request.param


def test_table_init():
    """Basic check creating an empty Table."""
    table = ut.Table(pd.DataFrame(), units={})
    assert isinstance(table, ut.Table)
    assert isinstance(table.data, pd.DataFrame)


def test_table_attributes(table_factory):
    """Check conversion of different samples into Table objects.

    Adapter modules should overwrite table_factory to provide real samples.
    """
    table = table_factory(rename=False)
    check_table(table)

    table_short_names = table_factory(rename=True)
    check_table(table_short_names)

    assert len(table.data) == len(table_short_names.data)
    assert len(table.data.columns) == len(table_short_names.data.columns)


@pytest.mark.parametrize("rename", [True, False])
def test_table_columns(table_factory, rename):
    columns = table_factory(rename=rename).data.columns
    assert all(isinstance(column, str) for column in columns)
    assert len(columns) == len(set(columns))  # unique column names


@pytest.mark.parametrize("rename", [True, False])
def test_table_units(table_factory, rename):
    units = table_factory(rename=rename).units
    assert isinstance(units, dict)
    assert all(isinstance(unit, str) for unit in units.keys())
    assert all(isinstance(unit, str) for unit in units.values())
    assert "J" in units.values()  # Energy is always in
    assert "" in units.values()  # Columns with no units are always in


def test_table_xy(table_llg_factory):
    """Test setting table.x and automatic table.y generation."""
    table = table_llg_factory(table_kwargs={"x": "t"})
    assert table.x == "t"
    assert "mx" in table.y
    assert "t" not in table.y

    with pytest.raises(ValueError):
        table = table_llg_factory(table_kwargs={"x": "wrong"})


# TODO: how do we best generalise this test?
@pytest.mark.skip
def test_table_xmax(self):
    table = ut.Table.fromfile(self.odtfiles[0], x="t")
    assert abs(table.xmax - 25e-12) < 1e-15


def test_table_lshift(table_llg_factory):
    table1 = table_llg_factory(table_kwargs={"x": "t"})
    table2 = table_llg_factory(table_kwargs={"x": "t"})

    res = table1 << table2

    assert res.xmax == table1.xmax + table2.xmax
    # Are all time values unique?
    assert len(set(res.data[res.x].to_numpy())) == len(table1.data) + len(table2.data)

    # Concatenating tables with different independent variables "x" is not possible
    table3 = table_llg_factory(table_kwargs={"x": "mx"})
    with pytest.raises(ValueError):
        res = table1 << table3

    with pytest.raises(ValueError):
        res = table3 << table1

    with pytest.raises(TypeError):
        res = table3 << 5


def test_table_mpl(table_factory):
    table = table_factory()

    # plotting requires 'x' to be set to a column in the data frame;
    # we set it to the first column ("t" or "iteration") for the mock data
    if table.x is None:
        table.x = list(table.units.keys())[0]

    # No axis
    table.mpl()

    # Axis
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    table.mpl(ax=ax)

    # figsize
    table.mpl(figsize=(10, 5))

    # x
    table.mpl(x="mx")

    # multiplier
    table.mpl(multiplier=1e-6)

    # yaxis
    table.mpl(y=["mx", "my"])

    # xlim
    table.mpl(xlim=(0, 20e-12))

    # kwargs
    table.mpl(marker="o")

    # filename
    filename = "table-plot.pdf"
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfilename = os.path.join(tmpdir, filename)
        table.mpl(filename=tmpfilename)

    # Exception - invalid column name
    with pytest.raises(ValueError):
        table.mpl(x="wrong")

    plt.close("all")


def test_table_rfft(table_llg_factory):
    table = table_llg_factory(table_kwargs={"x": "t"})
    fft_table = table.rfft()
    fft_table.x = None
    check_table(fft_table)


# TODO
def test_table_irfft(table_llg_factory):
    table = table_llg_factory(table_kwargs={"x": "t"})
    fft_table = table.rfft()
    ifft_table = fft_table.irfft()
    ifft_table.x = None  # TODO ASK SAM WHY THIS IS SET TO NONE
    check_table(ifft_table)
    assert np.allclose(ifft_table.data["t"].values, table.data["t"].values)
    for y in ifft_table.y:
        assert np.allclose(ifft_table.data[y].values, table.data[y].values)


# TODO: how do we best deal with this?
@pytest.mark.skip
def test_table_slider(self):
    # Exception
    table = ut.Table.fromfile(self.odtfiles[0], x="t")
    assert isinstance(table.slider(x="t"), ipywidgets.SelectionRangeSlider)
    table = ut.Table.fromfile(self.odtfiles[-5], x="B_hysteresis")
    assert isinstance(table.slider(x="B_hysteresis"), ipywidgets.SelectionRangeSlider)
    with pytest.raises(ValueError):
        table.slider(x="wrong")


# TODO: how do we best deal with this?
@pytest.mark.skip
def test_table_selector(self):
    table = ut.Table.fromfile(self.odtfiles[0], x="t")
    assert isinstance(table.selector(x="t"), ipywidgets.SelectMultiple)
    table = ut.Table.fromfile(self.odtfiles[-4], x="iteration")
    assert isinstance(table.selector(), ipywidgets.SelectMultiple)
    # Exception
    with pytest.raises(ValueError):
        table.selector(x="wrong")
