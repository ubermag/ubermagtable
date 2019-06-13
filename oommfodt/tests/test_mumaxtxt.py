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
#test_file2 = os.path.join(test_sample_dirname, 'file2.txt')
#test_file3 = os.path.join(test_sample_dirname, 'file3.txt')
#test_file4 = os.path.join(test_sample_dirname, 'file4.txt')
#test_file5 = os.path.join(test_sample_dirname, 'file5.txt')
#test_file6 = os.path.join(test_sample_dirname, 'file6.txt')
#test_file7 = os.path.join(test_sample_dirname, 'file7.txt')
#test_file8 = os.path.join(test_sample_dirname, 'file8.txt')
test_files = [test_file1]


def test_columns():
    def check(columns):
        assert isinstance(columns, list)
        assert all(isinstance(column, str) for column in columns)

    for test_file in test_files:
        # Without rename
        columns = oo.mumax_columns(test_file, rename=False)
        check(columns)
        #assert all(':' in column for column in columns) - these tests don't make sense for mumax

        # With rename
        columns = oo.mumax_columns(test_file, rename=True)
        check(columns)
        #assert all(':' not in column for column in columns)


def test_data():
    for test_file in test_files:
        data = oo.mumax_data(test_file)
        assert isinstance(data, list)
        assert all(isinstance(x, float) for x in itertools.chain(*data))


def test_read():
    for test_file in test_files:
        # Without rename
        df = oo.mumax_read(test_file, rename=False)
        assert isinstance(df, pd.DataFrame)

        # With rename
        df = oo.mumax_read(test_file, rename=True)
        assert isinstance(df, pd.DataFrame)


def test_read_timedriver1():
    df = oo.mumax_read(test_file1)
    assert df.shape == (10, 11)

    t = df['t'].values
    assert abs(t[0] - 1e-10) < tol
    assert abs(t[-1] - 10e-10) < tol
