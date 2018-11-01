import os
import math
import itertools
import pandas as pd
import oommfodt as oo


tol = 1e-20
test_file1 = os.path.join(os.path.dirname(__file__),
                          'test_files', 'file1.odt')
test_file2 = os.path.join(os.path.dirname(__file__),
                          'test_files', 'file2.odt')
test_file3 = os.path.join(os.path.dirname(__file__),
                          'test_files', 'file3.odt')
test_files = [test_file1, test_file2, test_file3]


def test_columns():
    for test_file in test_files:
        columns = oo.columns(test_file, rename=False)
        assert isinstance(columns, list)
        assert all(isinstance(column, str) for column in columns)
        assert all(':' in column for column in columns)

        columns = oo.columns(test_file, rename=True)
        assert isinstance(columns, list)
        assert all(isinstance(column, str) for column in columns)
        assert all(':' not in column for column in columns)


def test_units():
    for test_file in test_files:
        units = oo.units(test_file, rename=False)
        assert isinstance(units, dict)
        assert all(isinstance(unit, str) for unit in units.keys())
        assert all(':' in unit for unit in units.keys())
        assert 'J' in units.values()
        assert '' in units.values()

        units = oo.units(test_file, rename=True)
        assert isinstance(units, dict)
        assert all(isinstance(unit, str) for unit in units.keys())
        assert all(':' not in unit for unit in units.keys())
        assert units['E'] == 'J'
        assert '' in units.values()


def test_data():
    for test_file in test_files:
        data = oo.data(test_file)
        assert isinstance(data, list)
        assert all(isinstance(x, float) for x in itertools.chain(*data))


def test_read():
    for test_file in test_files:
        df = oo.read(test_file, rename=False)
        assert isinstance(df, pd.DataFrame)

        df = oo.read(test_file, rename=True)
        assert isinstance(df, pd.DataFrame)


def test_read_timedriver1():
    df = oo.read(test_file1)
    assert df.shape == (25, 18)

    t = df['t'].values
    assert abs(t[0] - 1e-12) < tol
    assert abs(t[-1] - 25e-12) < tol


def test_read_timedriver2():
    df = oo.read(test_file2)
    assert df.shape == (15, 18)

    t = df['t'].values
    assert abs(t[0] - 1e-12) < tol
    assert abs(t[-1] - 15e-12) < tol


def test_read_mindriver():
    df = oo.read(test_file3)
    assert df.shape == (1, 20)


def test_merge_files():
    df = oo.merge(test_files)
    assert df.shape == (41, 24)
    assert any(math.isnan(x) for x in df['t'].values)
