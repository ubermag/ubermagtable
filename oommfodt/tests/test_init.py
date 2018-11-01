import oommfodt as oo


def test_version():
    assert isinstance(oo.__version__, str)
    assert '.' in oo.__version__


def test_dependencies():
    assert isinstance(oo.__dependencies__, list)
    assert len(oo.__dependencies__) > 0
    
