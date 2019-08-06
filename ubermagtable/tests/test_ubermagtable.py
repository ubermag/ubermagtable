import os
import math
import pytest
import itertools
import numpy as np
import pandas as pd
import ubermagtable as ut

tol = 1e-20
test_sample_dirname = os.path.join(os.path.dirname(__file__),
                                   'test_sample/')
oommf_file1 = os.path.join(test_sample_dirname, 'oommf_file1.odt')
oommf_file2 = os.path.join(test_sample_dirname, 'oommf_file2.odt')
oommf_file3 = os.path.join(test_sample_dirname, 'oommf_file3.odt')
oommf_file4 = os.path.join(test_sample_dirname, 'oommf_file4.odt')
oommf_file5 = os.path.join(test_sample_dirname, 'oommf_file5.odt')
oommf_file6 = os.path.join(test_sample_dirname, 'oommf_file6.odt')
oommf_file7 = os.path.join(test_sample_dirname, 'oommf_file7.odt')
oommf_file8 = os.path.join(test_sample_dirname, 'oommf_file8.odt')

oommf_files = [oommf_file1, oommf_file2, oommf_file3, oommf_file4,
              oommf_file5, oommf_file6, oommf_file7, oommf_file8]

mumax_file1 = os.path.join(test_sample_dirname, 'mumax_file1.txt')
mumax_files = [mumax_file1]

all_files = oommf_files + mumax_files

def test_columns():
    def check(columns):
        assert isinstance(columns, list)
        assert all(isinstance(column, str) for column in columns)

    for f in all_files:
        # Without rename
        columns = ut.columns(f, rename=False)
        check(columns)

        # With rename
        columns = ut.columns(f, rename=True)
        check(columns)


def test_units():
    def check(units):
        assert isinstance(units, dict)
        assert all(isinstance(unit, str) for unit in units.keys())
        assert all(isinstance(unit, str) for unit in units.values())
        assert 'J' in units.values()
        assert '' in units.values()

    for f in all_files:
        # Without rename
        units = ut.units(f, rename=False)
        check(units)

        # With rename
        units = ut.units(f, rename=True)
        check(units)


def test_data():
    for f in all_files:
        data = ut.data(f)
        assert isinstance(data, list)
        assert all(isinstance(x, float) for x in itertools.chain(*data))


def test_read():
    for f in all_files:
        # Without rename
        df = ut.read(f, rename=False)
        assert isinstance(df, pd.DataFrame)

        # With rename
        df = ut.read(f, rename=True)
        assert isinstance(df, pd.DataFrame)


def test_read_oommf_timedriver1():
    df = ut.read(oommf_file1)
    assert df.shape == (25, 18)

    t = df['t'].values
    assert abs(t[0] - 1e-12) < tol
    assert abs(t[-1] - 25e-12) < tol


def test_read_oommf_timedriver2():
    df = ut.read(oommf_file2)
    assert df.shape == (15, 18)

    t = df['t'].values
    assert abs(t[0] - 1e-12) < tol
    assert abs(t[-1] - 15e-12) < tol


def test_read_mumax_timedriver1():
    df = ut.read(mumax_file1)
    assert df.shape == (10, 11)

    t = df['t'].values
    assert abs(t[0] - 1e-10) < tol
    assert abs(t[-1] - 10e-10) < tol


def test_read_oommf_mindriver():
    df = ut.read(oommf_file3)
    assert df.shape == (1, 20)


def test_merge_files():
    # Without time merge
    df = ut.merge(oommf_files[3:])
    assert df.shape == (56, 25)
    assert any(math.isnan(x) for x in df['t'].values)

    # With time merge - exception should be raised because one of the
    # files is from MinDriver.
    with pytest.raises(ValueError):
        df = ut.merge(oommf_files[3:], mergetime=True)

    # With time merge
    odtfiles = [oommf_file4, oommf_file5, oommf_file6, oommf_file8]
    df = ut.merge(odtfiles, mergetime=True)
    assert df.shape == (55, 19)
    assert min(df['tm'].values) == 1e-12
    assert max(df['tm'].values) == 50e-12
    assert 0 not in np.diff(df['tm'].values)  # monotonic

    # With time merge, pandas.DataFrames are passed
    df1 = ut.read(oommf_file4)
    df2 = ut.read(oommf_file8)
    df = ut.merge([df1, df2], mergetime=True)
    assert df.shape == (30, 19)
    assert min(df['tm'].values) == 1e-12
    assert max(df['tm'].values) == 30e-12
    assert 0 not in np.diff(df['tm'].values)  # monotonic
