import os
import pandas as pd
import numpy as np
from oommfodt import OOMMFodt

test_file = os.path.join(os.path.dirname(__file__), 'test_odt_file.odt')


class TestOOMMFodt(object):
    def setup(self):
        self.odt = OOMMFodt(test_file)

    def test_init(self):
        assert isinstance(self.odt.df, pd.DataFrame)
    
    def test_header(self):
        assert isinstance(self.odt.header, list)

        assert len(self.odt.header) == 19

        for i in self.odt.header:
            assert isinstance(i, str)

        assert 'E' in self.odt.header
        assert 'Ecount' in self.odt.header
        assert 'max_dm/dt' in self.odt.header
        assert 'dE/dt' in self.odt.header
        assert 'deltaE' in self.odt.header
        assert 'Eex' in self.odt.header
        assert 'max_spin_angle' in self.odt.header
        assert 'stage_max_spin_angle' in self.odt.header
        assert 'run_max_spin_angle' in self.odt.header
        assert 'Ed' in self.odt.header
        assert 'Ez' in self.odt.header
        assert 'iteration' in self.odt.header
        assert 'stage' in self.odt.header
        assert 'mx' in self.odt.header
        assert 'my' in self.odt.header
        assert 'mz' in self.odt.header
        assert 'last_time_step' in self.odt.header
        assert 't' in self.odt.header

    def test_units(self):
        assert isinstance(self.odt.units, list)
        assert len(self.odt.header) == 19

        for i in self.odt.units:
            assert isinstance(i, str)

        assert 'J' in self.odt.units
        assert '{}' in self.odt.units
        assert 'deg/ns' in self.odt.units

    def test_number_of_rows(self):
        assert len(self.odt.df['E'].as_matrix()) == 200

    def test_data(self):
        assert self.odt.df.as_matrix().shape == (200, 19)

    def test_time(self):
        dt = 5e-12
        T = 1e-9
        tol = 1e-20
        t_array = self.odt.times()
        assert len(t_array) == 200
        assert abs(t_array.min() - dt) < tol
        assert abs(t_array.max() - T) < tol
        assert t_array.min() == t_array[0]
        assert t_array.max() == t_array[-1]
        assert np.all(np.sort(t_array) == t_array)

    def test_last_row(self):
        lr = self.odt.last_row()
        assert lr[0] == -2.7155372712318564e-18
        assert lr[1] == 3878
        assert lr[2] == 1197.6227323394278
        assert lr[3] == -1.9370522259265568e-09
        assert lr[4] == -2.692767808494078e-21
        assert lr[5] == 7.1471885127248497e-20
        assert lr[6] == 4.3950299455634969
        assert lr[7] == 4.7098633974834705
        assert lr[8] == 29.981558387992568
        assert lr[9] == 9.2894784173044561e-19
        assert lr[10] == -3.7159569980895502e-18
        assert lr[11] == 812
        assert lr[12] == 3
        assert lr[13] == 199
        assert lr[14] == -0.98403391909751314 
        assert lr[15] == 0.13158424282201089
        assert lr[16] == 0.042795161919992566
        assert lr[17] == 1.3747680147350528e-12
        assert lr[18] == 9.9999999999999903e-10
        
        assert len(lr) == 19

    def test_header_dictionary(self):
        dic = self.odt.get_header_dictionary()
        assert isinstance(dic, dict)
        assert len(dic.keys()) == 35

    def test_can_write_xls(self):
        import numpy as np
        
        # write xlsx
        self.odt.save_excel('tmp.xlsx')

        # read file back and check shape is identical
        df = pd.read_excel('tmp.xlsx')
        assert df.shape == (200, 19)
        
        # compare data with source
        assert np.allclose(np.array(df), np.array(self.odt.df))

        # write xls
        self.odt.save_excel('tmp.xls')
        # read file back and check shape is identical
        df2 = pd.read_excel('tmp.xls')
        assert df2.shape == (200, 19)
        
        # compare data with source
        assert np.allclose(np.array(df2), np.array(self.odt.df))

        # Note: we could compare the data frame directly instead of comparing numpy arrays:
        # assert (df == self.odt.df).all().all()
        # Interestingly, this passes at the interactive prompt, but not when run in the test.
        # In the test, there appear to be small floating point deviations between the
        # saved xlsx / xls file and the data frame we started from.
        #
        # HF, 5 Aug 2016, pandas 0.18.1
        
        
        
        
