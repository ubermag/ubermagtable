import ipywidgets


def interact(**kwargs):
    """Decorator for interactive plotting. This is a wrapper around
    ``ipywidgets.interact``. For details, please refer to ``interact`` function
    in ``ipywidgets`` package.

    Example
    -------
    1. Interactive plotting.

    >>> import ubermagtable as ut
    >>> table = ut.sample_data()
    >>> @ut.interact(xlim=table.slider())  # doctest: +SKIP
    ... def myplot(xlim):
    ...     field.mpl(xlim=xlim)
    interactive(...)

    """
    return ipywidgets.interact(**kwargs)
