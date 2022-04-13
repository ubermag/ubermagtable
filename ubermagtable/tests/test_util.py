import itertools
import numbers
import os

import ubermagtable.util as uu

dirname = os.path.join(os.path.dirname(__file__), "test_sample/")
filenames = [
    "oommf-old-file1.odt",
    "oommf-old-file2.odt",
    "oommf-old-file3.odt",
    "oommf-old-file4.odt",
    "oommf-old-file5.odt",
    "oommf-old-file6.odt",
    "oommf-old-file7.odt",
    "oommf-old-file8.odt",
    "oommf-new-file1.odt",
    "oommf-new-file2.odt",
    "oommf-new-file3.odt",
    "oommf-new-file4.odt",
    "oommf-new-file5.odt",
    "mumax3-file1.txt",
    "oommf-mel-file.odt",
]
odtfiles = [os.path.join(dirname, f) for f in filenames]


def test_columns():
    for odtfile in odtfiles:
        for rename in [True, False]:
            columns = uu.columns(odtfile, rename=rename)

            assert isinstance(columns, list)
            assert all(isinstance(column, str) for column in columns)
            assert len(columns) == len(set(columns))  # unique column names


def test_units():
    for odtfile in odtfiles:
        for rename in [True, False]:
            units = uu.units(odtfile, rename=rename)

            assert isinstance(units, dict)
            assert all(isinstance(unit, str) for unit in units.keys())
            assert all(isinstance(unit, str) for unit in units.values())
            assert "J" in units.values()  # Energy is always in
            assert "" in units.values()  # Columns with no units are always in


def test_data():
    for odtfile in odtfiles:
        data = uu.data(odtfile)

        assert isinstance(data, list)
        assert all(isinstance(i, numbers.Real) for i in itertools.chain(*data))
