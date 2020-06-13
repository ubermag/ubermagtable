import ipywidgets
import ubermagutil.units
import numpy as np
import pandas as pd
import ubermagtable.util as uu
import matplotlib.pyplot as plt
import ubermagutil.typesystem as ts


@ts.typesystem(data=ts.Typed(expected_type=pd.DataFrame),
               units=ts.Typed(expected_type=dict))
class Table:
    """Scalar data table.

    This class builds some functionality around `pandas.DataFrame` to make it
    convenient for the analysis and visualisation of time-dependent scalar
    data. It takes `pandas.DataFrame` and a units dictionary as input
    arguments. However, its recommended usage is via
    ``ubermagtable.Table.fromfile`` class method which takes an OOMMF ``.odt``
    or a mumax3 ``.txt`` file and converts it to ``pandas.DataFrame``.

    ``pandas.DataFrame`` object can be exposed using ``data`` argument.
    Dictionary mapping units to columns is stored in ``units`` attribute.

    Parameters
    ----------
    data : pandas.DataFrame

        DataFrame with scalar data.

    units : dict

        Dictionary mapping units to columns.

    Examples
    --------
    1. Defining ``ubermagtable.Table`` by reading an OOMMF ``.odt`` file.

    >>> import os
    >>> import ubermagtable as ut
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf-file1.odt')
    >>> table = ut.Table.fromfile(odtfile)

    """
    def __init__(self, data, units):
        self.data = data
        self.units = units

    @classmethod
    def fromfile(cls, filename, rename=True):
        """Reads an OOMMF ``.odt`` or mumax3 ``.txt`` scalar data file and
        returns a ``ubermagtable.Table`` object.

        Parameters
        ----------
        filename : str

            OOMMF ``.odt`` or mumax3 ``.txt`` file.

        rename : bool

            If ``rename=True``, the column names are renamed with their shorter
            versions. Defaults to ``True``.

        Returns
        -------
        ubermagtable.Table

            Table data object.

        Examples
        --------
        1. Defining ``ubermagtable.Table`` by reading an OOMMF ``.odt`` file.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample', 'oommf-file1.odt')
        >>> table = ut.Table.fromfile(odtfile)

        2. Defining ``ubermagtable.Table`` by reading a mumax3 ``.txt`` file.

        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample', 'mumax3-file1.txt')
        >>> table = ut.Table.fromfile(odtfile)

        """
        # MagnetoElastic OOMMF extension adds energy twice to data. The
        # following lines are just a way to fix that in the data.
        cols = uu.columns(filename, rename=rename)
        if 'MEL_E' in cols:
            cols.insert(cols.index('E'), 'E')

        return cls(data=pd.DataFrame(uu.data(filename), columns=cols),
                   units=uu.units(filename, rename=rename))

    @property
    def data_columns(self):
        """Data column names.

        This property returns all data column names. Data columns are
        considered to be those that are a function of time.

        Returns
        -------
        list

            Data column names.

        Examples
        --------
        1. Getting data columns.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample', 'oommf-file5.odt')
        >>> table = ut.Table.fromfile(odtfile)
        >>> table.data_columns
        [...]

        """
        return [col for col in self.data.columns
                if (col != 't' and 'Simulation time' not in col)]

    @property
    def time_column(self):
        """Time column name.

        This property returns the name of the column where time data is stored.
        If no time column is present in the data, ``None`` is returned.

        Returns
        -------
        str

            Time column name.

        Examples
        --------
        1. Getting time column name.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample', 'oommf-file5.odt')
        >>> table = ut.Table.fromfile(odtfile)
        >>> table.time_column
        't'

        """
        time_columns = ['t', 'TimeDriver::Simulation time']
        for name in time_columns:
            if name in self.data.columns:
                return name
        else:
            return None

    @property
    def length(self):
        """Time length.

        This method returns the time length over which the scalar data was
        recorded.

        Returns
        -------
        numbers.Real

            Time length.

        Examples
        --------
        1. Getting time length.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample', 'oommf-file1.odt')
        >>> table = ut.Table.fromfile(odtfile)
        >>> table.length / 1e-12  # get the results in picoseconds
        24.999...

        """
        if self.time_column is None:
            msg = 'Cannot compute length for a table with no time column.'
            raise ValueError(msg)

        return self.data[self.time_column].iloc[-1]

    def __repr__(self):
        """Representation string.

        Returns
        -------
        str

            Representation string.

        Example
        -------
        1. Getting representation string.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample', 'oommf-file3.odt')
        >>> table = ut.Table.fromfile(odtfile)
        >>> repr(table)
        '...

        """
        return repr(self.data)

    def __lshift__(self, other):
        """Merges two tables into a single one.

        Tables are merged in such a way that the second operand data is
        concatenated to the first operand's data. Because time is unique and
        always successive, the time length of the first operand is added to the
        time column of the second. If there is no time column in any of the
        ``.odt`` files, no merging is allowed and ``ValueError`` is raised. If
        there are non-matching columns, the missing values will be ``NaN``.

        Parameters
        ----------
        other : ubermagtable.Table

            Second operand.

        Returns
        -------
        ubermagtable.Table

            Merged table.

        Raises
        ------
        ValueError

            If one of the tables does not have time column.

        Examples
        --------
        1. Merging two tables.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> dirname = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample')
        >>> odtfile1 = os.path.join(dirname, 'oommf-file1.odt')
        >>> odtfile2 = os.path.join(dirname, 'oommf-file2.odt')
        ...
        >>> table1 = ut.Table.fromfile(odtfile1)
        >>> table2 = ut.Table.fromfile(odtfile2)
        >>> merged_table = table1 << table2
        ...
        >>> table1.length / 1e-12  # in picoseconds
        24.999...
        >>> table2.length / 1e-12  # in picoseconds
        15.0
        >>> merged_table.length / 1e-12  # in picoseconds
        39.99...

        """
        if not isinstance(other, self.__class__):
            msg = (f'Unsupported operand type(s) for <<: '
                   f'{type(self)} and {type(other)}.')
            raise TypeError(msg)

        if self.time_column is None or other.time_column is None:
            msg = 'Some of the tables are missing the time column.'
            raise ValueError(msg)

        other_df = other.data.copy()  # make a deep copy of dataframe
        other_df[self.time_column] += self.data[self.time_column].iloc[-1]

        return self.__class__(data=pd.concat([self.data, other_df],
                                             ignore_index=True),
                              units=self.units)

    def mpl(self, ax=None, figsize=None, yaxis=None, xlim=None,
            multiplier=None, filename=None, **kwargs):
        """Table data plot.

        This method plots the scalar values as a function of time. ``mpl`` adds
        the plot to ``matplotlib.axes.Axes`` passed via ``ax`` argument. If
        ``ax`` is not passed, ``matplotlib.axes.Axes`` object is created
        automatically and the size of a figure can be specified using
        ``figsize``. To choose particular data columns to be plotted ``yaxis``
        can be passed as a list of column names. The range of ``t`` values on
        the horizontal axis can be defined by passing a lenth-2 tuple using
        ``xlim``. It is often the case that the time length is small (e.g. on a
        nanosecond scale). Accordingly, ``multiplier`` can be passed as
        :math:`10^{n}`, where :math:`n` is a multiple of 3  (..., -6, -3, 0, 3,
        6,...). According to that value, the horizontal axis will be scaled and
        appropriate units shown. For instance, if ``multiplier=1e-9`` is
        passed, the horizontal axis will be divided by :math:`1\\,\\text{ns}`
        and :math:`\\text{ns}` units will be used as axis labels. If
        ``multiplier`` is not passed, the best one is calculated internally.
        The plot can be saved as a PDF when ``filename`` is passed. This method
        plots the data using ``matplotlib.pyplot.plot()`` function, so any
        keyword arguments accepted by it can be passed.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional

            Axes to which the field plot is added. Defaults to ``None`` - axes
            are created internally.

        figsize : tuple, optional

            The size of a created figure if ``ax`` is not passed. Defaults to
            ``None``.

        yaxis : list, optional

            A list of data columns to be plotted.

        xlim : tuple

            A length-2 tuple setting the limits of the horizontal axis.

        multiplier : numbers.Real, optional

            Time axis multiplier.

        filename : str, optional

            If filename is passed, the plot is saved. Defaults to ``None``.

        Examples
        --------
        1. Visualising time-dependent data.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample', 'oommf-file1.odt')
        >>> table = ut.Table.fromfile(odtfile)
        >>> table.mpl()

        """
        if self.time_column is None:
            msg = 'Cannot plot table data with no time column.'
            raise ValueError(msg)

        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        if multiplier is None:
            multiplier = ubermagutil.units.si_multiplier(self.length)

        if yaxis is None:
            yaxis = self.data_columns

        for i in yaxis:
            ax.plot(np.divide(self.data[self.time_column].to_numpy(),
                              multiplier),
                    self.data[i],
                    label=i,
                    **kwargs)

        ax.set_xlabel(f't ({ubermagutil.units.rsi_prefixes[multiplier]}s)')
        ax.set_ylabel('value')

        ax.grid(True)  # grid is turned off by default for field plots
        ax.legend()

        if xlim is not None:
            plt.xlim(*np.divide(xlim, multiplier))

        if filename is not None:
            plt.savefig(filename, bbox_inches='tight', pad_inches=0)

    def slider(self, multiplier=None, description=None, **kwargs):
        """Slider for interactive plotting.

        Based on the values in the time column,
        ``ipywidgets.SelectionRangeSlider`` is returned for navigating
        interactive plots. This method is based on
        ``ipywidgets.SelectionRangeSlider``, so any keyword argument accepted
        by it can be passed.

        Parameters
        ----------
        multiplier : numbers.Real, optional

            ``multiplier`` can be passed as :math:`10^{n}`, where :math:`n` is
            a multiple of 3 (..., -6, -3, 0, 3, 6,...). According to that
            value, the values will be scaled and appropriate units shown. For
            instance, if ``multiplier=1e-9`` is passed, the slider points will
            be divided by :math:`1\\,\\text{ns}` and :math:`\\text{ns}` units
            will be used in the description. If ``multiplier`` is not passed,
            the optimum one is computed internally. Defaults to ``None``.

        description : str

            Slider description. Defaults to ``None``.

        Returns
        -------
        ipywidgets.SelectionRangeSlider

            Time range slider.

        Example
        -------
        1. Get the slider for the horizontal axis.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample', 'oommf-file1.odt')
        >>> table = ut.Table.fromfile(odtfile)
        >>> table.slider()
        SelectionRangeSlider(...)

        """
        if self.time_column is None:
            msg = 'Cannot create slider if no time is present in data.'
            raise ValueError(msg)

        if multiplier is None:
            multiplier = ubermagutil.units.si_multiplier(self.length)

        values = self.data[self.time_column].to_numpy()
        labels = np.around(values/multiplier, decimals=2)
        options = list(zip(labels, values))
        if description is None:
            description = f't ({ubermagutil.units.rsi_prefixes[multiplier]}s):'

        return ipywidgets.SelectionRangeSlider(options=options,
                                               value=(values[0], values[-1]),
                                               description=description,
                                               **kwargs)

    def selector(self, **kwargs):
        """Selection list for interactive plotting.

        Based on the data columns, ``ipywidgets.SelectMultiple`` widget is
        returned for selecting the data columns to be plotted. This method is
        based on ``ipywidgets.SelectMultiple``, so any keyword argument
        accepted by it can be passed.

        Returns
        -------
        ipywidgets.SelectMultiple

            Selection list.

        Example
        -------
        1. Get the widget for selecting data columns.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample', 'oommf-file1.odt')
        >>> table = ut.Table.fromfile(odtfile)
        >>> table.selector()
        SelectMultiple(...)

        """
        return ipywidgets.SelectMultiple(options=self.data_columns,
                                         value=self.data_columns,
                                         rows=5,
                                         description='y-axis:',
                                         disabled=False,
                                         **kwargs)
