import pytest
import pkg_resources
from .ubermagtable import columns, units, data, read, merge


def test():
    return pytest.main(["-v", "--pyargs", "ubermagtable"])  # pragma: no cover


__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)
