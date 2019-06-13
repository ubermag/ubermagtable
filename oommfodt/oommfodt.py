import re
import functools
import pandas as pd

# When the column name is shortened, it is renamed with the portion of
# the string after the last `:` character. If a different name is
# required, it should be added to this dictionary.
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


def oommf_columns(filename, rename=True):
    """Extract the names of columns from an OOMMF `.odt` file.

    This function extracts the names of columns from an OOMMF `.odt`
    file and returns a list of strings. If `rename=True`, the columns
    will be renamed to shorter versions.

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
    1. Extracting the names of columns from an OOMMF `.odt` file.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf_samples', 'file1.odt')
    >>> columns = oo.oommf_columns(odtfile)
    >>> type(columns)
    <class 'list'>

    .. note::

           This function does not extract units for individual
           columns. For that `oommfodt.units` can be used.

    """
    with open(filename) as f:
        lines = f.readlines()

    columns = []
    for line in lines:
        if line.startswith('# Columns:'):
            splitted_line = re.split(r'Oxs_|Anv_|Southampton_', line)[1:]
            for column in splitted_line:
                column = re.sub(r'[{}\s]', '', column)
                if rename:
                    if column in column_dict.keys():
                        column = column_dict[column]
                    else:
                        column = column.split(':')[-1]
                columns.append(column)
            break

    return columns


def units(filename, rename=True):
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
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf_samples', 'file2.odt')
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

    return dict(zip(oommf_columns(filename, rename=rename), units))


def oommf_data(filename):
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
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf_samples', 'file3.odt')
    >>> data = oo.oommf_data(odtfile)
    >>> type(data)
    <class 'list'>

    """
    with open(filename) as f:
        lines = f.readlines()

    values = []
    for line in lines:
        if not line.startswith("#"):
            values.append(list(map(float, line.split())))

    return values


def oommf_read(filename, rename=True):
    """Read an OOMMF `.odt` file and return it as `pandas.DataFrame`.

    This function reads column names and data from an OOMMF `.odt`
    file and returns a `pandas.DataFrame`. Because there is no
    appropriate way of adding metadata to the `pandas.DataFrame`,
    obtaining units from the `.odt` file is ignored and can be
    extracted using `oommfodt.units` function. If `rename=True`, the
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
    pandas.DataFrame

    Examples
    --------
    1. Reading an OOMMF `.odt` file.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf_samples', 'file1.odt')
    >>> df = oo.oommf_read(odtfile)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    .. note::

           For more information on how the names of columns are
           renamed, please see `oommfodt.columns`.

    """
    return pd.DataFrame(oommf_data(filename),
                        columns=oommf_columns(filename, rename=rename))


def merge(input_iterable, rename=True, mergetime=False):
    """Read multiple `.odt` files or multiple `pandas.DataFrames` and
    merge them into a single `pandas.DataFrame`.

    This function takes an iterable of OOMMF `.odt` files or
    `pandas.DataFrames`, merges them, and returns a single
    `pandas.DataFrame`. If there are non-matching columns, the missing
    values will be `NaN`. If `rename=True` and `.odt` filenames are
    passed, the column names will be renamed with their shorter
    versions.

    If `mergetime=True`, an additional column will be added to the
    resulting `pandas.DataFrame`. The column's name is `tm` and
    contains a successive array of time starting from 0. If there is
    no time column in one of the `.odt` files, no merging is allowed
    and `ValueError` is raised.

    Parameters
    ----------
    input_iterable : list(str), list(pandas.DataFrame)
        An iterable with `.odt` filenames or `pandas.DataFrames`.
    rename : bool
        Flag (the default is `True`). If `rename=True`, the column
        names are renamed with their shorter versions.
    mergetime : bool
        Flag (the default is `True`). If `mergetime=True`, a new `tm`
        column is added with successive values of time to the
        resulting `pandas.dataFrame`.

    Returns
    -------
    pandas.DataFrame

    Raises
    ------
    ValueError
        If `mergetime=True` and one of the passed `pandas.DataFrames`
        is missing `t` column.

    Examples
    --------
    1. Reading and merging `.odt` files.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> dirname = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf_samples')
    >>> odtfile1 = os.path.join(dirname, 'file4.odt')
    >>> odtfile2 = os.path.join(dirname, 'file5.odt')
    >>> odtfile3 = os.path.join(dirname, 'file6.odt')
    >>> df = oo.merge([odtfile1, odtfile2, odtfile3], mergetime=True)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    .. note::

           For more information on how the names of columns are
           renamed, please see `oommfodt.columns`.

    """
    if all(isinstance(element, str) for element in input_iterable):
        # .odt filenames are passed
        dfs = list(map(functools.partial(oommf_read, rename=rename),
                       input_iterable))
    else:
        # pandas.DataFrames are passed
        dfs = list(input_iterable)

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
        dfs = retimed_dfs

    return pd.concat(dfs, ignore_index=True, sort=False)
