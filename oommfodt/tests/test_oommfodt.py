import os
import oommfodt
import numpy as np
import pandas as pd


test_file = os.path.join(os.path.dirname(__file__), 'test_odt_file.odt')


def test_read():
    df = oommfodt.read(test_file)

    assert isinstance(df, pd.DataFrame)

    assert len(df.columns) == 19

    assert isinstance(df.units, list)
    for i in df.units:
        assert isinstance(i, str)

    assert 'J' in df.units
    assert '{}' in df.units
    assert 'deg/ns' in df.units

    assert len(df['E'].as_matrix()) == 200

    assert df.as_matrix().shape == (200, 19)


def test_times():
    df = oommfodt.read(test_file)

    dt = 5e-12
    T = 1e-9
    tol = 1e-20
    t_array = df['t'].as_matrix()
    assert len(t_array) == 200
    assert abs(t_array.min() - dt) < tol
    assert abs(t_array.max() - T) < tol
    assert t_array.min() == t_array[0]
    assert t_array.max() == t_array[-1]
    assert np.all(np.sort(t_array) == t_array)


def test_can_write_xlsx():
    df = oommfodt.read(test_file)

    df.to_excel('tmp.xlsx')

    df_load = pd.read_excel('tmp.xlsx')
    assert df_load.shape == (200, 19)
    assert np.allclose(np.array(df_load), np.array(df))

    os.remove("tmp.xlsx")


def test_can_write_xls():
    df = oommfodt.read(test_file)

    df.to_excel('tmp.xls')

    df_load = pd.read_excel('tmp.xls')
    assert df_load.shape == (200, 19)
    assert np.allclose(np.array(df_load), np.array(df))

    os.remove("tmp.xls")
