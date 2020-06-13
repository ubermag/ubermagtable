import os
import numbers
import itertools
import ubermagtable.util as uu


dirname = os.path.join(os.path.dirname(__file__), 'test_sample/')
filenames = ['oommf-file1.odt',
             'oommf-file2.odt',
             'oommf-file3.odt',
             'oommf-file4.odt',
             'oommf-file5.odt',
             'oommf-file6.odt',
             'oommf-file7.odt',
             'oommf-file8.odt',
             'mumax3-file1.txt',
             'oommf-mel-file.odt']
odtfiles = [os.path.join(dirname, f) for f in filenames]


def test_columns():
    for odtfile in odtfiles:
        for rename in [True, False]:
            columns = uu.columns(odtfile, rename=rename)

            assert isinstance(columns, list)
            assert all(isinstance(column, str) for column in columns)


def test_units():
    for odtfile in odtfiles:
        for rename in [True, False]:
            units = uu.units(odtfile, rename=rename)

            assert isinstance(units, dict)
            assert all(isinstance(unit, str) for unit in units.keys())
            assert all(isinstance(unit, str) for unit in units.values())
            assert 'J' in units.values()  # Energy is always in
            assert '' in units.values()  # Columns with no units are always in


def test_data():
    for odtfile in odtfiles:
        data = uu.data(odtfile)

        assert isinstance(data, list)
        assert all(isinstance(i, numbers.Real) for i in itertools.chain(*data))
