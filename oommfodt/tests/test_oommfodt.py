import os
import oommfodt
import numpy as np
import pandas as pd


test_file1 = os.path.join(os.path.dirname(__file__),
                          'test_odt_files/test_odt_file1.odt')
test_file2 = os.path.join(os.path.dirname(__file__),
                          'test_odt_files/test_odt_file2.odt')


def test_read():
    for test_file in [test_file1, test_file2]:
        df = oommfodt.read(test_file)

        assert isinstance(df, pd.DataFrame)
        assert isinstance(df.units, dict)
        for i in df.units.values():
            assert isinstance(i, str)
        assert 'J' in df.units.values()
        assert '{}' in df.units.values()

        for column in df.columns:
            assert ':' not in column

        assert 'E' in df.columns


def test_single_row():
    df = oommfodt.read(test_file1)

    assert len(df.columns) == 23
    assert len(df['E'].values) == 1


def test_multiple_rows():
    df = oommfodt.read(test_file2)

    dt = 5e-12
    T = 1e-9
    tol = 1e-20
    t_array = df['t'].values
    assert len(t_array) == 200
    assert abs(t_array.min() - dt) < tol
    assert abs(t_array.max() - T) < tol
    assert t_array.min() == t_array[0]
    assert t_array.max() == t_array[-1]
    assert np.all(np.sort(t_array) == t_array)


def test_can_write_xlsx():
    df = oommfodt.read(test_file2, replace_columns=False)

    df.to_excel('tmp.xlsx')

    df_load = pd.read_excel('tmp.xlsx')
    assert df_load.shape == (200, 22)
    assert np.allclose(np.array(df_load), np.array(df))

    os.remove("tmp.xlsx")


def test_can_write_xls():
    df = oommfodt.read(test_file1)

    df.to_excel('tmp.xls')

    df_load = pd.read_excel('tmp.xls')
    assert df_load.shape == (1, 23)
    assert np.allclose(np.array(df_load), np.array(df))

    os.remove("tmp.xls")


def test_merge_files():
    df = oommfodt.merge([test_file1, test_file2])
    assert df.shape == (201, 30)
