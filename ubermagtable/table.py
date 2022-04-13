import ipywidgets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ubermagutil.typesystem as ts
import ubermagutil.units

import ubermagtable.util as uu


@ts.typesystem(
    data=ts.Typed(expected_type=pd.DataFrame), units=ts.Typed(expected_type=dict)
)
class Table:
    """Tabular data class.

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

    x : str, optional

        Independent variable column name. Defaults to ``None``.

    Examples
    --------
    1. Defining ``ubermagtable.Table`` by reading an OOMMF ``.odt`` file.

    >>> import os
    >>> import ubermagtable as ut
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'oommf-new-file1.odt')
    >>> table = ut.Table.fromfile(odtfile, x='iteration')

    """

    def __init__(self, data, units, x=None, attributes=None):
        self.data = data
        self.units = units
        self.x = x
        self.attributes = attributes if attributes is not None else {}
        self.attributes.setdefault("fourierspace", False)

    def apply(self, func, columns=None, args=(), **kwargs):
        r"""Apply function.

        ``apply`` takes a function and its arguments along with a list of
        columns that the function should be applied to.
        It uses the fuction on all of the values in the chosen columns and
        returns an ``ubermagtable.Table`` object.
        This function is based off of `pandas.DataFrame.apply
        <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html>`_.

        If ``columns`` is not specified, by default the function will be
        applied to all dependent variable columns i.e. ``Table.y``.

        Parameters
        ----------
        func : function

            Function to apply to selected columns.

        columns : list, optional

            A list of variables to be plotted.  Defaults to ``None``.

        args : turple

            Positional arguments to pass to func in addition to the data.

        **kwargs

            Additional keyword arguments to pass as keywords arguments to func.

        Returns
        -------
        ubermagtable.Table

            Result of applying func to selected columns in the table.

        Examples
        --------
        1. Applying absolute function to data.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample',
        ...                        'oommf-old-file1.odt')
        >>> table = ut.Table.fromfile(odtfile, x='t')
        >>> new_table = table.apply(np.abs)
        ...

        """
        if columns is None:
            columns = self.y

        return self.__class__(
            self.data.apply(
                lambda x: func(x, *args, **kwargs) if x.name in columns else x
            ),
            self.units,
            x=self.x,
            attributes=self.attributes,
        )

    @property
    def dx(self):
        """Spacing of independent variable."""
        d = np.diff(self.data[self.x])
        if np.isclose(np.max(d), np.min(d)):
            return d[0]
        else:
            msg = f"Independent variable {self.x=} spacing is not even."
            raise ValueError(msg)

    def rfft(self, x=None, y=None):
        """Real Fast Fourier Transform.

        The real fast Fourier transform of columns ``y`` with frequency
        dependent on ``x``.

        Parameters
        ----------
        x : str, optional

            The independent variable to be Fourier transformed. If not
            specified ``table.x`` is used. Defaults to ``None``.

        y : list, optional

            A list of dependent variables to be Fourier transformed. If not
            specified all columns in ``table.y`` are Fourier transformed.
            Defaults to ``None``.

        Returns
        -------
        ubermagtable.Table

            Result of applying a real Fourier transform to selected columns in
            the table.

        Examples
        --------
        1. Applying Fourier transforms to the table.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample',
        ...                        'oommf-new-file5.odt')
        >>> table = ut.Table.fromfile(odtfile, x='t')
        >>> fft_table = table.rfft()
        ...

        """
        x = self.x if x is None else x

        if x is None:
            raise ValueError("No independent variable specified.")
        elif x not in self.data.columns:
            msg = f"Independent variable {x=} is not in table."
            raise ValueError(msg)

        freqs = np.fft.rfftfreq(self.data[x].size, self.dx)
        cols = ["f"]
        units = {"f": "Hz"}
        data = pd.DataFrame(freqs, columns=cols)

        if y is None:
            y = self.y

        for i in y:
            cols.append(f"ft_{i}")
            units["ft_" + i] = f"({self.units[i]})^-1"
            data[cols[-1]] = np.fft.rfft(self.data[i])

        attributes = dict(self.attributes)  # to explicitly copy
        attributes["realspace_x"] = [
            np.min(self.data[x]),  # Min
            np.max(self.data[x]),  # Max
            self.data[x].size,  # n
        ]
        attributes["fourierspace"] = True
        return self.__class__(data, units, x=cols[0], attributes=attributes)

    def irfft(self, x=None, y=None):
        """Inverse Real Fast Fourier Transform.

        The inverse real fast Fourier transform of columns :code:`y` with
        frequency dependent on :code:`x`.

        Parameters
        ----------
        x : str, optional

            The independent variable to be inverse Fourier transformed. If not
            specified ``table.x`` is used. Defaults to ``None``.

        y : list, optional

            A list of dependent variables to be inverse Fourier transformed. If
            not specified all columns in ``table.y`` are Fourier transformed.
            Defaults to ``None``.

        Returns
        -------
        ubermagtable.Table

            Result of applying a inverse real Fourier transform to selected
            columns in the table.

        Examples
        --------
        1. Applying inverse Fourier transforms to the table.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample',
        ...                        'oommf-new-file5.odt')
        >>> table = ut.Table.fromfile(odtfile, x='t')
        >>> ifft_table = table.rfft().irfft()
        ...

        """
        if not self.attributes["fourierspace"]:
            msg = (
                "Cannot inverse Fourier transform a table which "
                "has not already been Fourier transformed."
            )
            raise RuntimeError(msg)

        x = self.x if x is None else x

        if x is None:
            raise ValueError("No independent variable specified.")
        elif x not in self.data.columns:
            msg = f"Independent variable {x=} is not in table."
            raise ValueError(msg)

        t = np.linspace(*self.attributes["realspace_x"])
        cols = ["t"]
        units = {"t": "s"}
        data = pd.DataFrame(t, columns=cols)

        if y is None:
            y = self.y

        for i in y:
            cols.append(i[3:])  # remove leading 'ft_'
            units[i[3:]] = self.units[i][1:-4]  # remove '()^-1'
            data[cols[-1]] = np.fft.irfft(self.data[i])

        attributes = dict(self.attributes)  # to explicitly copy
        attributes["realspace_x"] = None
        attributes["fourierspace"] = False
        return self.__class__(data, units, x=cols[0], attributes=attributes)

    @property
    def x(self):
        """Independent variable.

        Returns
        -------
        str

            Column name.

        """
        return self._x

    @x.setter
    def x(self, value):
        if value in self.data.columns or value is None:
            self._x = value
        else:
            msg = f"Column {value} is not a column in data."
            raise ValueError(msg)

    @property
    def y(self):
        """Dependent variable(s).

        This property returns all data column names that are not specified as
        independent.

        Returns
        -------
        list

            Independent variables.

        Examples
        --------
        1. Getting data columns.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample',
        ...                        'oommf-old-file5.odt')
        >>> table = ut.Table.fromfile(odtfile, x='t')
        >>> table.y
        [...]

        """
        return [col for col in self.data.columns if col != self.x]

    @property
    def xmax(self):
        """Maximum value of independent variable.

        Returns
        -------
        numbers.Real

            Independent variable range.

        Examples
        --------
        1. Getting independent variable range.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample',
        ...                        'oommf-old-file1.odt')
        >>> table = ut.Table.fromfile(odtfile, x='t')
        >>> table.xmax / 1e-12  # get the results in picoseconds
        24.999...

        """
        return self.data[self.x].iloc[-1]

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
        ...                        'tests', 'test_sample',
        ...                        'oommf-old-file3.odt')
        >>> table = ut.Table.fromfile(odtfile, x='iteration')
        >>> repr(table)
        '...

        """
        return repr(self.data)

    def __lshift__(self, other):
        """Merges two tables into a single one.

        Tables are merged in such a way that the second operand's data is
        concatenated to the first operand's data. Because independent variable
        is unique and always successive, the xmax of the first operand is
        added to the independent variable of the second. If there is no
        independent variable column in second operand's table, no merging is
        allowed and ``ValueError`` is raised. If there are non-matching
        columns, the missing values will be ``NaN``.

        Merging is not supported for Fourier transformed tables.

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

            If second operand's table does not have independent variable
            column.

        Examples
        --------
        1. Merging two tables.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> dirname = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample')
        >>> odtfile1 = os.path.join(dirname, 'oommf-old-file1.odt')
        >>> odtfile2 = os.path.join(dirname, 'oommf-old-file2.odt')
        ...
        >>> table1 = ut.Table.fromfile(odtfile1, x='t')
        >>> table2 = ut.Table.fromfile(odtfile2, x='t')
        >>> merged_table = table1 << table2
        ...
        >>> table1.xmax / 1e-12  # in picoseconds
        24.999...
        >>> table2.xmax / 1e-12  # in picoseconds
        15.0
        >>> merged_table.xmax / 1e-12  # in picoseconds
        39.99...

        """
        if not isinstance(other, self.__class__):
            msg = (
                f"Unsupported operand type(s) for <<: {type(self)=} and {type(other)=}."
            )
            raise TypeError(msg)

        if other.x != self.x:
            msg = f"Independent variable {self.x=} mismatch."
            raise ValueError(msg)

        if self.attributes["fourierspace"]:
            # Concatenating frequency values as done for the independent
            # variable generally does not make sense.
            msg = "Fourier transformed table does not support operand <<."
            raise RuntimeError(msg)

        other_df = other.data.copy()  # make a deep copy of dataframe
        other_df[self.x] += self.data[self.x].iloc[-1]

        return self.__class__(
            data=pd.concat([self.data, other_df], ignore_index=True),
            units=self.units,
            x=self.x,
            attributes=self.attributes,
        )

    @classmethod
    def fromfile(cls, filename, /, x=None, rename=True):
        """Reads an OOMMF ``.odt`` or mumax3 ``.txt`` scalar data file and
        returns a ``ubermagtable.Table`` object.

        Parameters
        ----------
        filename : str

            OOMMF ``.odt`` or mumax3 ``.txt`` file.

        x : str, optional

            Independent variable name. Defaults to ``None``.

        rename : bool, optional

            If ``rename=True``, the column names are renamed with their shorter
            versions. Defaults to ``True``.

        Returns
        -------
        ubermagtable.Table

            Table object.

        Examples
        --------
        1. Defining ``ubermagtable.Table`` by reading an OOMMF ``.odt`` file.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample',
        ...                        'oommf-hysteresis1.odt')
        >>> table = ut.Table.fromfile(odtfile, x='B_hysteresis')

        2. Defining ``ubermagtable.Table`` by reading a mumax3 ``.txt`` file.

        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample', 'mumax3-file1.txt')
        >>> table = ut.Table.fromfile(odtfile, x='t')

        """
        cols = uu.columns(filename, rename=rename)

        return cls(
            data=pd.DataFrame(uu.data(filename), columns=cols),
            units=uu.units(filename, rename=rename),
            x=x,
        )

    def mpl(
        self,
        ax=None,
        figsize=None,
        x=None,
        y=None,
        xlim=None,
        multiplier=None,
        filename=None,
        **kwargs,
    ):
        """Table data plot.

        This method plots scalar values as a function of ``x``. If ``x`` is not
        passed, ``self.x`` is used. ``mpl`` adds the plot to
        ``matplotlib.axes.Axes`` passed via ``ax`` argument. If ``ax`` is not
        passed, ``matplotlib.axes.Axes`` object is created automatically and
        the size of a figure can be specified using ``figsize``. To choose
        particular data columns to be plotted ``y`` can be passed as a list of
        column names. The range of ``x`` values on the horizontal axis can be
        defined by passing a length-2 tuple using ``xlim``.

        It is often the case that the time length is small (e.g. on a
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

        x : str, optional

            Independent variable. Defaults to ``None``.

        y : list, optional

            A list of variables to be plotted.  Defaults to ``None``.

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
        ...                        'tests', 'test_sample',
        ...                        'oommf-old-file1.odt')
        >>> table = ut.Table.fromfile(odtfile, x='t')
        >>> table.mpl()

        """
        if x is None and self.x is not None:
            x = self.x

        if x not in self.data.columns:
            msg = f"Independent variable {x=} is not in table."
            raise ValueError(msg)

        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        if multiplier is None:
            multiplier = ubermagutil.units.si_multiplier(self.xmax)

        if y is None:
            y = self.y

        for i in y:
            ax.plot(
                np.divide(self.data[x].to_numpy(), multiplier),
                self.data[i],
                label=i,
                **kwargs,
            )

        units = f"({ubermagutil.units.rsi_prefixes[multiplier]}{self.units[x]})"
        ax.set_xlabel(f"{x}{units}")
        ax.set_ylabel("value")

        ax.grid(True)  # grid is turned off by default for field plots
        ax.legend()

        if xlim is not None:
            plt.xlim(*np.divide(xlim, multiplier))

        if filename is not None:
            plt.savefig(filename, bbox_inches="tight", pad_inches=0)

    def slider(self, x=None, multiplier=None, description=None, **kwargs):
        """Slider for interactive plotting.

        Based on the values in the independent variable column,
        ``ipywidgets.SelectionRangeSlider`` is returned for navigating
        interactive plots. This method is based on
        ``ipywidgets.SelectionRangeSlider``, so any keyword argument accepted
        by it can be passed.

        Parameters
        ----------
        x : str, optional

            Independent variable. Defaults to ``None``.

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

            Independent variable slider.

        Example
        -------
        1. Get slider for the independent variable.

        >>> import os
        >>> import ubermagtable as ut
        ...
        >>> odtfile = os.path.join(os.path.dirname(__file__),
        ...                        'tests', 'test_sample',
        ...                        'oommf-old-file1.odt')
        >>> table = ut.Table.fromfile(odtfile, x='t')
        >>> table.slider()
        SelectionRangeSlider(...)

        """
        if x is None and self.x is not None:
            x = self.x

        if x not in self.data.columns:
            msg = f"Independent variable {x=} is not in table."
            raise ValueError(msg)

        if multiplier is None:
            multiplier = ubermagutil.units.si_multiplier(self.xmax)

        values = self.data[self.x].to_numpy()
        labels = np.around(values / multiplier, decimals=2)
        options = list(zip(labels, values))

        if x == "t":
            units = f" ({ubermagutil.units.rsi_prefixes[multiplier]}s)"
        else:
            units = ""
        if description is None:
            description = f"{x}{units}:"

        return ipywidgets.SelectionRangeSlider(
            options=options,
            value=(values[0], values[-1]),
            description=description,
            **kwargs,
        )

    def selector(self, x=None, **kwargs):
        """Selection list for interactive plotting.

        Based on the independent variables, ``ipywidgets.SelectMultiple``
        widget is returned for selecting the data columns to be plotted. This
        method is based on ``ipywidgets.SelectMultiple``, so any keyword
        argument accepted by it can be passed.

        Parameters
        ----------
        x : str, optional

            Independent variable. Defaults to ``None``.

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
        ...                        'tests', 'test_sample',
        ...                        'oommf-old-file1.odt')
        >>> table = ut.Table.fromfile(odtfile, x='t')
        >>> table.selector()
        SelectMultiple(...)

        """
        if x is None and self.x is not None:
            x = self.x

        if x not in self.data.columns:
            msg = f"Independent variable {x=} is not in table."
            raise ValueError(msg)

        options = [col for col in self.data.columns if col != x]

        return ipywidgets.SelectMultiple(
            options=options,
            value=options,
            rows=5,
            description="y-axis:",
            disabled=False,
            **kwargs,
        )
