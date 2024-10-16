import os

import pytest

import ubermagtable as ut


@pytest.mark.skip
def test_interact():
    dirname = os.path.join(os.path.dirname(__file__), "test_sample/")
    odtfile = os.path.join(dirname, "oommf-new-file2.odt")
    table = ut.Table.fromfile(odtfile, x="t")

    # Only test whether it runs.
    @ut.interact(xlim=table.slider())
    def myplot(xlim):
        table.mpl(xlim=xlim)
