import re
import pandas as pd
import numpy as np

columns_dic = {'RungeKuttaEvolve:evolver:Totalenergy': 'E',
               'RungeKuttaEvolve:evolver:Energycalccount': 'Ecount',
               'RungeKuttaEvolve:evolver:Maxdm/dt': 'max_dm/dt',
               'RungeKuttaEvolve:evolver:dE/dt': 'dE/dt',
               'RungeKuttaEvolve:evolver:DeltaE': 'deltaE',
               'UniformExchange::Energy': 'Eex',
               'UniformExchange::MaxSpinAng': 'max_spin_angle',
               'UniformExchange::StageMaxSpinAng': 'stage_max_spin_angle',
               'UniformExchange::RunMaxSpinAng': 'run_max_spin_angle',
               'Demag::Energy': 'Ed',
               'FixedZeeman:fixedzeeman:Energy': 'Ez',
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
               'UniaxialAnisotropy::Energy': 'Ea',
               'Southampton_UniaxialAnisotropy4::Energy': 'Ea',
               'MinDriver::Iteration': 'iteration',
               'MinDriver::Stageiteration': 'stage_iteration',
               'MinDriver::Stage': 'stage',
               'MinDriver::mx': 'mx',
               'MinDriver::my': 'my',
               'MinDriver::mz': 'mz'}


def read(filename, replace_columns=True):
    """
    Opens an OOMMF odt file and returns a Pandas DataFrame.

    Parameters
    ----------
    filename : str
        Filename of an OOMMF odt File

    Returns
    -------
    pandas dataframe

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
            odt_section = i
            for part in re.split('Oxs_|Anv_|Southampton_', line)[1:]:
                column = part
                for char in ["{", "}", " ", "\n"]:
                    column = column.replace(char, '')

                if column in columns_dic.keys() and replace_columns:
                    columns.append(columns_dic[column])
                else:
                    columns.append(column)

    # Extract units from the odt file.
    for i, line in enumerate(lines):
        if line.startswith('# Units:'):
            units = line.split()[1:]

    # Extract the data from the odt file.
    data = []
    for i, line in enumerate(lines[odt_section:]):
        if not line.startswith("#"):
            data.append([float(number) for number in line.split()])

    df = pd.DataFrame(data, columns=columns)
    df.units = units
    return df
