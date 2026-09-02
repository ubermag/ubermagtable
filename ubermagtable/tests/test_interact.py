import ipywidgets
import pytest

import ubermagtable as ut


def test_interact():
    table = ut.sample_data()

    # Only test whether it runs.
    @ut.interact(xlim=table.slider())
    def myplot(xlim):
        table.mpl(xlim=xlim)


def test_table_slider():
    table = ut.sample_data()
    assert isinstance(table.slider(x="t"), ipywidgets.SelectionRangeSlider)

    with pytest.raises(ValueError):
        table.slider(x="wrong")


def test_table_selector():
    table = ut.sample_data()
    assert isinstance(table.selector(x="t"), ipywidgets.SelectMultiple)

    with pytest.raises(ValueError):
        table.selector(x="wrong")
