import numbers
import os
import tempfile

import ipywidgets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

import ubermagtable as ut


def check_table(table):
    assert isinstance(table, ut.Table)
    assert isinstance(table.data, pd.DataFrame)
    assert isinstance(table.units, dict)

    assert isinstance(table.y, list)
    assert all(isinstance(i, str) for i in table.y)

    assert isinstance(repr(table), str)

    if table.x is not None:
        assert isinstance(table.x, str)
        assert table.x in ["t", "iteration", "B", None]

        assert isinstance(table.xmax, numbers.Real)
        assert table.xmax > 0

        res = table << table
        assert isinstance(res, ut.Table)
        assert res.xmax == 2 * table.xmax

        assert isinstance(table.slider(), ipywidgets.SelectionRangeSlider)
        assert isinstance(table.selector(), ipywidgets.SelectMultiple)


class TestTable:
    def setup(self):
        dirname = os.path.join(os.path.dirname(__file__), "test_sample/")
        filenames = [
            "oommf-old-file1.odt",
            "oommf-old-file2.odt",
            "oommf-old-file3.odt",
            "oommf-old-file4.odt",
            "oommf-old-file5.odt",
            "oommf-old-file6.odt",
            "oommf-old-file7.odt",
            "oommf-old-file8.odt",
            "oommf-new-file1.odt",
            "oommf-new-file2.odt",
            "oommf-new-file3.odt",
            "oommf-new-file4.odt",
            "oommf-new-file5.odt",
            "oommf-hysteresis1.odt",
            "oommf-minsteps.odt",
            "mumax3-file1.txt",
            "oommf-mel-file.odt",
            "oommf-issue1.odt",
        ]

        self.odtfiles = [os.path.join(dirname, f) for f in filenames]

    def test_init(self):
        table = ut.Table(pd.DataFrame(), units={})
        assert isinstance(table, ut.Table)
        assert isinstance(table.data, pd.DataFrame)

    def test_fromfile(self):
        for odtfile in self.odtfiles:
            for rename in [True, False]:
                table = ut.Table.fromfile(odtfile)
                check_table(table)

    def test_xy(self):
        table = ut.Table.fromfile(self.odtfiles[0], x="t")
        assert table.x == "t"
        assert "mx" in table.y

        with pytest.raises(ValueError):
            table = ut.Table.fromfile(self.odtfiles[0], x="wrong")

    def test_xmax(self):
        table = ut.Table.fromfile(self.odtfiles[0], x="t")
        assert abs(table.xmax - 25e-12) < 1e-15

    def test_lshift(self):
        table1 = ut.Table.fromfile(self.odtfiles[0], x="t")
        table2 = ut.Table.fromfile(self.odtfiles[1], x="t")

        res = table1 << table2

        assert res.xmax == table1.xmax + table2.xmax
        # Are all time values unique?
        assert len(set(res.data[res.x].to_numpy())) == 40

        # Exception
        table3 = ut.Table.fromfile(self.odtfiles[2], x="iteration")
        with pytest.raises(ValueError):
            res = table1 << table3

        with pytest.raises(ValueError):
            res = table3 << table1

        with pytest.raises(TypeError):
            res = table3 << 5

    def test_mpl(self):
        table = ut.Table.fromfile(self.odtfiles[0], x="t")

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
        table.mpl(y=["E", "mx"])

        # xlim
        table.mpl(xlim=(0, 20e-12))

        # kwargs
        table.mpl(marker="o")

        # filename
        filename = "table-plot.pdf"
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfilename = os.path.join(tmpdir, filename)
            table.mpl(filename=tmpfilename)

        # Exception - no time column
        table = ut.Table.fromfile(self.odtfiles[2])
        with pytest.raises(ValueError):
            table.mpl(x="t")

        # Hysteresis plot
        table = ut.Table.fromfile(self.odtfiles[-5], x="B_hysteresis")
        table.mpl()

        plt.close("all")

    def test_slider(self):
        # Exception
        table = ut.Table.fromfile(self.odtfiles[0], x="t")
        assert isinstance(table.slider(x="t"), ipywidgets.SelectionRangeSlider)
        table = ut.Table.fromfile(self.odtfiles[-5], x="B_hysteresis")
        assert isinstance(
            table.slider(x="B_hysteresis"), ipywidgets.SelectionRangeSlider
        )
        with pytest.raises(ValueError):
            table.slider(x="wrong")

    def test_selector(self):
        table = ut.Table.fromfile(self.odtfiles[0], x="t")
        assert isinstance(table.selector(x="t"), ipywidgets.SelectMultiple)
        table = ut.Table.fromfile(self.odtfiles[-4], x="iteration")
        assert isinstance(table.selector(), ipywidgets.SelectMultiple)
        # Exception
        with pytest.raises(ValueError):
            table.selector(x="wrong")

    def test_oommf_mel(self):
        table = ut.Table.fromfile(self.odtfiles[-2])
        columns = table.data.columns.to_list()
        assert len(columns) == 16

    def test_oommf_issue1(self):
        table = ut.Table.fromfile(self.odtfiles[-1])
        columns = table.data.columns.to_list()
        assert len(columns) == 30

    def test_rfft(self):
        table = ut.Table.fromfile(self.odtfiles[12], x="t")
        fft_table = table.rfft()
        fft_table.x = None
        check_table(fft_table)

    def test_irfft(self):
        table = ut.Table.fromfile(self.odtfiles[12], x="t")
        fft_table = table.rfft()
        ifft_table = fft_table.irfft()
        ifft_table.x = None
        check_table(ifft_table)
        assert np.allclose(ifft_table.data["t"].values, table.data["t"].values)
        for y in ifft_table.y:
            assert np.allclose(ifft_table.data[y].values, table.data[y].values)
