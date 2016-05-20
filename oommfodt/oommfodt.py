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
              'TimeDriver::Simulationtime': 't'}


class OOMMFodt(object):
    def __init__(self, odt_filename):
        """Opens the oommf odt file and creates a pandas dataframe."""
        # Open and read the lines of an odt file.
        f = open(odt_filename)
        lines = f.readlines()
        f.close()

        # Extract the header from the odt file.
        for i in range(len(lines)):
            if lines[i].startswith('# Columns:'):
                columns_line = i
                line = lines[i]
                parts = line.split('Oxs_')[1:]
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

        # Create pandas dataframe.
        self.df = pd.DataFrame(self.data, columns=self.header)

    def last_row(self):
        """Return the data from the last row of pandas dataframe."""
        return self.df.loc[self.df.index[-1]]

    def get_header_dictionary(self):
        """Print the header dictionary."""
        return header_dic

    def times(self):
        """Return the stage times."""
        return self.df['t'].as_matrix()
