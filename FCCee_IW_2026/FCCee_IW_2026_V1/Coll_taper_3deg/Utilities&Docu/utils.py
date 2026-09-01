# ============================================================
# FCC-ee WAKE MODEL UTILITIES
# ============================================================
#
# Designed for the FCC-ee IW repository structure:
#
# FCCee_IW_2026_V1/Coll_taper_3deg/
# ├── Impedances/
# ├── Plots/
# ├── Simulation_files/
# ├── Utilities&Docu/
# └── Wakes/
#     ├── Devices/
#     └── Total/
#
# This module contains all functions used to:
#
#   - read wake files
#   - read Xwakes wake files
#   - check and align time grids
#   - sum selected device wakes
#   - save wakes in PyHEADTAIL and Xwakes conventions
#   - plot wakes
#   - plot device contributions
#   - compare selected wakes with the total wake
#
# The internal wake representation is PyHEADTAIL convention.
# ============================================================


import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

REPO_ROOT = Path.cwd().parent

WAKES_DEVICES = REPO_ROOT / "Wakes" / "Devices"
WAKES_TOTAL   = REPO_ROOT / "Wakes" / "Total"
PLOTS_FOLDER  = REPO_ROOT / "Plots"


# ============================================================
# STANDARD WAKE COLUMNS
# ============================================================

WAKE_COLUMNS = [
    "time_ns",
    "Wlong",
    "Wxdip",
    "Wydip",
    "Wxquad",
    "Wyquad",
]


# ============================================================
# WAKE LABELS
# ============================================================

WAKE_LABELS = {
    "Wlong":  r"$W_{long}$  [V/pC]",
    "Wxdip":  r"$W_{x,dip}$  [V/(pC mm)]",
    "Wydip":  r"$W_{y,dip}$  [V/(pC mm)]",
    "Wxquad": r"$W_{x,quad}$  [V/(pC mm)]",
    "Wyquad": r"$W_{y,quad}$  [V/(pC mm)]",
}


WAKE_LABELS_SI = {
    "Wlong":  r"$W_{long}$  [V/C]",
    "Wxdip":  r"$W_{x,dip}$  [V/(C m)]",
    "Wydip":  r"$W_{y,dip}$  [V/(C m)]",
    "Wxquad": r"$W_{x,quad}$  [V/(C m)]",
    "Wyquad": r"$W_{y,quad}$  [V/(C m)]",
}


# ============================================================
# DEVICE FILES
# ============================================================

DEVICE_FILES = {

    "IR":                "W_IR.txt",
    "RF":                "W_RF.txt",
    "bpm":               "W_bpm.txt",
    "coll3cm":           "W_coll3cm.txt",
    "ems":               "W_ems.txt",
    "kickers":           "W_kickers.txt",
    "pipe_rw":           "W_pipe_RW.txt",
    "strip_kickers":     "W_strip_kickers.txt",
    "SRabs":             "W_SRabs.txt",
    "kickers_optimized": "W_kickers_opt.txt",
    "int_mod":           "W_int_mod.txt",
}


# ============================================================
# READ ONE WAKE FILE
# ============================================================

def read_wake_file(filename):
    """
    Read a wake file using PyHEADTAIL units/convention.

    Internal representation:

        time_ns : ns
        Wlong   : V/pC
        Wxdip   : V/(pC mm)
        Wydip   : V/(pC mm)
        Wxquad  : V/(pC mm)
        Wyquad  : V/(pC mm)

    Files can contain either 4 or 6 columns.

    4 columns:
        time, Wlong, Wxdip, Wydip

    6 columns:
        time, Wlong, Wxdip, Wydip, Wxquad, Wyquad
    """

    file = Path(filename)

    if not file.exists():

        raise FileNotFoundError(
            f"Wake file not found: {file}"
        )

    data = np.loadtxt(
        file,
        skiprows=1,
        ndmin=2
    )

    if data.shape[1] not in (4, 6):

        raise ValueError(
            f"{file.name}: expected 4 or 6 columns, "
            f"found {data.shape[1]}"
        )

    # --------------------------------------------------------
    # Read common columns
    # --------------------------------------------------------

    time = data[:, 0]
    Wlong = data[:, 1]
    Wxdip = data[:, 2]
    Wydip = data[:, 3]

    # --------------------------------------------------------
    # Quadrupolar wakes
    # --------------------------------------------------------

    if data.shape[1] == 6:

        Wxquad = data[:, 4]
        Wyquad = data[:, 5]

    else:

        Wxquad = np.zeros_like(time)
        Wyquad = np.zeros_like(time)

    # --------------------------------------------------------
    # Return standard internal representation
    # --------------------------------------------------------

    return {
        "time_ns": time,
        "Wlong": Wlong,
        "Wxdip": Wxdip,
        "Wydip": Wydip,
        "Wxquad": Wxquad,
        "Wyquad": Wyquad,
    }


# ============================================================
# WAKE DICTIONARY -> STANDARD ARRAY
# ============================================================

def wake_to_array(wake):
    """
    Return a wake dictionary as the standard 6-column array.
    """

    return np.column_stack([
        wake["time_ns"],
        wake["Wlong"],
        wake["Wxdip"],
        wake["Wydip"],
        wake["Wxquad"],
        wake["Wyquad"],
    ])


# ============================================================
# SAVE WAKE
# ============================================================

def save_wake(wake, filename, folder=None):

    path = Path(filename)

    if folder is not None:

        folder = Path(folder)

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        path = folder / path

    # ========================================================
    # PYHEADTAIL
    # ========================================================

    pyheadtail_path = path.with_name(
        path.stem + "_pyheadtail" + path.suffix
    )

    time_ns = np.asarray(
        wake["time_ns"]
    )

    Wlong = np.asarray(
        wake["Wlong"]
    )

    Wxdip = np.asarray(
        wake["Wxdip"]
    )

    Wydip = np.asarray(
        wake["Wydip"]
    )

    Wxquad = np.asarray(
        wake["Wxquad"]
    )

    Wyquad = np.asarray(
        wake["Wyquad"]
    )

    header_pyheadtail = (
        "time [ns]\t"
        "Wlong [V/pC]\t"
        "Wxdip [V/pC.mm]\t"
        "Wydip [V/pC.mm]\t"
        "Wxquad [V/pC.mm]\t"
        "Wyquad [V/pC.mm]"
    )

    data_pyheadtail = np.column_stack((
        time_ns,
        Wlong,
        Wxdip,
        Wydip,
        Wxquad,
        Wyquad,
    ))

    np.savetxt(
        pyheadtail_path,
        data_pyheadtail,
        header=header_pyheadtail,
        comments="",
    )

    # ========================================================
    # XWAKES SI CONVERSION
    # ========================================================

    # Time:
    # ns -> s

    time_s = time_ns * 1e-9

    # Longitudinal:
    # V/pC -> V/C
    #
    # and invert sign according to the chosen
    # PyHEADTAIL <-> Xwakes convention.

    Wlong_SI = -Wlong * 1e12

    # Transverse:
    # V/(pC mm) -> V/(C m)

    Wxdip_SI = Wxdip * 1e15
    Wydip_SI = Wydip * 1e15
    Wxquad_SI = Wxquad * 1e15
    Wyquad_SI = Wyquad * 1e15

    si_path = path.with_name(
        path.stem + "_xwakes" + path.suffix
    )

    header_xwakes = (
        "time [s]\t"
        "Wlong [V/C]\t"
        "Wxdip [V/(C.m)]\t"
        "Wydip [V/(C.m)]\t"
        "Wxquad [V/(C.m)]\t"
        "Wyquad [V/(C.m)]"
    )

    data_xwakes = np.column_stack((
        time_s,
        Wlong_SI,
        Wxdip_SI,
        Wydip_SI,
        Wxquad_SI,
        Wyquad_SI,
    ))

    np.savetxt(
        si_path,
        data_xwakes,
        header=header_xwakes,
        comments="",
    )

    print(
        f"Saved PyHEADTAIL wake: {pyheadtail_path}"
    )

    print(
        f"Saved Xwakes wake:   {si_path}"
    )


# ============================================================
# LIST WAKE DEVICES
# ============================================================

def list_wake_devices(folder=WAKES_DEVICES):

    files = sorted(
        Path(folder).glob("W_*.txt")
    )

    print(
        f"Looking in: {Path(folder).resolve()}"
    )

    print("Files found:")

    for f in files:

        print(
            f"  {f.name}"
        )

    return files


# ============================================================
# CHECK / ALIGN TIME GRIDS
# ============================================================

def check_time_grid(
    wakes,
    reference_name=None,
    rtol=1e-10,
    atol=1e-14,
):
    """
    Check and align the time grids of the wakes.

    If the time grids are different, all wakes are
    interpolated onto a common time grid.

    The common grid is the union of all time points
    present in the input wakes.

    Outside the original range of a wake,
    the wake is set to zero.
    """

    if not wakes:

        raise ValueError(
            "No wakes supplied."
        )

    names = list(
        wakes.keys()
    )

    if reference_name is None:

        reference_name = names[0]

    # ========================================================
    # BUILD COMMON TIME GRID
    # ========================================================

    common_time = np.unique(
        np.concatenate([
            wakes[name]["time_ns"]
            for name in names
        ])
    )

    common_time = np.sort(
        common_time
    )

    # ========================================================
    # INTERPOLATE ALL WAKES
    # ========================================================

    wakes_interpolated = {}

    wake_components = [
        "Wlong",
        "Wxdip",
        "Wydip",
        "Wxquad",
        "Wyquad",
    ]

    for name in names:

        wake = wakes[name]

        t_old = wake["time_ns"]

        interpolated_wake = {
            "time_ns": common_time.copy()
        }

        for component in wake_components:

            interpolated_wake[component] = np.interp(
                common_time,
                t_old,
                wake[component],
                left=0.0,
                right=0.0,
            )

        wakes_interpolated[name] = (
            interpolated_wake
        )

    # ========================================================
    # CHECK INTERPOLATION
    # ========================================================

    for name, wake in wakes_interpolated.items():

        if not np.allclose(
            wake["time_ns"],
            common_time,
            rtol=rtol,
            atol=atol,
        ):

            raise ValueError(
                f"Time-grid interpolation failed "
                f"for '{name}'."
            )

    return wakes_interpolated


# ============================================================
# SUM SELECTED WAKES
# ============================================================

def sum_selected_wakes(
    devices,
    selected_components
):
    """
    Sum the wakes of the selected devices.

    All wakes are first interpolated onto the
    same common time grid.
    """

    if len(selected_components) == 0:

        raise ValueError(
            "selected_components is empty."
        )

    # --------------------------------------------------------
    # Check that requested devices exist
    # --------------------------------------------------------

    missing = [
        name
        for name in selected_components
        if name not in devices
    ]

    if missing:

        raise KeyError(
            "These selected components are not available: "
            f"{missing}"
        )

    # --------------------------------------------------------
    # Select devices
    # --------------------------------------------------------

    selected = {
        name: devices[name]
        for name in selected_components
    }

    # --------------------------------------------------------
    # IMPORTANT:
    # use the interpolated wakes returned by
    # check_time_grid()
    # --------------------------------------------------------

    selected = check_time_grid(
        selected
    )

    # --------------------------------------------------------
    # Common time grid
    # --------------------------------------------------------

    t = selected[
        selected_components[0]
    ]["time_ns"]

    # --------------------------------------------------------
    # Initialize total wake
    # --------------------------------------------------------

    summed = {

        "time_ns": t.copy(),

        "Wlong": np.zeros_like(
            t,
            dtype=float
        ),

        "Wxdip": np.zeros_like(
            t,
            dtype=float
        ),

        "Wydip": np.zeros_like(
            t,
            dtype=float
        ),

        "Wxquad": np.zeros_like(
            t,
            dtype=float
        ),

        "Wyquad": np.zeros_like(
            t,
            dtype=float
        ),
    }

    # --------------------------------------------------------
    # Sum all selected devices
    # --------------------------------------------------------

    wake_components = [
        "Wlong",
        "Wxdip",
        "Wydip",
        "Wxquad",
        "Wyquad",
    ]

    for name in selected_components:

        wake = selected[name]

        for key in wake_components:

            summed[key] += wake[key]

    return summed


# ============================================================
# READ ALL WAKE DEVICES
# ============================================================

def read_wake_devices(
    device_files=DEVICE_FILES,
    folder=WAKES_DEVICES
):
    """
    Read all devices defined in DEVICE_FILES.

    All wakes are stored internally using the
    PyHEADTAIL convention.
    """

    devices = {}

    for name, filename in device_files.items():

        path = Path(folder) / filename

        if not path.exists():

            print(
                f"WARNING: {name}: "
                f"file not found -> {path}"
            )

            continue

        devices[name] = read_wake_file(
            path
        )

    if not devices:

        raise FileNotFoundError(
            "No wake device files could be read from "
            f"{Path(folder).resolve()}"
        )

    return devices


# ============================================================
# READ XWAKES FILE
# ============================================================

def read_xwakes_file(filename):
    """
    Read an already saved Xwakes-convention wake file.

    Units:

        time  : s
        Wlong : V/C
        Wxdip : V/(C m)
        Wydip : V/(C m)
        Wxquad: V/(C m)
        Wyquad: V/(C m)

    This function is ONLY used for reading Xwakes files
    for plotting or other Xwakes-specific operations.

    Internal device/summation wakes remain in PyHEADTAIL
    convention.
    """

    file = Path(filename)

    if not file.exists():

        raise FileNotFoundError(
            f"Xwakes wake file not found: {file}"
        )

    data = np.loadtxt(
        file,
        skiprows=1,
        ndmin=2
    )

    if data.shape[1] not in (4, 6):

        raise ValueError(
            f"{file.name}: expected 4 or 6 columns, "
            f"found {data.shape[1]}"
        )

    time_s = data[:, 0]
    Wlong = data[:, 1]
    Wxdip = data[:, 2]
    Wydip = data[:, 3]

    if data.shape[1] == 6:

        Wxquad = data[:, 4]
        Wyquad = data[:, 5]

    else:

        Wxquad = np.zeros_like(
            time_s
        )

        Wyquad = np.zeros_like(
            time_s
        )

    return {
        "time_s": time_s,
        "Wlong": Wlong,
        "Wxdip": Wxdip,
        "Wydip": Wydip,
        "Wxquad": Wxquad,
        "Wyquad": Wyquad,
    }


# ============================================================
# PLOT ONE WAKE
# ============================================================


def plot_wake(
    wake,
    wake_name="wake",
    wake_component="Wydip",
    save=True,
    filename=None,
    ax=None,
    label=None,
    convention="pyheadtail",
):
    """
    Plot a wake dictionary.

    convention="pyheadtail":
        time in ns
        wake in PyHEADTAIL units

    convention="xwakes":
        time in s
        wake in Xwakes SI units
    """

    if convention == "pyheadtail":

        labels = WAKE_LABELS
        time_key = "time_ns"
        xlabel = "time [ns]"

    elif convention == "xwakes":

        labels = WAKE_LABELS_SI
        time_key = "time_s"
        xlabel = "time [s]"

    else:

        raise ValueError(
            "convention must be "
            "'pyheadtail' or 'xwakes'."
        )

    if wake_component not in labels:

        raise ValueError(
            f"Unknown wake component: "
            f"{wake_component}"
        )

    # --------------------------------------------------------
    # MATPLOTLIB SETTINGS
    # --------------------------------------------------------

    mpl.rcParams.update({
        "font.size": 18,
        "axes.titlesize": 18,
        "axes.labelsize": 18,
        "xtick.labelsize": 18,
        "ytick.labelsize": 18,
        "legend.fontsize": 15,
    })

    # --------------------------------------------------------
    # CREATE FIGURE IF NECESSARY
    # --------------------------------------------------------

    own_figure = ax is None

    if own_figure:

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        # Give the axes enough room for the labels,
        # while keeping the complete figure centered
        # in the notebook output.
        fig.tight_layout(
            pad=2.0
        )

    # --------------------------------------------------------
    # PLOT
    # --------------------------------------------------------

    ax.plot(
        wake[time_key],
        wake[wake_component],
        lw=1.8,
        label=(
            label
            if label is not None
            else wake_name
        )
    )

    # --------------------------------------------------------
    # AXES
    # --------------------------------------------------------

    ax.set_xlabel(
        xlabel
    )

    ax.set_ylabel(
        labels[wake_component]
    )

    ax.legend(
        loc="best"
    )

    # --------------------------------------------------------
    # STANDALONE FIGURE
    # --------------------------------------------------------

    if own_figure:

        ax.set_xlim(
            np.min(
                wake[time_key]
            ),
            np.max(
                wake[time_key]
            )
        )

        if filename is None:

            filename = (
                f"{wake_name}_"
                f"{wake_component}.jpg"
            )

        if save:

            fig.savefig(
                PLOTS_FOLDER / filename,
                dpi=300,
                bbox_inches="tight"
            )

        # ----------------------------------------------------
        # DISPLAY FIGURE CENTERED IN JUPYTER
        # ----------------------------------------------------

        from IPython.display import display

        display(
            fig
        )

        plt.close(fig)

        return ax

    return ax


# ============================================================
# PLOT WAKE FILE
# ============================================================

def plot_wake_file(
    filename,
    wake_component="Wydip",
    folder=None,
    save=True,
    plot_filename=None,
    convention="pyheadtail",
):
    """
    Read and plot an already existing wake file.

    For PyHEADTAIL:
        use the normal PyHEADTAIL wake file.

    For Xwakes:
        use the already saved _xwakes file.
    """

    path = Path(
        filename
    )

    if folder is not None:

        path = Path(folder) / path

    # --------------------------------------------------------
    # READ ACCORDING TO CONVENTION
    # --------------------------------------------------------

    if convention == "pyheadtail":

        wake = read_wake_file(
            path
        )

    elif convention == "xwakes":

        wake = read_xwakes_file(
            path
        )

    else:

        raise ValueError(
            "convention must be "
            "'pyheadtail' or 'xwakes'."
        )

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    wake_name = path.stem

    # --------------------------------------------------------
    # PLOT
    # --------------------------------------------------------

    return plot_wake(
        wake,
        wake_name=wake_name,
        wake_component=wake_component,
        save=save,
        filename=plot_filename,
        convention=convention,
    )


# ============================================================
# PLOT DEVICE CONTRIBUTIONS
# ============================================================

def plot_wake_contributions(
    devices,
    component_names,
    wake_component="Wydip",
    save=True,
    filename=None,
):
    """
    Plot individual device contributions.

    Device wakes are stored internally in PyHEADTAIL
    convention.
    """

    if wake_component not in WAKE_LABELS:

        raise ValueError(
            f"Unknown wake component: "
            f"{wake_component}"
        )

    missing = [
        name
        for name in component_names
        if name not in devices
    ]

    if missing:

        raise KeyError(
            f"Unknown/unloaded devices: {missing}"
        )

    # --------------------------------------------------------
    # MATPLOTLIB SETTINGS
    # --------------------------------------------------------

    mpl.rcParams.update({
        "font.size": 18,
        "axes.titlesize": 18,
        "axes.labelsize": 18,
        "xtick.labelsize": 18,
        "ytick.labelsize": 18,
        "legend.fontsize": 15,
    })

    # --------------------------------------------------------
    # CREATE FIGURE
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(6, 4),
        constrained_layout=True
    )

    # --------------------------------------------------------
    # PLOT DEVICES
    # --------------------------------------------------------

    for name in component_names:

        wake = devices[name]

        ax.plot(
            wake["time_ns"],
            wake[wake_component],
            lw=1.8,
            label=name
        )

    # --------------------------------------------------------
    # AXES
    # --------------------------------------------------------

    ax.set_xlabel(
        "time [ns]"
    )

    ax.set_ylabel(
        WAKE_LABELS[wake_component]
    )

    xmin = min(
        np.min(
            devices[name]["time_ns"]
        )
        for name in component_names
    )

    xmax = max(
        np.max(
            devices[name]["time_ns"]
        )
        for name in component_names
    )

    ax.set_xlim(
        xmin,
        xmax
    )

    ax.legend(
        loc="best"
    )

#   fig.subplots_adjust(
#      left=0.4,
#       right=0.95,
#       bottom=0.18,
#       top=0.92
#   )
    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    if filename is None:

        filename = (
            f"W_devices_"
            f"{wake_component}.jpg"
        )

    if save:

        fig.savefig(
            PLOTS_FOLDER / filename,
            dpi=300,
            bbox_inches="tight"
        )

    return fig, ax


# ============================================================
# PLOT SELECTED WAKE VS TOTAL
# PYHEADTAIL VERSION
# ============================================================

def plot_selected_vs_total(
    selected_wake,
    total_wake,
    selected_components,
    wake_component="Wydip",
    save=True,
):
    """
    Compare selected wake with total wake.

    Both wakes are already stored internally in
    PyHEADTAIL convention.
    """

    if wake_component not in WAKE_LABELS:

        raise ValueError(
            f"Unknown wake component: "
            f"{wake_component}"
        )

    # --------------------------------------------------------
    # CREATE FIGURE
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(6, 4),
        constrained_layout=True
    )

    # --------------------------------------------------------
    # SELECTED WAKE
    # --------------------------------------------------------

    plot_wake(
        selected_wake,
        wake_name="selected",
        wake_component=wake_component,
        save=False,
        ax=ax,
        label=" + ".join(
            selected_components
        ),
        convention="pyheadtail",
    )

    # --------------------------------------------------------
    # TOTAL WAKE
    # --------------------------------------------------------

    plot_wake(
        total_wake,
        wake_name="W_total",
        wake_component=wake_component,
        save=False,
        ax=ax,
        label="W_total",
        convention="pyheadtail",
    )

    # --------------------------------------------------------
    # FINAL SETTINGS
    # --------------------------------------------------------

    ax.legend(
        loc="best"
    )

    #   fig.subplots_adjust(
    #      left=0.4,
    #       right=0.95,
    #       bottom=0.18,
    #       top=0.92
    #   )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    if save:

        filename = (
            f"W_selected_vs_total_"
            f"{wake_component}_pyheadtail.jpg"
        )

        fig.savefig(
            PLOTS_FOLDER / filename,
            dpi=300,
            bbox_inches="tight"
        )

    return fig, ax


# ============================================================
# PLOT TOTAL XWAKES FILE
# ============================================================

def plot_total_xwakes_file(
    filename,
    wake_component="Wydip",
    folder=None,
    save=True,
    plot_filename=None,
):
    """
    Read an already saved Xwakes wake file and plot it.

    No conversion is performed here.

    The file is assumed to already contain:

        time [s]
        Wlong [V/C]
        transverse wakes [V/(C m)]
    """

    path = Path(
        filename
    )

    if folder is not None:

        path = Path(folder) / path

    # --------------------------------------------------------
    # READ EXISTING XWAKES FILE
    # --------------------------------------------------------

    wake_xwakes = read_xwakes_file(
        path
    )

    # --------------------------------------------------------
    # PLOT
    # --------------------------------------------------------

    if plot_filename is None:

        plot_filename = (
            f"{path.stem}_"
            f"{wake_component}_xwakes.jpg"
        )

    return plot_wake(
        wake_xwakes,
        wake_name=path.stem,
        wake_component=wake_component,
        save=save,
        filename=plot_filename,
        convention="xwakes",
    )
 