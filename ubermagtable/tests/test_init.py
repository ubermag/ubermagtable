import re

import ubermagtable as ut


def test_version():
    assert isinstance(ut.__version__, str)
    assert re.search(r"^\d+.\d+.?\d*$", ut.__version__)
