import re
import functools
import pandas as pd

column_dict = {'RungeKuttaEvolve::Totalenergy': 'E',
               'UniformExchange::Energy': 'E_Exchange',
               'DMExchange6Ngbr::Energy': 'E_DMI',
               'DMI_Cnv::Energy': 'E_DMI_Cnv',
               'DMI_T::Energy': 'E_DMI_T',
               'DMI_D2d::Energy': 'E_DMI_D2d',
               'Demag::Energy': 'E_Demag',
               'FixedZeeman::Energy': 'E_Zeeman',
               'UZeeman::Energy': 'E_UZeeman',
               'CubicAnisotropy::Energy': 'E_CubicAnisotropy',
               'TimeDriver::Simulationtime': 't',
               'CGEvolve::Totalenergy': 'E',
               'SpinTEvolve::Totalenergy': 'E',
               'UniaxialAnisotropy::Energy': 'E_UniaxialAnisotropy',
               'UniaxialAnisotropy4::Energy': 'E_UniaxialAnisotropy4',
               'Southampton_UniaxialAnisotropy4::Energy':
               'E_UniaxialAnisotropy'}


def columns(filename, rename=True):
    """Extract the names of columns from an OOMMF `.odt` file.

    This function extracts the names of columns from an OOMMF .odt
    file and returns it as a list of strings. If rename=True, the
    column names will be renamed to their shorter versions.

    Parameters
    ----------
    filename : str
        Name of an OOMMF `.odt` file
    rename : bool
        Flag (the default is `True`). If `rename=True`, the column
        names are renamed with their shorter versions.

    Returns
    -------
    list(str)

    Examples
    --------
    1. Extracting the names of columns from an .odt file.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> odtfile = os.path.join('oommfodt', 'tests', 'test_sample', 'file1.odt')
    >>> columns = oo.columns(odtfile)
    >>> type(columns)
    <class 'list'>

    """
    with open(filename) as f:
        lines = f.readlines()

    columns = []
    for line in lines:
        if line.startswith('# Columns:'):
            line_split = re.split(r'Oxs_|Anv_|Southampton_', line)[1:]
            for column in line_split:
                column = re.sub(r'[{}\s]', '', column)
                if rename:
                    if column in column_dict.keys():
                        column = column_dict[column]
                    else:
                        column = column.split(':')[-1]
                columns.append(column)
            break

    return columns


def units(filename, rename=False):
    """Extract units for individual columns from an OOMMF `.odt` file.

    This function extracts the units for every column from an OOMMF
    `.odt` file and returns a dictionary.

    Parameters
    ----------
    filename : str
        Name of an OOMMF `.odt` file
    rename : bool
        Flag (the default is `True`). If `rename=True`, the column
        names are renamed with their shorter versions.

    Returns
    -------
    dict

    Examples
    --------
    1. Extracting units for individual columns from an OOMMF `.odt`
    file.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> odtfile = os.path.join('oommfodt', 'tests', 'test_sample', 'file2.odt')
    >>> units = oo.units(odtfile)
    >>> type(units)
    <class 'dict'>

    """
    with open(filename) as f:
        lines = f.readlines()

    units = []
    for line in lines:
        if line.startswith('# Units:'):
            units = line.split()[2:]
            units = [re.sub(r'[{}]', '', unit) for unit in units]
            break

    return dict(zip(columns(filename, rename=rename), units))


def data(filename):
    """Read numerical data from an OOMMF `.odt` file.

    This function reads data from an OOMMF `.odt` file and returns it
    as a list of floats.

    Parameters
    ----------
    filename : str
        Name of an OOMMF `.odt` file

    Returns
    -------
    list(float)

    Examples
    --------
    1. Reading data from an OOMMF `.odt` file.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> odtfile = os.path.join('oommfodt', 'tests', 'test_sample', 'file3.odt')
    >>> data = oo.data(odtfile)
    >>> type(data)
    <class 'list'>

    """
    with open(filename) as f:
        lines = f.readlines()

    values = []
    for line in lines:
        if not line.startswith("#"):
            values.append(map(float, line.split()))

    return values


def read(filename, rename=True):
    """Read an OOMMF `.odt` file and return it as `pandas.DataFrame`.

    This function reads column names and data from an OOMMF `.odt`
    file and returns a `pandas.DataFrame`. Because there is no
    appropriate way of adding metadata to the `pandas.DataFrame`,
    obtaining units from the `.odt` file is ignored. If `rename=True`,
    the column names will be renamed to their shorter versions.

    Parameters
    ----------
    filename : str
        Name of an OOMMF `.odt` file
    rename : bool
        Flag (the default is `True`). If `rename=True`, the column
        names are renamed with their shorter versions.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    1. Reading an OOMMF `.odt` file.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> odtfile = os.path.join('oommfodt', 'tests', 'test_sample', 'file1.odt')
    >>> df = oo.read(odtfile)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    """
    return pd.DataFrame(data(filename),
                        columns=columns(filename, rename=rename))


def merge(input_iterable, rename=True, mergetime=False):
    """Read multiple `.odt` files or multiple `pandas.DataFrame` and merge
    them into a single `pandas.DataFrame`.

    This function takes an iterable of OOMMF `.odt` files or `pandas.DataFrames`, merges them,
    and returns a single `pandas.DataFrame`. If there are non-matching
    columns, the missing values will be `NaN`. If `rename=True`, the
    column names will be renamed with their shorter versions.

    If `mergetime=True`, an additional column will be added to the
    resulting `pandas.DataFrame`. The column's name is `tm` and
    contains a successive array of time starting from 0. If there is
    no time column in one of the `.odt` files, no mergeing is allowed.

    Parameters
    ----------
    input_iterable : list(str), list(pandas.DataFrame)
        An iterable with `.odt` filenames or `pandas.DataFrames`.
    rename : bool
        Flag (the default is `True`). If `rename=True`, the column
        names are renamed with their shorter versions.
    mergetime : bool
        Flag (the default is `True`). If `mergetime=True`, a new `tm`
        column is added with successive values of time.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    1. Reading and merging `.odt` files.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> test_files_dirname = os.path.join('oommfodt', 'tests', 'test_sample')
    >>> odtfile1 = os.path.join(test_files_dirname, 'file4.odt')
    >>> odtfile2 = os.path.join(test_files_dirname, 'file5.odt')
    >>> odtfile3 = os.path.join(test_files_dirname, 'file6.odt')
    >>> df = oo.merge([odtfile1, odtfile2, odtfile3], mergetime=True)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    """
    if all(isinstance(i, str) for i in input_iterable):
        # .odt filenames are passed
        dfs = list(map(functools.partial(read, rename=True), input_iterable))

    if mergetime:
        if not all('t' in df.columns for df in dfs):
            raise ValueError('Some of the data tables are '
                             'missing the time column.')

        time_offset = 0
        retimed_dfs = []
        for df in dfs:
            df['tm'] = time_offset + df['t']
            time_offset += df['t'].iloc[-1]
            retimed_dfs.append(df)

        return pd.concat(retimed_dfs, ignore_index=True, sort=False)
    else:
        return pd.concat(dfs, ignore_index=True, sort=False)
