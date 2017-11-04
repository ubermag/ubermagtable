from .oommfodt import read


def test():
    import pytest  # pragma: no cover
    return pytest.main(["-v", "--pyargs", "oommfodt"])  # pragma: no cover
