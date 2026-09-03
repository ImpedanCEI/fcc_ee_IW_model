# ============================================================
# utils_impedance.py
# Utility functions for FCC-ee impedance plotting
# ============================================================

from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import LogLocator


# ============================================================
# DEFAULT DEVICE INFORMATION
# ============================================================

DEVICE_ORDER = ["optimizedKicker","coll3cm","pipe_rw","SRabs","ems","stripkickers26","IR","flanges","int_mod","bpm","RF"]

DEVICE_LABELS = ["optimized kickers","collimators","beam pipe RW","SR abs.","ems","strip. kickers","IR","flanges","int. mod","bpm","RF",]

DEVICE_COLORS = ["purple","orange","blue","limegreen","steelblue","salmon","cyan","magenta","yellow","brown","gray",]


# ============================================================
# GENERAL PLOT SETTINGS
# ============================================================

def set_plot_style(font_size=16):
    """
    Set the global matplotlib font sizes.
    """

    mpl.rcParams.update({
        "font.size": font_size,
        "axes.titlesize": font_size,
        "axes.labelsize": font_size,
        "xtick.labelsize": font_size,
        "ytick.labelsize": font_size,
        "legend.fontsize": font_size - 2,
    })


# ============================================================
# READ DEVICE IMPEDANCES
# ============================================================

# ============================================================
# READ DEVICE IMPEDANCES
# ============================================================

def read_impedance_devices(folder, plane):
    """
    Read all device impedance files for a given plane.

    Expected filenames:
        Z_dipx_*.txt
        Z_dipy_*.txt
        Z_long_*.txt
        Z_quadx_*.txt
        Z_quady_*.txt

    Parameters
    ----------
    folder : str or Path
        Folder containing the impedance files.

    plane : str
        One of:
            'dipx'
            'dipy'
            'long'
            'quadx'
            'quady'

    Returns
    -------
    freq : ndarray
        Frequency grid.

    devices : dict
        Dictionary containing complex impedance arrays.

        Example:
            devices["kickers"]
            devices["bpm"]
            devices["RF"]
    """

    folder = Path(folder)

    if plane not in ["dipx", "dipy", "long", "quadx", "quady"]:
        raise ValueError(
            "plane must be 'dipx', 'dipy', 'long', 'quadx' or 'quady'"
        )

    pattern = f"Z_{plane}_*.txt"
    files = sorted(folder.glob(pattern))

    print("Looking in:", folder.resolve())
    print("Pattern:", pattern)
    print("Files found:")

    for f in files:
        print("  ", f.name)

    if len(files) == 0:
        raise FileNotFoundError(
            f"No files found with pattern '{pattern}' in:\n"
            f"{folder.resolve()}"
        )

    freq_ref = None
    devices = {}

    for f in files:

        data = np.loadtxt(f, comments="#")

        freq = data[:, 0]
        Z = data[:, 1] + 1j * data[:, 2]

        # Example:
        # Z_dipx_bpm.txt -> bpm
        name = f.stem.replace(f"Z_{plane}_", "")

        devices[name] = Z

        if freq_ref is None:
            freq_ref = freq

        else:
            if (
                len(freq) != len(freq_ref)
                or not np.allclose(freq, freq_ref)
            ):
                raise ValueError(
                    f"Frequency grid mismatch in file '{f.name}'.\n"
                    "All device files must have the same frequency grid."
                )

    return freq_ref, devices
# ============================================================
# GET DEVICE CONTRIBUTIONS
# ============================================================

def get_device_contributions(
    devices,
    device_order=None,
    device_labels=None,
    device_colors=None,
):
    """
    Select device contributions in a specified order.

    Returns
    -------
    Z_contributions : list
        List of impedance arrays.

    labels : list
        Labels corresponding to the contributions.

    colors : list
        Colors corresponding to the contributions.
    """

    if device_order is None:
        device_order = DEVICE_ORDER

    if device_labels is None:
        device_labels = DEVICE_LABELS

    if device_colors is None:
        device_colors = DEVICE_COLORS

    Z_contributions = []
    labels = []
    colors = []

    for device, label, color in zip(
        device_order,
        device_labels,
        device_colors,
    ):

        if device not in devices:
            print(
                f"Warning: device '{device}' not found. "
                "Skipping."
            )
            continue

        Z_contributions.append(devices[device])
        labels.append(label)
        colors.append(color)

    return Z_contributions, labels, colors


# ============================================================
# PLOT STACKED IMPEDANCE
# ============================================================

def plot_stacked_impedance(
    frequency,
    Z_contributions,
    labels,
    colors,
    plane="dipy",
    part="imag",
    image_folder=None,
    xlim=(1e-3, 10),
    ylim=(1e0, 1e10),
    figsize=(10, 7.5),
    show=True,
    save=True,
):
    """
    Plot impedance contributions as filled areas.

    Parameters
    ----------
    frequency : ndarray
        Frequency grid in GHz.

    Z_contributions : list of ndarray
        Complex impedance contributions.

    labels : list
        Labels for the legend.

    colors : list
        Fill colors.

    plane : str
        'dipx', 'dipy' or 'long'

    part : str
        'real' or 'imag'

    image_folder : str or Path
        Folder where the plot is saved.

    xlim : tuple
        Frequency limits.

    ylim : tuple
        Y-axis limits.

    show : bool
        Whether to display the plot.

    save : bool
        Whether to save the plot.

    Returns
    -------
    fig, ax
    """

    plane_label_map = {
        "dipx": r"$Z_x$",
        "dipy": r"$Z_y$",
        "long": r"$Z_{long}$",
        "quadx": r"$Z_{quad,x}$",
        "quady": r"$Z_{quad,y}$",
    }

    unit_map = {
        "dipx": r"($\Omega$/m)",
        "dipy": r"($\Omega$/m)",
        "long": r"($\Omega$)",
        "quadx": r"($\Omega$/m)",
        "quady": r"($\Omega$/m)",
    }

    if part not in ["real", "imag"]:
        raise ValueError(
            "part must be 'real' or 'imag'"
        )

    if plane not in plane_label_map:
        raise ValueError(
            "plane must be 'dipx', 'dipy', 'long', 'quadx' or 'quady'"
        )

    set_plot_style()

    if image_folder is not None:
        image_folder = Path(image_folder)
        image_folder.mkdir(parents=True, exist_ok=True)

    plt.close("all")

    fig, ax = plt.subplots(figsize=figsize)

    ax.set_xlabel("f (GHz)")

    if part == "real":
        values = [Z.real for Z in Z_contributions]
        part_label = "Re"
    else:
        values = [Z.imag for Z in Z_contributions]
        part_label = "Im"

    ylabel = (
        f"{part_label}[{plane_label_map[plane]}] "
        f"{unit_map[plane]}"
    )

    ax.set_ylabel(ylabel)

    for Z, color in zip(values, colors):
        ax.fill_between(
            frequency,
            Z,
            color=color,
            alpha=1,
        )

    legend_patches = [
        mpatches.Patch(color=color, label=label)
        for color, label in zip(colors, labels)
    ]

    ax.legend(
        handles=legend_patches,
        loc="upper right",
        bbox_to_anchor=(1.015, 1.02),
    )

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

    ax.set_yscale("log")
    ax.set_xscale("linear")

    ax.yaxis.set_major_locator(
        LogLocator(
            base=10.0,
            subs=(1.0,),
            numticks=8,
        )
    )

    ax.yaxis.set_minor_locator(
        LogLocator(
            base=10.0,
            subs=np.arange(2, 10) * 0.1,
            numticks=40,
        )
    )

    ax.tick_params(
        axis="y",
        which="minor",
        length=1.5,
        width=0.3,
    )

    fig.subplots_adjust(
        left=0.12,
        right=0.93,
        bottom=0.15,
        top=0.92,
    )

    filename = (
        f"Z_{plane}_{part}_log_area.jpg"
    )

    if save and image_folder is not None:
        fig.savefig(
            image_folder / filename,
            dpi=300,
            bbox_inches="tight",
        )

    if show:
        plt.show()

    return fig, ax


# ============================================================
# PLOT TOTAL DIPOLE IMPEDANCE
# ============================================================

def plot_dipoles(
    freq_x,
    Zx,
    freq_y,
    Zy,
    part="real",
    image_folder=None,
    scale="linear",
    xlim=(1e-3, 20),
    figsize=(7, 5),
    show=True,
    save=True,
):
    """
    Plot total horizontal and vertical dipolar impedance.
    """

    if part not in ["real", "imag"]:
        raise ValueError(
            "part must be 'real' or 'imag'"
        )

    if scale not in ["log", "linear"]:
        raise ValueError(
            "scale must be 'log' or 'linear'"
        )

    set_plot_style()

    if image_folder is not None:
        image_folder = Path(image_folder)
        image_folder.mkdir(parents=True, exist_ok=True)

    plt.close("all")

    fig, ax = plt.subplots(figsize=figsize)

    ax.set_xlabel("f (GHz)")

    if part == "real":
        yx = Zx.real
        yy = Zy.real
        ylabel = r"Re[$Z_{dip}$] ($\Omega$/m)"
        name_part = "Re"

    else:
        yx = Zx.imag
        yy = Zy.imag
        ylabel = r"Im[$Z_{dip}$] ($\Omega$/m)"
        name_part = "Im"

    ax.set_ylabel(ylabel)

    ax.plot(
        freq_x,
        yx,
        lw=2,
        label=r"$Z_x$ dipole",
    )

    ax.plot(
        freq_y,
        yy,
        lw=2,
        label=r"$Z_y$ dipole",
    )

    ax.set_xlim(*xlim)

    ax.set_yscale(scale)
    ax.set_xscale("linear")

    if scale == "log":
        ax.yaxis.set_major_locator(
            LogLocator(base=10.0)
        )

        ax.yaxis.set_minor_locator(
            LogLocator(
                base=10.0,
                subs=np.arange(2, 10) * 0.1,
            )
        )

    ax.legend()

    fig.subplots_adjust(
        left=0.12,
        right=0.93,
        bottom=0.15,
        top=0.92,
    )

    filename = (
        f"Z_total_dipole_{name_part}_{scale}.jpg"
    )

    if save and image_folder is not None:
        fig.savefig(
            image_folder / filename,
            dpi=300,
            bbox_inches="tight",
        )

    if show:
        plt.show()

    return fig, ax


# ============================================================
# PLOT TOTAL LONGITUDINAL IMPEDANCE
# ============================================================

def plot_longitudinal(
    freq,
    Z,
    part="real",
    image_folder=None,
    scale="linear",
    xlim=(1e-3, 20),
    figsize=(7, 5),
    show=True,
    save=True,
):
    """
    Plot total longitudinal impedance.
    """

    if part not in ["real", "imag"]:
        raise ValueError(
            "part must be 'real' or 'imag'"
        )

    if scale not in ["log", "linear"]:
        raise ValueError(
            "scale must be 'log' or 'linear'"
        )

    set_plot_style()

    if image_folder is not None:
        image_folder = Path(image_folder)
        image_folder.mkdir(parents=True, exist_ok=True)

    plt.close("all")

    fig, ax = plt.subplots(figsize=figsize)

    ax.set_xlabel("f (GHz)")

    if part == "real":
        y = Z.real
        ylabel = r"Re[$Z_{long}$] ($\Omega$)"
        name_part = "Re"

    else:
        y = Z.imag
        ylabel = r"Im[$Z_{long}$] ($\Omega$)"
        name_part = "Im"

    ax.set_ylabel(ylabel)

    ax.plot(
        freq,
        y,
        lw=2,
        label=r"$Z_{long}$",
    )

    ax.set_xlim(*xlim)

    ax.set_yscale(scale)
    ax.set_xscale("linear")

    if scale == "log":
        ax.yaxis.set_major_locator(
            LogLocator(base=10.0)
        )

        ax.yaxis.set_minor_locator(
            LogLocator(
                base=10.0,
                subs=np.arange(2, 10) * 0.1,
            )
        )

    ax.legend()

    fig.subplots_adjust(
        left=0.12,
        right=0.93,
        bottom=0.15,
        top=0.92,
    )

    filename = (
        f"Z_total_longitudinal_{name_part}_{scale}.jpg"
    )

    if save and image_folder is not None:
        fig.savefig(
            image_folder / filename,
            dpi=300,
            bbox_inches="tight",
        )

    if show:
        plt.show()

    return fig, ax


def read_total_impedance(folder,filename):
    """
    Read the total impedance file containing all impedance components.

    Expected file format:

        # f_GHz    Zlong[Ohm]    Zxdip[Ohm/m]    Zydip[Ohm/m]
        #          Zxquad[Ohm/m] Zyquad[Ohm/m]

    Example:
        0.000000e+00   -1.61e+03+...j   4.83e-08+...j   ...

    Parameters
    ----------
    folder : str or Path
        Folder containing the total impedance file.

    Returns
    -------
    freq : ndarray
        Frequency in GHz.

    Zlong : ndarray
        Total longitudinal impedance [Ohm].

    Zxdip : ndarray
        Total horizontal dipolar impedance [Ohm/m].

    Zydip : ndarray
        Total vertical dipolar impedance [Ohm/m].

    Zxquad : ndarray
        Total horizontal quadrupolar impedance [Ohm/m].

    Zyquad : ndarray
        Total vertical quadrupolar impedance [Ohm/m].
    """

    folder = Path(folder)

    # Expected total impedance file
    file = folder / filename

    if not file.exists():
        raise FileNotFoundError(
            f"Total impedance file not found:\n"
            f"  {file.resolve()}"
        )

    # Read the file as strings because the impedance
    # columns are stored directly as complex numbers,
    # e.g. 1.23e+03+4.56e+02j
    data = np.loadtxt(
        file,
        comments="#",
        dtype=str,
    )

    # Frequency
    freq = data[:, 0].astype(float)

    # Complex impedance columns
    Zlong = data[:, 1].astype(complex)
    Zxdip = data[:, 2].astype(complex)
    Zydip = data[:, 3].astype(complex)
    Zxquad = data[:, 4].astype(complex)
    Zyquad = data[:, 5].astype(complex)

    return (
        freq,
        Zlong,
        Zxdip,
        Zydip,
        Zxquad,
        Zyquad,
    )

    # ============================================================
# SUM SELECTED IMPEDANCES
# ============================================================

def sum_selected_impedances(
    devices,
    selected_devices,
):
    """
    Sum the impedance of selected devices.

    Devices that are not present in `devices` are assumed to have
    zero impedance. This is useful for quadrupolar planes (`quadx`,
    `quady`) when a device has no quadrupolar impedance contribution.

    Parameters
    ----------
    devices : dict
        Dictionary returned by read_impedance_devices().

    selected_devices : list of str
        Names of the devices to include.

    Returns
    -------
    Z_sum : ndarray
        Complex summed impedance.

    Notes
    -----
    All available device impedances must already be on the same
    frequency grid.

    Missing devices contribute zero.
    """

    if len(selected_devices) == 0:
        raise ValueError(
            "selected_devices is empty."
        )

    # --------------------------------------------------------
    # Find the first device that is actually available
    # --------------------------------------------------------

    available_devices = [
        name
        for name in selected_devices
        if name in devices
    ]

    if len(available_devices) == 0:
        raise KeyError(
            "None of the selected devices are available in `devices`."
        )

    # --------------------------------------------------------
    # Initialize sum using an available device
    # --------------------------------------------------------

    first_device = available_devices[0]

    Z_sum = np.zeros_like(
        devices[first_device],
        dtype=complex,
    )

    # --------------------------------------------------------
    # Sum selected devices
    # Missing devices contribute zero
    # --------------------------------------------------------

    for name in selected_devices:

        if name not in devices:
            print(
                f"WARNING: '{name}' not available. "
                "Assuming zero impedance."
            )
            continue

        Z_sum += devices[name]

    return Z_sum
# ============================================================
# SAVE TOTAL IMPEDANCE
# ============================================================

# ============================================================
# SAVE TOTAL IMPEDANCE
# ============================================================

def save_total_impedance(
    folder,
    selected_components,
    freq,
    Zlong,
    Zxdip,
    Zydip,
    Zxquad,
    Zyquad,
):
    """
    Save the total impedance obtained from the selected components.

    The filename is automatically generated from the selected
    components:

        Ztotal_<component1>_<component2>_....txt

    Example
    -------
    selected_components = [
        "pipe_rw",
        "coll3cm",
        "kickers_optimized",
        "RF",
    ]

    Output:
        Ztotal_pipe_rw_coll3cm_kickers_optimized_RF.txt
    """

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    if len(selected_components) == 0:
        raise ValueError("selected_components is empty.")

    filename = "Ztotal_" + "_".join(selected_components) + ".txt"
    file = folder / filename

    data = np.column_stack([
        freq,
        Zlong,
        Zxdip,
        Zydip,
        Zxquad,
        Zyquad,
    ])

    header = (
        "f_GHz\t"
        "Zlong[Ohm]\t"
        "Zxdip[Ohm/m]\t"
        "Zydip[Ohm/m]\t"
        "Zxquad[Ohm/m]\t"
        "Zyquad[Ohm/m]"
    )

    np.savetxt(
        file,
        data,
        fmt=[
            "%.12e",
            "%+.12e%+.12ej",
            "%+.12e%+.12ej",
            "%+.12e%+.12ej",
            "%+.12e%+.12ej",
            "%+.12e%+.12ej",
        ],
        delimiter="\t",
        header=header,
        comments="# ",
    )

    print("Total impedance saved to:")
    print(f"  {file.resolve()}")

    return file

def save_total_impedance_test(
    folder,
    selected_components,
    freq,
    Zlong,
    Zxdip,
    Zydip,
    Zxquad,
    Zyquad,
):
    """
    Save the total impedance obtained from the selected components.

    The filename is automatically generated from the selected
    components:

        Ztotal_<component1>_<component2>_....txt

    Example
    -------
    selected_components = [
        "pipe_rw",
        "coll3cm",
        "kickers_optimized",
        "RF",
    ]

    Output:
        Ztotal_pipe_rw_coll3cm_kickers_optimized_RF.txt
    """

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    if len(selected_components) == 0:
        raise ValueError("selected_components is empty.")

    filename = "Ztotal_" + "_".join(selected_components) + ".txt"
    file = folder / filename

    freq = np.asarray(freq)
    Zlong = np.asarray(Zlong, dtype=complex)
    Zxdip = np.asarray(Zxdip, dtype=complex)
    Zydip = np.asarray(Zydip, dtype=complex)
    Zxquad = np.asarray(Zxquad, dtype=complex)
    Zyquad = np.asarray(Zyquad, dtype=complex)

    header = (
        "f_GHz\t"
        "Zlong[Ohm]\t"
        "Zxdip[Ohm/m]\t"
        "Zydip[Ohm/m]\t"
        "Zxquad[Ohm/m]\t"
        "Zyquad[Ohm/m]"
    )

    with open(file, "w") as f:
        f.write("# " + header + "\n")
        for i in range(len(freq)):
            row = (
                f"{freq[i]:.12e}\t"
                f"{Zlong[i].real:+.12e}{Zlong[i].imag:+.12e}j\t"
                f"{Zxdip[i].real:+.12e}{Zxdip[i].imag:+.12e}j\t"
                f"{Zydip[i].real:+.12e}{Zydip[i].imag:+.12e}j\t"
                f"{Zxquad[i].real:+.12e}{Zxquad[i].imag:+.12e}j\t"
                f"{Zyquad[i].real:+.12e}{Zyquad[i].imag:+.12e}j"
            )
            f.write(row + "\n")

    print("Total impedance saved to:")
    print(f"  {file.resolve()}")

    return file

def load_total_impedance(file):
    """
    Load a Ztotal_*.txt file produced by save_total_impedance.

    Returns
    -------
    freq, Zlong, Zxdip, Zydip, Zxquad, Zyquad : ndarray
        freq is real, the others are complex.
    """
    file = Path(file)

    freq, Zlong, Zxdip, Zydip, Zxquad, Zyquad = [], [], [], [], [], []

    with open(file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            freq.append(float(parts[0]))
            Zlong.append(complex(parts[1]))
            Zxdip.append(complex(parts[2]))
            Zydip.append(complex(parts[3]))
            Zxquad.append(complex(parts[4]))
            Zyquad.append(complex(parts[5]))

    return (
        np.array(freq),
        np.array(Zlong, dtype=complex),
        np.array(Zxdip, dtype=complex),
        np.array(Zydip, dtype=complex),
        np.array(Zxquad, dtype=complex),
        np.array(Zyquad, dtype=complex),
    )



def plot_total_impedance(
    frequency,
    Zlong,
    Zxdip,
    Zydip,
    Zxquad,
    Zyquad,
    filename=None,
    image_folder=None,
    xlim=None,
    ylim=None,
    show=True,
    save=True,
):
    """
    Plot the total impedance.

    Three figures are produced:
        1. Longitudinal impedance
        2. Dipolar impedance
        3. Quadrupolar impedance

    Parameters
    ----------
    frequency : ndarray
        Frequency grid [GHz].

    Zlong : ndarray
        Total longitudinal impedance [Ohm].

    Zxdip : ndarray
        Total horizontal dipolar impedance [Ohm/m].

    Zydip : ndarray
        Total vertical dipolar impedance [Ohm/m].

    Zxquad : ndarray
        Total horizontal quadrupolar impedance [Ohm/m].

    Zyquad : ndarray
        Total vertical quadrupolar impedance [Ohm/m].

    filename : str, optional
        Name of the total impedance file.
        Used to identify the plots.

    image_folder : str or Path, optional
        Folder where plots are saved.

    xlim : tuple, optional
        Frequency limits, e.g. (1e-3, 10).

    show : bool
        Show the plots.

    save : bool
        Save the plots.
    """

    if save:
        if image_folder is None:
            raise ValueError(
                "image_folder must be provided when save=True."
            )

        image_folder = Path(image_folder)
        image_folder.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Name used for saved plots
    # --------------------------------------------------------

    if filename is not None:
        plot_name = Path(filename).stem
    else:
        plot_name = "total_impedance"

    # ========================================================
    # LONGITUDINAL
    # ========================================================

    fig, ax = plt.subplots(figsize=(7,5))

    ax.plot(
        frequency,
        np.real(Zlong),
        label="Re(Zlong)",
    )

    ax.plot(
        frequency,
        np.imag(Zlong),
        label="Im(Zlong)",
    )

    ax.set_xlabel("Frequency [GHz]")
    ax.set_ylabel("Longitudinal impedance [Ohm]")
    ax.set_title("Total Longitudinal Impedance")

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    ax.grid(True, which="both", alpha=0.3)
    ax.legend()

    fig.tight_layout()

    if save:
        fig.savefig(
            image_folder / f"{plot_name}_longitudinal.png",
            dpi=300,
            bbox_inches="tight",
        )

    if show:
        plt.show()
    else:
        plt.close(fig)

    # ========================================================
    # DIPOLE
    # ========================================================

    fig, ax = plt.subplots(figsize=(7,5))

    ax.plot(
        frequency,
        np.real(Zxdip),
        label="Re(Zxdip)",
    )

    ax.plot(
        frequency,
        np.imag(Zxdip),
        label="Im(Zxdip)",
    )

    ax.plot(
        frequency,
        np.real(Zydip),
        label="Re(Zydip)",
    )

    ax.plot(
        frequency,
        np.imag(Zydip),
        label="Im(Zydip)",
    )

    ax.set_xlabel("Frequency [GHz]")
    ax.set_ylabel("Dipolar impedance [Ohm/m]")
    ax.set_title("Total Dipolar Impedance")

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    ax.grid(True, which="both", alpha=0.3)
    ax.legend()

    fig.tight_layout()

    if save:
        fig.savefig(
            image_folder / f"{plot_name}_dipolar.png",
            dpi=300,
            bbox_inches="tight",
        )

    if show:
        plt.show()
    else:
        plt.close(fig)

    # ========================================================
    # QUADRUPOLE
    # ========================================================

    fig, ax = plt.subplots(figsize=(7,5))
    #
    ax.plot(
         frequency,
         np.real(Zxquad),
         label="Re(Zxquad)",
    )
    
    ax.plot(
         frequency,
        np.imag(Zxquad),
         label="Im(Zxquad)",
    )
    
    ax.plot(
         frequency,
         np.real(Zyquad),
         label="Re(Zyquad)",
    )
    
    ax.plot(
         frequency,
         np.imag(Zyquad),
         label="Im(Zyquad)",
    )
    
    #
    ax.set_xlabel("Frequency [GHz]")
    ax.set_ylabel("Quadrupolar impedance [Ohm/m]")
    ax.set_title("Total Quadrupolar Impedance")
    
    if xlim is not None:
         ax.set_xlim(xlim)
    if ylim is not None:
         ax.set_ylim(ylim)
    
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    
    fig.tight_layout()
    
    if save:
         fig.savefig(
             image_folder / f"{plot_name}_quadrupolar.png",
             dpi=300,
             bbox_inches="tight",
         )
    
    if show:
        plt.show()
    else:
        plt.close(fig)

