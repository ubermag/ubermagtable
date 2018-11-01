import re
import pandas as pd

column_dict = {'RungeKuttaEvolve:evolver:Totalenergy': 'E',
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


def columns(filename, rename_columns=True):
    """Read column names from an OOMMF .odt file.

    This function extracts the names of columns from an OOMMF .odt
    file and returns it as a list of strings. If rename_columns=True,
    the column names will be renamed to their shorter versions.

    Parameters
    ----------
    filename : str
        Name of an OOMMF .odt file
    rename_columns : bool
        Flag (the default is True) if column names should be renamed
        with their shorter versions.

    Returns
    -------
    list(str)

    Examples
    --------
    Extracting names of columns from an .odt file.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> odtfile = os.path.join('oommfodt', 'tests', 'test_files', 'odt-file1.odt')
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
                if rename_columns:
                    if column in column_dict.keys():
                        column = column_dict[column]
                    else:
                        column = column.split(':')[-1]
                columns.append(column)
            break

    return columns


def units(filename):
    """Read units from an OOMMF .odt file.

    This function extracts the units from an OOMMF .odt file and
    returns it as a list of strings.

    Parameters
    ----------
    filename : str
        Name of an OOMMF .odt file

    Returns
    -------
    list(str)

    Examples
    --------
    Extracting units from an .odt file.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> odtfile = os.path.join('oommfodt', 'tests', 'test_files', 'odt-file2.odt')
    >>> units = oo.units(odtfile)
    >>> type(units)
    <class 'list'>

    """
    with open(filename) as f:
        lines = f.readlines()

    units = []
    for line in lines:
        if line.startswith('# Units:'):
            units = line.split()[2:]
            break

    return units


def data(filename):
    """Read data from an OOMMF .odt file.

    This function reads data from an OOMMF .odt file and returns it as
    a list of floats.

    Parameters
    ----------
    filename : str
        Name of an OOMMF .odt file

    Returns
    -------
    list(float)

    Examples
    --------
    Reading data from an .odt file.

    >>> import os
    >>> import oommfodt as oo
    ...
    >>> odtfile = os.path.join('oommfodt', 'tests', 'test_files', 'odt-file3.odt')
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


def read(filename, rename_columns=True):
    """Read an .odt file and convert it into pandas.DataFrame.

    This function is going to read column names and data from an OOMMF
    .odt file and return a pandas.DataFrame. Because there is no
    appropriate way of adding metadata to the pandas.DataFrame,
    obtaining units from the .odt file is ignored at the moment. If
    rename_columns=True, the column names will be renamed to their
    shorter versions.

    Parameters
    ----------
    filename : str
        Name of an OOMMF .odt file
    rename_columns : bool
        Flag (the default is True) if column names should be renamed
        with their shorter versions.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    Reading simple odt file.

    >>> import os
    >>> import oommfodt
    ...
    >>> odtfile = os.path.join('oommfodt', 'tests', 'test_files', 'odt-file1.odt')
    >>> df = read(odtfile)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    """
    return pd.DataFrame(data(filename),
                        columns=columns(filename, rename_columns=rename_columns))


def merge(files):
    frames = [read(file) for file in files]
    return pd.concat(frames, ignore_index=True)
