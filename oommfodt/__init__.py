import pytest
import pkg_resources
from .oommfodt import oommf_columns, units, oommf_data, oommf_read, merge
from .mumaxtxt import mumax_columns, mumax_data, mumax_read


def test():
    return pytest.main(["-v", "--pyargs", "oommfodt"])  # pragma: no cover


__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)
