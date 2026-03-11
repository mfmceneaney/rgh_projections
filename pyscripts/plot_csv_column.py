#!/usr/bin/env python3

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import re
import itertools

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

def resolve_files(patterns):
    """Resolve file patterns (glob or regex) into file paths."""
    files = set()

    for p in patterns:
        g = glob.glob(p)
        if g:
            files.update(g)
            continue

        regex = re.compile(p)
        for f in os.listdir("."):
            if regex.match(f):
                files.add(f)

    return sorted(files)


def cycle_or_default(values, default):
    """Return infinite cycle of values or a single default."""
    if values:
        return itertools.cycle(values)
    return itertools.cycle([default])


def plot_columns(file, xcols, ycols, labels, markers, linestyles,
                 xlim, ylim, xlabel, ylabel, normalize, title, alpha, markersize):

    df = pd.read_csv(file)

    for col in xcols + ycols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in {file}")

    marker_cycle = cycle_or_default(markers, None)
    linestyle_cycle = cycle_or_default(linestyles, "-")

    set_default_plt_settings()

    plt.figure(figsize=(16,10))

    for i, (xcol, ycol) in enumerate(zip(xcols, ycols)):
        x = df[xcol]
        y = df[ycol].astype(float)

        if normalize:
            total = y.sum()
            if total != 0:
                y = y / total

        if labels and i < len(labels):
            label = labels[i]
        else:
            label = f"{ycol} vs {xcol}"

        marker = next(marker_cycle)
        linestyle = next(linestyle_cycle)

        plt.plot(
            x,
            y,
            label=label,
            marker=marker,
            linestyle=linestyle,
            alpha=alpha,
            markersize=markersize,
        )

    if xlim:
        plt.xlim(xlim)

    if ylim:
        plt.ylim(ylim)

    plt.xlabel(xlabel if xlabel else xcols[0])
    plt.ylabel(ylabel if ylabel else ("Normalized Value" if normalize else "Value"))

    plt.title(title if title else os.path.basename(file), usetex=True, pad=20)

    plt.legend()

    outname = os.path.splitext(file)[0] + "_multi_plot.pdf"
    plt.savefig(outname)
    plt.close()

    print(f"Saved {outname}")


def main():
    parser = argparse.ArgumentParser(
        description="Plot multiple (x,y) column pairs from CSV files"
    )

    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input CSV filenames, glob patterns, or regex patterns",
    )

    parser.add_argument(
        "--xcols",
        nargs="+",
        required=True,
        help="Column names for x-axis data",
    )

    parser.add_argument(
        "--ycols",
        nargs="+",
        required=True,
        help="Column names for y-axis data",
    )

    parser.add_argument(
        "--labels",
        nargs="+",
        help="Optional legend labels for each curve",
    )

    parser.add_argument(
        "--markers",
        nargs="+",
        help="Marker styles for curves (e.g. o s ^ d x)",
    )

    parser.add_argument(
        "--linestyles",
        nargs="+",
        help="Line styles for curves (e.g. - -- -. :)",
    )

    parser.add_argument(
        "--xlim",
        nargs=2,
        type=float,
        metavar=("XMIN", "XMAX"),
        help="X-axis limits",
    )

    parser.add_argument(
        "--ylim",
        nargs=2,
        type=float,
        metavar=("YMIN", "YMAX"),
        help="Y-axis limits",
    )

    parser.add_argument(
        "--xlabel",
        help="X-axis label (can include LaTeX)",
    )

    parser.add_argument(
        "--ylabel",
        help="Y-axis label (can include LaTeX)",
    )

    parser.add_argument(
        "--title",
        help="Plot title (can include LaTeX)",
    )

    parser.add_argument(
        "--alpha",
        type=float,
        default=1.0,
        help="Transparency of plotted lines (0.0–1.0, default=1.0)",
    )

    parser.add_argument(
        "--markersize",
        type=float,
        default=None,
        help="Size of the plot markers (default: matplotlib default)",
    )

    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Normalize each y dataset by its sum",
    )

    args = parser.parse_args()

    if len(args.xcols) != len(args.ycols):
        raise ValueError("Number of --xcols must match number of --ycols")

    files = resolve_files(args.inputs)

    if not files:
        print("No files matched input patterns.")
        return

    for f in files:
        try:
            plot_columns(
                f,
                args.xcols,
                args.ycols,
                args.labels,
                args.markers,
                args.linestyles,
                args.xlim,
                args.ylim,
                args.xlabel,
                args.ylabel,
                args.normalize,
                args.title,
                args.alpha,
                args.markersize,
            )
        except Exception as e:
            print(f"Error processing {f}: {e}")


if __name__ == "__main__":
    main()
