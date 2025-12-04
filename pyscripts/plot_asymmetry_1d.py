#!/usr/bin/env python3

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Plot asymmetry vs bin variable from a CSV file. "
                    "CSV file name must have form <prefix>_<binvar>.csv"
    )

    parser.add_argument("csvfile", help="Path to the input CSV file")

    parser.add_argument(
        "--prefix",
        default="out_",
        help="Expected prefix in the CSV filename (default: out_)"
    )

    parser.add_argument(
        "--asym",
        default="a0",
        help="Asymmetry column name (default: a0)"
    )

    args = parser.parse_args()

    # Extract components of the filename
    fname = os.path.basename(args.csvfile)

    # Ensure it ends with .csv
    if not fname.endswith(".csv"):
        raise ValueError(f"Input filename must end with .csv, got {fname}")

    # Remove .csv
    core = fname[:-4]

    # Check prefix
    if not core.startswith(args.prefix):
        raise ValueError(
            f"Filename '{fname}' does not start with prefix '{args.prefix}'. "
            f"Expected format: {args.prefix}<binvar>.csv"
        )

    # Extract binvar from the filename
    binvar = core[len(args.prefix):]

    # Construct expected column names
    binvar_err = f"{binvar}_err"
    asym = args.asym
    asym_err = f"{asym}_err"

    # Load CSV
    df = pd.read_csv(args.csvfile)

    # Column validation
    required_cols = [binvar, binvar_err, asym, asym_err]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in CSV.")

    # Plot
    plt.errorbar(
        df[binvar],
        df[asym],
        xerr=df[binvar_err],
        yerr=df[asym_err],
        fmt='o',
        ecolor='black',
        capsize=3
    )

    plt.xlabel(binvar)
    plt.ylabel(asym)
    plt.title(f"{asym} vs {binvar}")
    plt.grid(True)

    # Save to a PDF with .pdf appended
    outpdf = args.csvfile + ".pdf"
    plt.savefig(outpdf)
    print(f"Saved plot to {outpdf}")


if __name__ == "__main__":
    main()
