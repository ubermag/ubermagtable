import re
import ubermagtable as ut


def test_version():
    assert isinstance(ut.__version__, str)
    assert re.search(r'^\d+.\d+.?\d*$', ut.__version__)


def test_dependencies():
    assert isinstance(ut.__dependencies__, list)
    assert len(ut.__dependencies__) > 0
