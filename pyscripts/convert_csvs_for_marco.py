#!/usr/bin/env python3

import argparse
import pandas as pd
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge two CSV files by bin with renamed columns."
    )
    parser.add_argument(
        "input_csv1",
        help="Path to first input CSV file (rgc)"
    )
    parser.add_argument(
        "input_csv2",
        help="Path to second input CSV file (rgh)"
    )
    parser.add_argument(
        "-o", "--output",
        default="merged_output.csv",
        help="Path to output CSV file (default: merged_output.csv)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Read input CSV files
    try:
        df1 = pd.read_csv(args.input_csv1)
        df2 = pd.read_csv(args.input_csv2)
    except Exception as e:
        print(f"Error reading input files: {e}")
        sys.exit(1)

    # Expected columns
    required_cols1 = ["bin", "count", "x", "y", "xerr", "yerr", "xerrsyst", "yerrsyst"]
    required_cols2 = ["bin", "count", "x", "y", "xerr", "yerr", "acceptanceratio", "scaling"]

    for col in required_cols1:
        if col not in df1.columns:
            print(f"Missing column '{col}' in first CSV")
            sys.exit(1)

    for col in required_cols2:
        if col not in df2.columns:
            print(f"Missing column '{col}' in second CSV")
            sys.exit(1)

    # Select and rename columns from CSV 1
    df1_selected = df1[["bin", "count", "x", "y", "yerr"]].copy()
    df1_selected.rename(columns={
        "count": "count_rgc",
        "x": "x_rgc",
        "y": "y_rgc",
        "yerr": "yerr_rgc"
    }, inplace=True)

    # Select and rename columns from CSV 2
    df2_selected = df2[["bin", "count", "x", "yerr", "acceptanceratio"]].copy()
    df2_selected.rename(columns={
        "count": "count_rgh",
        "x": "x_rgh",
        "yerr": "yerr_rgh"
    }, inplace=True)

    # Merge on 'bin'
    merged = pd.merge(df1_selected, df2_selected, on="bin", how="inner")

    # Reorder columns explicitly
    final_columns = [
        "bin",
        "count_rgc", "x_rgc", "y_rgc", "yerr_rgc",
        "count_rgh", "x_rgh", "yerr_rgh",
        "acceptanceratio"
    ]

    merged = merged[final_columns]

    # Write output
    try:
        merged.to_csv(args.output, index=False)
        print(f"Successfully wrote merged CSV to: {args.output}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
