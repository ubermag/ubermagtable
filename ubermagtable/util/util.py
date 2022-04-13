import re

# The OOMMF columns are renamed according to this dictionary.
oommf_dict = {
    "RungeKuttaEvolve:evolver:Total energy": "E",
    "RungeKuttaEvolve:evolver:Energy calc count": "E_calc_count",
    "RungeKuttaEvolve:evolver:Max dm/dt": "max_dm/dt",
    "RungeKuttaEvolve:evolver:dE/dt": "dE/dt",
    "RungeKuttaEvolve:evolver:Delta E": "delta_E",
    "RungeKuttaEvolve::Total energy": "E",
    "RungeKuttaEvolve::Energy calc count": "E_calc_count",
    "RungeKuttaEvolve::Max dm/dt": "max_dm/dt",
    "RungeKuttaEvolve::dE/dt": "dE/dt",
    "RungeKuttaEvolve::Delta E": "delta_E",
    "EulerEvolve:evolver:Total energy": "E",
    "EulerEvolve:evolver:Energy calc count": "E_calc_count",
    "EulerEvolve:evolver:Max dm/dt": "max_dmdt",
    "EulerEvolve:evolver:dE/dt": "dE/dt",
    "EulerEvolve:evolver:Delta E": "delta_E",
    "TimeDriver::Iteration": "iteration",
    "TimeDriver::Stage iteration": "stage_iteration",
    "TimeDriver::Stage": "stage",
    "TimeDriver::mx": "mx",
    "TimeDriver::my": "my",
    "TimeDriver::mz": "mz",
    "TimeDriver::Last time step": "last_time_step",
    "TimeDriver::Simulation time": "t",
    "CGEvolve:evolver:Max mxHxm": "max_mxHxm",
    "CGEvolve:evolver:Total energy": "E",
    "CGEvolve:evolver:Delta E": "delta_E",
    "CGEvolve:evolver:Bracket count": "bracket_count",
    "CGEvolve:evolver:Line min count": "line_min_count",
    "CGEvolve:evolver:Conjugate cycle count": "conjugate_cycle_count",
    "CGEvolve:evolver:Cycle count": "cycle_count",
    "CGEvolve:evolver:Cycle sub count": "cycle_sub_count",
    "CGEvolve:evolver:Energy calc count": "energy_calc_count",
    "CGEvolve::Max mxHxm": "max_mxHxm",
    "CGEvolve::Total energy": "E",
    "CGEvolve::Delta E": "delta_E",
    "CGEvolve::Bracket count": "bracket_count",
    "CGEvolve::Line min count": "line_min_count",
    "CGEvolve::Conjugate cycle count": "conjugate_cycle_count",
    "CGEvolve::Cycle count": "cycle_count",
    "CGEvolve::Cycle sub count": "cycle_sub_count",
    "CGEvolve::Energy calc count": "energy_calc_count",
    "FixedMEL::Energy": "MEL_E",
    "FixedMEL:magnetoelastic:Energy": "MEL_E",
    "SpinTEvolve:evolver:Total energy": "E",
    "SpinTEvolve:evolver:Energy calc count": "E_calc_count",
    "SpinTEvolve:evolver:Max dm/dt": "max_dmdt",
    "SpinTEvolve:evolver:dE/dt": "dE/dt",
    "SpinTEvolve:evolver:Delta E": "delta_E",
    "SpinTEvolve:evolver:average u": "average_u",
    "SpinXferEvolve:evolver:Total energy": "E",
    "SpinXferEvolve:evolver:Energy calc count": "E_calc_count",
    "SpinXferEvolve:evolver:Max dm/dt": "max_dmdt",
    "SpinXferEvolve:evolver:dE/dt": "dE/dt",
    "SpinXferEvolve:evolver:Delta E": "delta_E",
    "SpinXferEvolve:evolver:average u": "average_u",
    "SpinXferEvolve:evolver:average J": "average_J",
    "ThetaEvolve:evolver:Total energy": "E",
    "ThetaEvolve:evolver:Energy calc count": "E_calc_count",
    "ThetaEvolve:evolver:Max dm/dt": "max_dmdt",
    "ThetaEvolve:evolver:dE/dt": "dE/dt",
    "ThetaEvolve:evolver:Delta E": "delta_E",
    "ThetaEvolve:evolver:Temperature": "T",
    "ThermHeunEvolve:evolver:Total energy": "E",
    "ThermHeunEvolve:evolver:Energy calc count": "E_calc_count",
    "ThermHeunEvolve:evolver:Max dm/dt": "max_dmdt",
    "ThermHeunEvolve:evolver:dE/dt": "dE/dt",
    "ThermHeunEvolve:evolver:Delta E": "delta_E",
    "ThermHeunEvolve:evolver:Temperature": "T",
    "ThermSpinXferEvolve:evolver:Total energy": "E",
    "ThermSpinXferEvolve:evolver:Energy calc count": "E_calc_count",
    "ThermSpinXferEvolve:evolver:Max dm/dt": "max_dmdt",
    "ThermSpinXferEvolve:evolver:dE/dt": "dE/dt",
    "ThermSpinXferEvolve:evolver:Delta E": "delta_E",
    "ThermSpinXferEvolve:evolver:Temperature": "T",
    "MinDriver::Iteration": "iteration",
    "MinDriver::Stage iteration": "stage_iteration",
    "MinDriver::Stage": "stage",
    "MinDriver::mx": "mx",
    "MinDriver::my": "my",
    "MinDriver::mz": "mz",
    "UniformExchange::Max Spin Ang": "max_spin_ang",
    "UniformExchange::Stage Max Spin Ang": "stage_max_spin_ang",
    "UniformExchange::Run Max Spin Ang": "run_max_spin_ang",
    "UniformExchange::Energy": "E_exchange",
    "DMExchange6Ngbr::Energy": "E",
    "DMI_Cnv::Energy": "E",
    "DMI_T::Energy": "E",
    "DMI_D2d::Energy": "E",
    "Demag::Energy": "E",
    "FixedZeeman::Energy": "E_zeeman",
    "UZeeman::Energy": "E_zeeman",
    "UZeeman::B": "B",
    "UZeeman::Bx": "Bx",
    "UZeeman::By": "By",
    "UZeeman::Bz": "Bz",
    "ScriptUZeeman::Energy": "E",
    "ScriptUZeeman::B": "B",
    "ScriptUZeeman::Bx": "Bx",
    "ScriptUZeeman::By": "By",
    "ScriptUZeeman::Bz": "Bz",
    "TransformZeeman::Energy": "E",
    "CubicAnisotropy::Energy": "E",
    "UniaxialAnisotropy::Energy": "E",
    "UniaxialAnisotropy4::Energy": "E",
    "Southampton_UniaxialAnisotropy4::Energy": "E",
    "Exchange6Ngbr::Energy": "E",
    "Exchange6Ngbr::Max Spin Ang": "max_spin_ang",
    "Exchange6Ngbr::Stage Max Spin Ang": "stage_max_spin_ang",
    "Exchange6Ngbr::Run Max Spin Ang": "run_max_spin_ang",
    "ExchangePtwise::Energy": "E",
    "ExchangePtwise::Max Spin Ang": "max_spin_ang",
    "ExchangePtwise::Stage Max Spin Ang": "stage_max_spin_ang",
    "ExchangePtwise::Run Max Spin Ang": "run_max_spin_ang",
    "TwoSurfaceExchange::Energy": "E",
}

# The mumax3 columns are renamed according to this dictionary.
mumax3_dict = {
    "t": "t",
    "mx": "mx",
    "my": "my",
    "mz": "mz",
    "E_total": "E",
    "E_exch": "E_totalexchange",
    "E_demag": "E_demag",
    "E_Zeeman": "E_zeeman",
    "E_anis": "E_totalanisotropy",
    "dt": "dt",
    "maxTorque": "maxtorque",
}


def rename_column(name, cols_dict):
    if name in cols_dict.keys():
        return cols_dict[name]

    for key in cols_dict.keys():
        if len(key.split("::")) == 2:
            start, end = key.split("::")
            name_split = name.split(":")
            if name_split[0] == start and name_split[-1] == end:
                term_name = name.split(":")[1]
                type_name = cols_dict[key]
                # required for E_exchange in old and new OOMMF odt files
                if not type_name.endswith(term_name):
                    type_name = f"{type_name}_{term_name}"
                return type_name
    else:
        return name  # name cannot be found in dictionary


def columns(filename, rename=True):
    """Extracts column names from a table file.

    Parameters
    ----------
    filename : str

        OOMMF ``.odt`` or mumax3 ``.txt`` file.

    rename : bool

        If ``rename=True``, the column names are renamed with their shorter
        versions. Defaults to ``True``.

    Returns
    -------
    list

        List of column names.

    Examples
    --------
    1. Extracting the column names from an OOMMF `.odt` file.

    >>> import os
    >>> import ubermagtable.util as uu
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__), '..',
    ...                        'tests', 'test_sample', 'oommf-new-file1.odt')
    >>> uu.columns(odtfile)
    [...]

    2. Extracting the names of columns from a mumax3 `.txt` file.

    >>> odtfile = os.path.join(os.path.dirname(__file__), '..',
    ...                        'tests', 'test_sample', 'mumax3-file1.txt')
    >>> uu.columns(odtfile)
    [...]

    """
    with open(filename) as f:
        lines = f.readlines()

    if lines[0].startswith("# ODT"):  # OOMMF odt file
        cline = list(filter(lambda l: l.startswith("# Columns:"), lines))[0]
        cline = re.split(r"Oxs_|Anv_|Southampton_|My_|YY_|UHH_|Xf_", cline)[1:]
        cline = list(map(lambda col: re.sub(r"[{}]", "", col), cline))
        cols = list(map(lambda s: s.strip(), cline))
        cols_dict = oommf_dict
    else:  # mumax3 txt file
        cline = lines[0][2:].rstrip().split("\t")
        cols = list(map(lambda s: s.split(" ")[0], cline))
        cols_dict = mumax3_dict

    if rename:
        return [rename_column(col, cols_dict) for col in cols]
    else:
        return cols


def units(filename, rename=True):
    """Extracts units for individual columns from a table file.

    This method extracts both column names and units and returns a dictionary,
    where keys are column names and values are the units.

    Parameters
    ----------
    filename : str

        OOMMF ``.odt`` or mumax3 ``.txt`` file.

    rename : bool

        If ``rename=True``, the column names are renamed with their shorter
        versions. Defaults to ``True``.

    Returns
    -------
    dict

        Dictionary of column names and units.

    Examples
    --------
    1. Extracting units for individual columns from an OOMMF ``.odt`` file.

    >>> import os
    >>> import ubermagtable.util as uu
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__), '..',
    ...                        'tests', 'test_sample', 'oommf-new-file2.odt')
    >>> uu.units(odtfile)
    {...}

    2. Extracting units for individual columns from a mumax3 ``.txt`` file.

    >>> odtfile = os.path.join(os.path.dirname(__file__), '..',
    ...                        'tests', 'test_sample', 'mumax3-file1.txt')
    >>> uu.units(odtfile)
    {...}

    """
    with open(filename) as f:
        lines = f.readlines()

    if lines[0].startswith("# ODT"):  # OOMMF odt file
        uline = list(filter(lambda l: l.startswith("# Units:"), lines))[0]
        units = uline.split()[2:]
        units = list(map(lambda s: re.sub(r"[{}]", "", s), units))
    else:  # mumax3 txt file
        uline = lines[0][2:].rstrip().split("\t")
        units = list(map(lambda s: s.split()[1], uline))
        units = list(map(lambda s: re.sub(r"[()]", "", s), units))

    return dict(zip(columns(filename, rename=rename), units))


def data(filename):
    """Extracts numerical data from a table file.

    Parameters
    ----------
    filename : str

        OOMMF ``.odt`` or mumax3 ``.txt`` file.

    Returns
    -------
    list

        List of numerical data.

    Examples
    --------
    1. Reading data from an OOMMF ``.odt`` file.

    >>> import os
    >>> import ubermagtable.util as uu
    ...
    >>> odtfile = os.path.join(os.path.dirname(__file__), '..',
    ...                        'tests', 'test_sample', 'oommf-new-file3.odt')
    >>> uu.data(odtfile)
    [...]

    2. Reading data from a mumax3 ``.txt`` file.

    >>> odtfile = os.path.join(os.path.dirname(__file__), '..',
    ...                        'tests', 'test_sample', 'mumax3-file1.txt')
    >>> uu.data(odtfile)
    [...]

    """
    with open(filename) as f:
        lines = f.readlines()

    values = []
    for line in lines:
        if not line.startswith("#"):
            values.append(list(map(float, line.split())))

    return values
