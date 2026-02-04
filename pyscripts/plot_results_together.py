#!/usr/bin/env python3

import argparse
import pandas as pd
import matplotlib.pyplot as plt

def set_default_plt_settings():
    """
    Description
    -----------
    Set plt.rc parameters for font sizes and family and tick font size and tick length and direction
    in a nice format.
    """

    # Use LaTeX for text rendering
    plt.rcParams["text.usetex"] = True

    # Set font sizes
    plt.rc("font", size=25)  # controls default text size
    plt.rc("axes", titlesize=50)  # fontsize of the title
    plt.rc("axes", labelsize=50)  # fontsize of the x and y labels
    plt.rc("xtick", labelsize=25)  # fontsize of the x tick labels
    plt.rc("ytick", labelsize=25)  # fontsize of the y tick labels
    plt.rc("legend", fontsize=25)  # fontsize of the legend

    # Get some nicer plot settings
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["figure.autolayout"] = True

    # Set tick parameters
    plt.tick_params(
        direction="out",
        bottom=True,
        top=True,
        left=True,
        right=True,
        length=10,
        width=1,
    )



def load_csv(path):
    """
    Load a CSV expected to have columns: x, y, yerr
    """
    df = pd.read_csv(path)
    required = {"x", "y", "yerr"}
    if not required.issubset(df.columns):
        raise ValueError(f"{path} must contain columns: x, y, yerr")
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Plot two CSV datasets with an optional x-offset for the second dataset."
    )
    parser.add_argument("csv1", help="Path to first CSV file")
    parser.add_argument("csv2", help="Path to second CSV file")
    parser.add_argument(
        "--delta",
        type=float,
        default=0.0,
        help="Offset applied to x-values of the second dataset (default: 0.0)",
    )
    parser.add_argument(
        "--output",
        help="Optional path to save the figure instead of showing it",
    )
    parser.add_argument(
        "--label1",
        help="Optional label for the first dataset (legend)",
        default="Dataset 1",
    )
    parser.add_argument(
        "--label2",
        help="Optional label for the second dataset (legend)",
        default=None,
    )
    parser.add_argument(
        "--ylabel",
        help="Optional y-axis label (LaTeX allowed)",
        default="$\\delta A_{UL}$",
    )
    parser.add_argument(
        "--plot-uncertainty-ratio",
        help="If set, create a second plot showing the ratio of uncertainties (yerr2/yerr1)",
        action="store_true",
    )
    parser.add_argument(
        "--scale-yerr1",
        type=float,
        default=1.0,
        help="Scale factor applied to yerr of first dataset",
    )
    parser.add_argument(
        "--scale-yerr2",
        type=float,
        default=1.0,
        help="Scale factor applied to yerr of second dataset",
    )
    parser.add_argument(
        "--set-y1",
        type=float,
        default=None,
        help="Set all y values of the first dataset to this constant (overrides CSV y)",
    )
    parser.add_argument(
        "--set-y2",
        type=float,
        default=None,
        help="Set all y values of the second dataset to this constant (overrides CSV y)",
    )

    args = parser.parse_args()

    # Set matplotlib settings
    set_default_plt_settings()

    # Load data
    df1 = load_csv(args.csv1)
    df2 = load_csv(args.csv2)

    # Apply uncertainty scale factors
    if args.scale_yerr1 != 1.0:
        df1 = df1.copy()
        df1["yerr"] = df1["yerr"] * args.scale_yerr1
    if args.scale_yerr2 != 1.0:
        df2 = df2.copy()
        df2["yerr"] = df2["yerr"] * args.scale_yerr2

    # Optionally set y values to a constant for either dataset
    if args.set_y1 is not None:
        df1 = df1.copy()
        df1["y"] = float(args.set_y1)
    if args.set_y2 is not None:
        df2 = df2.copy()
        df2["y"] = float(args.set_y2)

    # Apply offset to second dataset
    x2_offset = df2["x"] + args.delta

    # Plot main comparison
    plt.figure(figsize=(16, 10))
    label1 = args.label1
    label2 = args.label2 if args.label2 is not None else f"Dataset 2 (x offset = {args.delta})"
    plt.errorbar(
        df1["x"],
        df1["y"],
        yerr=df1["yerr"],
        fmt="o",
        markersize=20,
        ecolor='black',
        elinewidth=2.0,
        capsize=18,
        capthick=2.0,
        label=label1,
    )
    plt.errorbar(
        x2_offset,
        df2["y"],
        yerr=df2["yerr"],
        fmt="s",
        markersize=20,
        ecolor='black',
        elinewidth=2.0,
        capsize=18,
        capthick=2.0,
        label=label2,
    )
    plt.xlim(0.0,1.0)
    plt.xlabel("$x$", usetex=True)
    plt.ylabel(args.ylabel, usetex=True)
    plt.legend(loc='best', frameon=False)
    plt.tight_layout()

    # Save/show main plot
    if args.output:
        plt.savefig(args.output, dpi=300)
    else:
        plt.show()

    # Optional: plot ratio of uncertainties (yerr2 / yerr1)
    if args.plot_uncertainty_ratio:
        # Match x points by nearest neighbor between df1.x and df2.x (after offset)
        x1 = df1["x"].to_numpy()
        yerr1 = df1["yerr"].to_numpy()
        x2 = x2_offset.to_numpy()
        yerr2 = df2["yerr"].to_numpy()

        # For each x1 find nearest index in x2
        import numpy as np

        idx2_for_x1 = np.array([np.argmin(np.abs(x2 - xv)) for xv in x1])
        matched_x2 = x2[idx2_for_x1]
        matched_yerr2 = yerr2[idx2_for_x1]

        # Compute safe ratio, avoid divide-by-zero
        ratio = np.full_like(matched_yerr2, np.nan, dtype=float)
        mask_nonzero = yerr1 != 0
        ratio[mask_nonzero] = matched_yerr2[mask_nonzero] / yerr1[mask_nonzero]

        plt.figure(figsize=(16,10))
        plt.xlim(0.0,1.0)
        plt.axhline(1.0, color="0.6", linestyle="--", label="ratio = 1")
        plt.plot(x1, ratio, marker="o", markersize=20,
        linestyle="-", label=f"Uncertainty ratio {label2} / {label1}")
        plt.xlabel("$x$", usetex=True)
        plt.ylabel(f"Uncertainty ratio")
        plt.legend(loc="best", frameon=False)
        plt.tight_layout()
        if args.output:
            # derive output name by appending suffix
            outpath = args.output
            if outpath.lower().endswith(".png") or outpath.lower().endswith(".pdf"):
                base, ext = outpath.rsplit(".", 1)
                out_unc = f"{base}_unc_ratio.{ext}"
            else:
                out_unc = f"{outpath}_unc_ratio.pdf"
            plt.savefig(out_unc, dpi=300)
        else:
            plt.show()


if __name__ == "__main__":
    main()
