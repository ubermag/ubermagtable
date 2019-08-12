import re
import functools
import pandas as pd

# The OOMMF columns are renamed according to this dictionary.
oommf_dict = {'RungeKuttaEvolve::Total energy': 'E',
              'RungeKuttaEvolve::Energy calc count': 'calc_count',
              'RungeKuttaEvolve::Max dm/dt': 'max_dm/dt',
              'RungeKuttaEvolve::dE/dt': 'dE/dt',
              'RungeKuttaEvolve::Delta E': 'delta_E',
              'UniformExchange::Max Spin Ang': 'max_spin_ang',
              'UniformExchange::Stage Max Spin Ang': 'stage_max_spin_ang',
              'UniformExchange::Run Max Spin Ang': 'run_max_spin_ang',
              'TimeDriver::Iteration': 'iteration',
              'TimeDriver::Stage iteration': 'stage_iteration',
              'TimeDriver::Stage': 'stage',
              'TimeDriver::mx': 'mx',
              'TimeDriver::my': 'my',
              'TimeDriver::mz': 'mz',
              'TimeDriver::Last time step': 'last_time_step',
              'TimeDriver::Simulation time': 't',
              'CGEvolve::Max mxHxm': 'max_mxHxm',
              'CGEvolve::Total energy': 'E',
              'CGEvolve::Delta E': 'delta_E',
              'CGEvolve::Bracket count': 'bracket_count',
              'CGEvolve::Line min count': 'line_min_count',
              'CGEvolve::Conjugate cycle count': 'conjugate_cycle_count',
              'CGEvolve::Cycle count': 'cycle_count',
              'CGEvolve::Cycle sub count': 'cycle_sub_count',
              'CGEvolve::Energy calc count': 'energy_calc_count',
              'MinDriver::Iteration': 'iteration',
              'MinDriver::Stage iteration': 'stage_iteration',
              'MinDriver::Stage': 'stage',
              'MinDriver::mx': 'mx',
              'MinDriver::my': 'my',
              'MinDriver::mz': 'mz',
              'UniformExchange::Energy': 'E_exchange',
              'DMExchange6Ngbr::Energy': 'E_dmi',
              'DMI_Cnv::Energy': 'E_dmi_cnv',
              'DMI_T::Energy': 'E_dmi_t',
              'DMI_D2d::Energy': 'E_dmi_d2d',
              'Demag::Energy': 'E_demag',
              'FixedZeeman::Energy': 'E_zeeman',
              'UZeeman::Energy': 'E_uzeeman',
              'UZeeman::B': 'B',
              'UZeeman::Bx': 'Bx',
              'UZeeman::By': 'By',
              'UZeeman::Bz': 'Bz',
              'CubicAnisotropy::Energy': 'E_cubicanisotropy',
              'SpinTEvolve::Total energy': 'E',
              'UniaxialAnisotropy::Energy': 'E_uniaxialanisotropy',
              'UniaxialAnisotropy4::Energy': 'E_uniaxialanisotropy4',
              'Southampton_UniaxialAnisotropy4::Energy':
              'E_uniaxialanisotropy'}

# The mumax3 columns are renamed according to this dictionary.
mumax_dict = {'t' : 't',
              'mx' : 'mx',
              'my' : 'my',
              'mz' : 'mz',
              'E_total': 'E',
              'E_exch' : 'E_totalexchange',
              'E_demag' : 'E_demag',
              'E_Zeeman': 'E_zeeman',
              'E_anis' : 'E_totalanisotropy',
              'dt' : 'dt',
              'maxTorque' : 'maxtorque'}

def columns(filename, rename=True):
    """Extract the names of columns from an OOMMF `.odt` or mumax3 `.txt`
    file.

    This function extracts the names of columns from an OOMMF `.odt`
    or a mumax3 `.txt` file and returns a list of strings. If
    `rename=True`, the columns will be renamed to shorter versions.

    Parameters
    ----------
    filename : str
        Name of an OOMMF `.odt` or a mumax3 `.txt` file
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
    >>> import ubermagtable as ut
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf_file1.odt')
    >>> columns = ut.columns(odtfile)
    >>> type(columns)
    <class 'list'>

    2. Extracting the names of columns from a mumax3 `.txt` file.

    >>> import os
    >>> import ubermagtable as ut
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'mumax_file1.txt')
    >>> columns = ut.columns(odtfile)
    >>> type(columns)
    <class 'list'>

    .. note::

           This function does not extract units for individual
           columns. For that `ubermagtable.units` should be used.

    """
    with open(filename) as f:
        lines = f.readlines()

    columns = []
    if lines[0].startswith('# ODT'):
        # OOMMF odt file
        columns_line = list(filter(lambda l: l.startswith('# Columns:'), lines))[0]
        columns_line = re.split(r'Oxs_|Anv_|Southampton_', columns_line)[1:]
        columns_line = list(map(lambda s: re.sub(r'[{}]', '', s), columns_line))
        columns_line = list(map(lambda s: s.strip(), columns_line))
        columns_dict = oommf_dict
    else:
        # mumax3 txt file
        columns_line = lines[0][2:].rstrip().split('\t')
        columns_line = list(map(lambda s: s.split(' ')[0], columns_line))
        columns_dict = mumax_dict

    columns = columns_line
    if rename:
        columns = [columns_dict[c] for c in columns]

    return columns


def units(filename, rename=True):
    """Extract units for individual columns from an OOMMF `.odt` or mumax3
    `.txt` file.

    This function extracts the units for every column from an OOMMF
    `.odt` or mumax3 `.txt` file and returns a dictionary.

    Parameters
    ----------
    filename : str
        Name of an OOMMF `.odt` or mumax3 `.txt` file
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
    >>> import ubermagtable as ut
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf_file2.odt')
    >>> units = ut.units(odtfile)
    >>> type(units)
    <class 'dict'>

    1. Extracting units for individual columns from a mumax3 `.txt`
    file.

    >>> import os
    >>> import ubermagtable as ut
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'mumax_file1.txt')
    >>> units = ut.units(odtfile)
    >>> type(units)
    <class 'dict'>

    """
    with open(filename) as f:
        lines = f.readlines()

    units = []
    if lines[0].startswith('# ODT'):
        # OOMMF odt file
        units_line = list(filter(lambda l: l.startswith('# Units:'), lines))[0]
        units = units_line.split()[2:]
        units = list(map(lambda s: re.sub(r'[{}]', '', s), units))
    else:
        # mumax3 txt file
        units_line = lines[0][2:].rstrip().split('\t')
        units = list(map(lambda s: s.split()[1], units_line))
        units = list(map(lambda s: re.sub(r'[()]', '', s), units))

    return dict(zip(columns(filename, rename=rename), units))


def data(filename):
    """Read numerical data from an OOMMF `.odt` or a mumax3 `.txt` file.

    This function reads data from an OOMMF `.odt` or a mumax3 `.txt`
    file and returns it as a list of floats.

    Parameters
    ----------
    filename : str
        Name of an OOMMF `.odt` or a mumax3 `.txt` file

    Returns
    -------
    list(float)

    Examples
    --------
    1. Reading data from an OOMMF `.odt` file.

    >>> import os
    >>> import ubermagtable as ut
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf_file3.odt')
    >>> data = ut.data(odtfile)
    >>> type(data)
    <class 'list'>

    2. Reading data from a mumax3 `.txt` file.

    >>> import os
    >>> import ubermagtable as ut
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'mumax_file1.txt')
    >>> data = ut.data(odtfile)
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


def read(filename, rename=True):
    """Read an OOMMF `.odt` or a mumax3 `.txt` file and return it as
    `pandas.DataFrame`.

    This function reads column names and data from an OOMMF `.odt` or
    a mumax3 `.txt` file and returns a `pandas.DataFrame`. Because
    there is no appropriate way of adding metadata to the
    `pandas.DataFrame`, obtaining units from the `.odt` file is
    ignored and can be extracted using `ubermagtable.units` function. If
    `rename=True`, the column names will be renamed to their shorter
    versions.

    Parameters
    ----------
    filename : str
        Name of an OOMMF `.odt` or a mumax3 `.txt` file
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
    >>> import ubermagtable as ut
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf_file1.odt')
    >>> df = ut.read(odtfile)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    2. Reading a mumax3 `.txt` file.

    >>> import os
    >>> import ubermagtable as oo
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'mumax_file1.txt')
    >>> df = ut.read(odtfile)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    .. note::

           For more information on how the names of columns are
           renamed, please see `ubermagtable.columns`.

    """
    return pd.DataFrame(data(filename),
                        columns=columns(filename, rename=rename))


def merge(input_iterable, rename=True, mergetime=False):
    """Read multiple OOMMF `.odt` or mumax3 `.txt` files or multiple
    `pandas.DataFrames` and merge them into a single
    `pandas.DataFrame`.

    This function takes an iterable of OOMMF `.odt` files, mumax3
    `.txt` files or `pandas.DataFrames`, merges them, and returns a
    single `pandas.DataFrame`. If there are non-matching columns, the
    missing values will be `NaN`. If `rename=True` and `.odt`
    filenames are passed, the column names will be renamed with their
    shorter versions.

    If `mergetime=True`, an additional column will be added to the
    resulting `pandas.DataFrame`. The column's name is `tm` and
    contains a successive array of time starting from 0. If there is
    no time column in one of the `.odt` files, no merging is allowed
    and `ValueError` is raised.

    Parameters
    ----------
    input_iterable : list(str), list(pandas.DataFrame)
        An iterable with OOMMF `.odt` or mumax3 `.txt` filenames or
        `pandas.DataFrames`.
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
    >>> import ubermagtable as ut
    ...
    >>> dirname = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample')
    >>> odtfile1 = os.path.join(dirname, 'oommf_file4.odt')
    >>> odtfile2 = os.path.join(dirname, 'oommf_file5.odt')
    >>> odtfile3 = os.path.join(dirname, 'oommf_file6.odt')
    >>> df = ut.merge([odtfile1, odtfile2, odtfile3], mergetime=True)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    .. note::

           For more information on how the names of columns are
           renamed, please see `ubermagtable.columns`.

    """
    if all(isinstance(element, str) for element in input_iterable):
        # .odt filenames are passed
        dfs = list(map(functools.partial(read, rename=rename),
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
