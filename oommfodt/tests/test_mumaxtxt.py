import os
import math
import pytest
import itertools
import numpy as np
import pandas as pd
import oommfodt as oo

tol = 1e-20
test_sample_dirname = os.path.join(os.path.dirname(__file__),
                                   'test_sample/mumax_samples')
test_file1 = os.path.join(test_sample_dirname, 'table1.txt')
test_files = [test_file1]


def test_columns():
    def check(columns):
        assert isinstance(columns, list)
        assert all(isinstance(column, str) for column in columns)

    for test_file in test_files:
        # Without rename
        columns = oo.columns(test_file, rename=False)
        check(columns)
        #assert all(':' in column for column in columns) - these tests don't make sense for mumax

        # With rename
        columns = oo.columns(test_file, rename=True)
        check(columns)
        #assert all(':' not in column for column in columns)


def test_units():
    def check(units):
        assert isinstance(units, dict)
        assert all(isinstance(unit, str) for unit in units.keys())
        assert all(isinstance(unit, str) for unit in units.values())
        assert 'J' in units.values()
        assert '' in units.values()

    for test_file in test_files:
        # Without rename
        units = oo.units(test_file, rename=False)
        check(units)

        # With rename
        units = oo.units(test_file, rename=True)
        check(units)


def test_data():
    for test_file in test_files:
        data = oo.data(test_file)
        assert isinstance(data, list)
        assert all(isinstance(x, float) for x in itertools.chain(*data))


def test_read():
    for test_file in test_files:
        # Without rename
        df = oo.read(test_file, rename=False)
        assert isinstance(df, pd.DataFrame)

        # With rename
        df = oo.read(test_file, rename=True)
        assert isinstance(df, pd.DataFrame)


def test_read_timedriver1():
    df = oo.read(test_file1)
    assert df.shape == (10, 11)

    t = df['t'].values
    assert abs(t[0] - 1e-10) < tol
    assert abs(t[-1] - 10e-10) < tol
