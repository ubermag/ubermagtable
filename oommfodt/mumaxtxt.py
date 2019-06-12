import re
import functools
import pandas as pd

def mumax_columns(filename, rename=True):
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
    ...                        'tests', 'test_sample', 'file1.odt')
    >>> columns = oo.columns(odtfile)
    >>> type(columns)
    <class 'list'>

    .. note::

           This function does not extract units for individual
           columns. For that `oommfodt.units` can be used.

    """
    with open(filename) as f:
        lines = f.readlines()

    columns = []
    splitted_line = lines[0][2:].rstrip().split("\t")
    for column in splitted_line:
        #print(re.sub(r'[(\w)]', '', column))
        columns.append(column.split(" ")[0])
        
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
    ...                        'tests', 'test_sample', 'file2.odt')
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


def mumax_data(filename):
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
    ...                        'tests', 'test_sample', 'file3.odt')
    >>> data = oo.data(odtfile)
    >>> type(data)
    <class 'list'>

    """
    with open(filename) as f:
        lines = f.readlines()

    values = []
    for line in lines:
        if not line.startswith("#"):
            values.append(list(map(float, line.rstrip().split("\t"))))

    return values

def mumax_read(filename, rename=True):
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
    ...                        'tests', 'test_sample', 'file1.odt')
    >>> df = oo.read(odtfile)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    .. note::

           For more information on how the names of columns are
           renamed, please see `oommfodt.columns`.

    """
    return pd.DataFrame(mumax_data(filename),
                        columns=mumax_columns(filename, rename=rename))

