import re
import pandas as pd
import numpy as np

headers_dic = {'RungeKuttaEvolve:evolver:Totalenergy': 'E',
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
               'MinDriver::Iteration': 'iteration',
               'MinDriver::Stageiteration': 'stage_iteration',
               'MinDriver::Stage': 'stage',
               'MinDriver::mx': 'mx',
               'MinDriver::my': 'my',
               'MinDriver::mz': 'mz'}


def read(filename, replace_headers=True):
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

    # Extract the headers from the odt file.
    for i in range(len(lines)):
        if lines[i].startswith('# Columns:'):
            columns_line = i
            line = lines[i]
            parts = re.split('Oxs_|Anv_', line)[1:]
            headers = []
            for part in parts:
                tmp_string = part
                tmp_string = tmp_string.replace('{', '')
                tmp_string = tmp_string.replace('}', '')
                tmp_string = tmp_string.replace(' ', '')
                tmp_string = tmp_string.replace('\n', '')
                if (tmp_string in headers_dic.keys()) and replace_headers:
                    headers.append(headers_dic[tmp_string])
                else:
                    headers.append(tmp_string)

    # Extract units from the odt file.
    for i in range(len(lines)):
        if lines[i].startswith('# Units:'):
            units_line = i
            line = lines[i]
            parts = line.split()[1:]
            units = []
            for part in parts:
                units.append(part)

    # Extract the data from the odt file.
    data = []
    for i in range(columns_line, len(lines)):
        line = lines[i]
        if line[0] != '#':
            data_line = []
            numbers = line.split()
            for number in numbers:
                data_line.append(float(number))
            data.append(data_line)

    df = pd.DataFrame(data, columns=headers)
    df.units = units
    return df
