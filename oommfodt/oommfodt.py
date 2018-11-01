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
    >>> odtfile = os.path.join('oommfodt', 'tests', 'test_odt_files', 'test_odt_file1.odt')
    >>> df = read(odtfile)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    """
    with open(filename) as f:
        lines = f.readlines()

    data = []
    for line in lines:
        if line.startswith('# Columns:'):
            columns = []
            line_split = re.split(r'Oxs_|Anv_|Southampton_', line)[1:]
            for column in line_split:
                column = re.sub(r'[{}\s]', '', column)
                if rename_columns:
                    if column in column_dict.keys():
                        column = column_dict[column]
                    else:
                        column = column.split(':')[-1]
                columns.append(column)
            
        if not line.startswith("#"):
            data.append(map(float, line.split()))

    return pd.DataFrame(data, columns=columns)


def merge(files):
    frames = [read(file) for file in files]
    return pd.concat(frames, ignore_index=True)
