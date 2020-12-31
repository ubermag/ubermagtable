import ipywidgets


def interact(**kwargs):
    """Decorator for interactive plotting. This is a wrapper around
    ``ipywidgets.interact``. For details, please refer to ``interact`` function
    in ``ipywidgets`` package.

    Example
    -------
    1. Interactive plotting.

    >>> import os
    >>> import ubermagtable as ut
    ...
    >>> dirname = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample')
    >>> odtfile = os.path.join(dirname, 'oommf-old-file1.odt')
    ...
    >>> table = ut.Table.fromfile(odtfile, x='t')
    >>> @ut.interact(xlim=table.slider())
    ... def myplot(xlim):
    ...     field.mpl(xlim=xlim)
    interactive(...)

    """
    return ipywidgets.interact(**kwargs)
