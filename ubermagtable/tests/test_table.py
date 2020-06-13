import os
import pytest
import numbers
import tempfile
import ipywidgets
import pandas as pd
import ubermagtable as ut
import matplotlib.pyplot as plt


def check_table(table):
    assert isinstance(table, ut.Table)
    assert isinstance(table.data, pd.DataFrame)
    assert isinstance(table.units, dict)

    assert isinstance(table.data_columns, list)
    assert all(isinstance(i, str) for i in table.data_columns)

    assert isinstance(repr(table), str)

    if table.time_column is not None:
        assert isinstance(table.time_column, str)
        assert table.time_column in ['t', 'TimeDriver::Simulation time']

        assert isinstance(table.length, numbers.Real)
        assert table.length > 0

        res = table << table
        assert isinstance(res, ut.Table)
        assert res.length == 2 * table.length

        assert isinstance(table.slider(), ipywidgets.SelectionRangeSlider)
        assert isinstance(table.selector(), ipywidgets.SelectMultiple)


class TestTable:
    def setup(self):
        dirname = os.path.join(os.path.dirname(__file__), 'test_sample/')
        filenames = ['oommf-file1.odt',
                     'oommf-file2.odt',
                     'oommf-file3.odt',
                     'oommf-file4.odt',
                     'oommf-file5.odt',
                     'oommf-file6.odt',
                     'oommf-file7.odt',
                     'oommf-file8.odt',
                     'mumax3-file1.txt',
                     'oommf-mel-file.odt']

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

    def test_time_data_columns(self):
        table = ut.Table.fromfile(self.odtfiles[0], rename=False)
        assert table.time_column == 'TimeDriver::Simulation time'
        assert 'TimeDriver::mx' in table.data_columns

        table = ut.Table.fromfile(self.odtfiles[0], rename=True)
        assert table.time_column == 't'
        assert 'mx' in table.data_columns

    def test_length(self):
        table = ut.Table.fromfile(self.odtfiles[0])
        assert abs(table.length - 25e-12) < 1e-15

        # Exception
        table = ut.Table.fromfile(self.odtfiles[2])
        with pytest.raises(ValueError):
            res = table.length

    def test_lshift(self):
        table1 = ut.Table.fromfile(self.odtfiles[0])
        table2 = ut.Table.fromfile(self.odtfiles[1])

        res = table1 << table2

        assert res.length == table1.length + table2.length
        # Are all time values unique?
        assert len(set(res.data[res.time_column].to_numpy())) == 40

        # Exception
        table3 = ut.Table.fromfile(self.odtfiles[2])
        with pytest.raises(ValueError):
            res = table1 << table3

        with pytest.raises(ValueError):
            res = table3 << table1

        with pytest.raises(TypeError):
            res = table3 << 5

    def test_mpl(self):
        table = ut.Table.fromfile(self.odtfiles[0])

        # No axis
        table.mpl()

        # Axis
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)
        table.mpl(ax=ax)

        # figsize
        table.mpl(figsize=(10, 5))

        # multiplier
        table.mpl(multiplier=1e-6)

        # yaxis
        table.mpl(yaxis=['E', 'mx'])

        # xlim
        table.mpl(xlim=(0, 20e-12))

        # kwargs
        table.mpl(marker='o')

        # filename
        filename = 'table-plot.pdf'
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfilename = os.path.join(tmpdir, filename)
            table.mpl(filename=tmpfilename)

        # Exception - no time column
        table = ut.Table.fromfile(self.odtfiles[2])
        with pytest.raises(ValueError):
            table.mpl()

        plt.close('all')

    def test_slider(self):
        # Exception
        table = ut.Table.fromfile(self.odtfiles[2])
        with pytest.raises(ValueError):
            slider = table.slider()

    def test_oommf_mel(self):
        table = ut.Table.fromfile(self.odtfiles[-1])
        columns = table.data.columns.to_list()
        assert len(columns) == 16
