import re
import pandas as pd
import numpy as np

header_dic = {'RungeKuttaEvolve:evolver:Totalenergy': 'E',
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


class OOMMFodt(object):

    """
    An instance of this class holds a Pandas DataFrame containing information
    from an OOMMF ODT file.

    Once initialised, the data can be accessed through the OOMMFodt.df
    attribute.
    """

    def __init__(self, odt_filename):
        """
        Opens an OOMMF ODT file and creates a Pandas DataFrame.

        Inputs:
        odt_filename, string:
            Filename of an OOMMF ODT File

        """
        # Open and read the lines of an odt file.
        f = open(odt_filename)
        lines = f.readlines()
        f.close()

        # Extract the header from the odt file.
        for i in range(len(lines)):
            if lines[i].startswith('# Columns:'):
                columns_line = i
                line = lines[i]
                parts = re.split('Oxs_|Anv_', line)[1:]
                print(parts)
                self.header = []
                for part in parts:
                    tmp_string = part
                    tmp_string = tmp_string.replace('{', '')
                    tmp_string = tmp_string.replace('}', '')
                    tmp_string = tmp_string.replace(' ', '')
                    tmp_string = tmp_string.replace('\n', '')
                    if tmp_string in header_dic.keys():
                        self.header.append(header_dic[tmp_string])
                    else:
                        self.header.append(tmp_string)

        # Extract units from the odt file.
        for i in range(len(lines)):
            if lines[i].startswith('# Units:'):
                units_line = i
                line = lines[i]
                parts = line.split()[1:]
                self.units = []
                for part in parts:
                    self.units.append(part)

        # Extract the data from the odt file.
        self.data = []
        for i in range(columns_line, len(lines)):
            line = lines[i]
            if line[0] != '#':
                data_line = []
                numbers = line.split()
                for number in numbers:
                    data_line.append(float(number))
                self.data.append(data_line)

        print(self.header)
        # Create pandas dataframe.
        self.df = pd.DataFrame(self.data, columns=self.header)

    def last_row(self):
        """
        last_row()

        Returns the data from the last row of the Pandas DataFrame.
        """
        return self.df.loc[self.df.index[-1]]

    def get_header_dictionary(self):
        """
        get_header_dictionary()

        Print the header dictionary.
        """
        return header_dic

    def times(self):
        """
        times()

        Return the stage times.
        """
        return self.df['t'].as_matrix()

    def save_excel(self, filename):
        """
        save_excel(filename)

        Saves the file to an excel file.
        Both *.xls and *.xlsx formats are supported.

        `filename` should end in `.xls` or `.xlsx` to decide on format.

        """
        self.df.to_excel(filename)
