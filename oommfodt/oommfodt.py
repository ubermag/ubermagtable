import re
import pandas as pd
import numpy as np

columns_dic = {'RungeKuttaEvolve:evolver:Totalenergy': 'E',
               'RungeKuttaEvolve:evolver:Energycalccount': 'Ecount',
               'RungeKuttaEvolve:evolver:Maxdm/dt': 'max_dm/dt',
               'RungeKuttaEvolve:evolver:dE/dt': 'dE/dt',
               'RungeKuttaEvolve:evolver:DeltaE': 'deltaE',
               'UniformExchange::Energy': 'E_Exchange',
               'UniformExchange::MaxSpinAng': 'max_spin_angle',
               'UniformExchange::StageMaxSpinAng': 'stage_max_spin_angle',
               'UniformExchange::RunMaxSpinAng': 'run_max_spin_angle',
               'Demag::Energy': 'E_Demag',
               'FixedZeeman:fixedzeeman:Energy': 'E_Zeeman',
               'TimeDriver::Iteration': 'iteration',
               'TimeDriver::Stageiteration': 'stage_iteration',
               'TimeDriver::Stage': 'stage',
               'TimeDriver::mx': 'mx',
               'TimeDriver::my': 'my',
               'TimeDriver::mz': 'mz',
               'TimeDriver::Lasttimestep': 'last_time_step',
               'TimeDriver::Simulationtime': 't',
               'CGEvolve:evolver:MaxmxHxm': 'max_mxHxm',
               'CGEvolve:evolver:Totalenergy': 'E',
               'CGEvolve:evolver:DeltaE': 'delta_E',
               'CGEvolve:evolver:Bracketcount': 'bracket_count',
               'CGEvolve:evolver:Linemincount': 'line_min_count',
               'CGEvolve:evolver:Conjugatecyclecount': 'conjugate_cycle_count',
               'CGEvolve:evolver:Cyclecount': 'cycle_count',
               'CGEvolve:evolver:Cyclesubcount': 'cycle_sub_count',
               'CGEvolve:evolver:Energycalccount': 'energy_cal_count',
               'UniaxialAnisotropy::Energy': 'E_UniaxialAnisotropy',
               'Southampton_UniaxialAnisotropy4::Energy': 'E_UniaxialAnisotropy',
               'MinDriver::Iteration': 'iteration',
               'MinDriver::Stageiteration': 'stage_iteration',
               'MinDriver::Stage': 'stage',
               'MinDriver::mx': 'mx',
               'MinDriver::my': 'my',
               'MinDriver::mz': 'mz'}


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
                        columns.append(part)
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
    df.units = units
    return df
