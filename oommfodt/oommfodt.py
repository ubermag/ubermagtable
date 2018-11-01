import re
import pandas as pd
import numpy as np


columns_dic = {'RungeKuttaEvolve:evolver:Totalenergy': 'E',
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


def rename(column):
    if column in column_dict:
        return column_dict[column]
    else:
        return column.split(':')[-1]


def read(filename, replace_columns=True):
    """Read an OOMMF odt file and return pandas DataFrame.

    Parameters
    ----------
    filename : str
        Name/path of an OOMMF odt file
    replace_columns : bool
        Flag (the default is True) if column names should be replaced
        with their shorter versions.

    Returns
    -------
    pandas DataFrame

    Examples
    --------
    Reading simple odt file.

    >>> import oommfodt

    """
    f = open(filename)
    lines = f.readlines()
    f.close()

    # Extract column names from the odt file.
    for i, line in enumerate(lines):
        if line.startswith('# Columns:'):
            columns = []
            odt_section = i  # Should be removed after runs are split.
            for part in re.split('Oxs_|Anv_|Southampton_', line)[1:]:
                for char in ["{", "}", " ", "\n"]:
                    part = part.replace(char, '')
                if replace_columns:
                    if part in columns_dic.keys():
                        columns.append(columns_dic[part])
                    else:
                        msg = "Entry {} not in lookup table.".format(part)
                        raise ValueError(msg)
                else:
                    columns.append(part)

    # Extract units from the odt file.
    for i, line in enumerate(lines):
        if line.startswith('# Units:'):
            units = line.split()[2:]

    # Extract the data from the odt file.
    data = []
    for i, line in enumerate(lines[odt_section:]):
        if not line.startswith("#"):
            data.append([float(number) for number in line.split()])

    df = pd.DataFrame(data, columns=columns)
    # next line is required to allow adding list-like attribute to pandas DataFrame
    # see https://github.com/pandas-dev/pandas/blob/2f9d4fbc7f289a48ed8b29f573675cd2e21b2c89/pandas/core/generic.py#L3631
    df._metadata.append('units')
    df.units = dict(zip(columns, units))
    return df


def merge(files):

    frames = [read(file) for file in files]
    return pd.concat(frames, ignore_index=True)
