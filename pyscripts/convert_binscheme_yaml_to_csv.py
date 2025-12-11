#!/usr/bin/env python3
import argparse
import yaml
import csv
import sys
import math
from decimal import Decimal

def format_sigfigs(value, sigfigs):
    """Format number to N significant figures and KEEP trailing zeros."""
    if value == "" or value is None:
        return value

    try:
        # Convert using Decimal for precise representation
        d = Decimal(str(value))
    except Exception:
        return value
    
    # Handle zero separately (Decimal cannot quantize 0 directly by sig figs)
    if d == 0:
        return "0." + "0"*(sigfigs)

    # Determine exponent = floor(log10(|d|))
    exponent = d.adjusted()

    # Number of decimals to keep
    places = sigfigs - exponent - 1

    # Quantize to the desired number of decimal places
    quant = Decimal("1e{}".format(-places))
    d_q = d.quantize(quant)

    # Convert to string (Decimal keeps trailing zeros)
    return format(d_q, "f") if exponent >= -6 else format(d_q, "E")

def main():
    parser = argparse.ArgumentParser(description="Convert YAML 1D bin definitions to CSV.")
    parser.add_argument("yaml_file", help="Input YAML file")
    parser.add_argument("--csv_file", default=None, help="Output CSV file")
    parser.add_argument("--entries", nargs="+", default=None,
                        help="Top-level YAML entries to extract (e.g. --entries x y z)")
    parser.add_argument("--sigfigs", type=int, default=None,
                        help="Number of significant figures for numeric CSV output")
    args = parser.parse_args()

    # Load YAML
    with open(args.yaml_file, "r") as f:
        data = yaml.safe_load(f)

    # Extract bin arrays for requested entries
    bins_dict = {}
    max_bins = 0

    keys_obj = args.entries if args.entries is not None else data
    for entry in keys_obj:
        if entry not in data:
            print(f"Warning: entry '{entry}' not found in YAML.", file=sys.stderr)
            continue
        
        subkeys = list(data[entry].keys())
        if len(subkeys) != 1:
            raise ValueError(
                f"Entry '{entry}' must contain exactly one subkey, found {subkeys}"
            )
        
        subkey = subkeys[0]
        arr = data[entry][subkey]

        if not isinstance(arr, list) or len(arr) < 2:
            raise ValueError(f"Entry '{entry}' does not contain a valid bin limit array.")

        bins_dict[entry] = arr
        max_bins = max(max_bins, len(arr) - 1)  # number of bins = N-1

    # Build CSV
    header = ["bin"]
    for entry in keys_obj:
        if entry in bins_dict:
            header.extend([f"{entry.split('_')[0]}binlo", f"{entry.split('_')[0]}binhi"])

    rows = []

    for i in range(max_bins):
        row = [i]
        for entry in keys_obj:
            if entry in bins_dict:
                arr = bins_dict[entry]
                if i < len(arr) - 1:
                    low = arr[i]
                    high = arr[i + 1]
                else:
                    low = ""
                    high = ""

                # Apply sigfig formatting if requested
                if args.sigfigs is not None:
                    low = format_sigfigs(low, args.sigfigs)
                    high = format_sigfigs(high, args.sigfigs)

                row.extend([low, high])
        rows.append(row)

    # Write CSV
    outpath = args.yaml_file.replace('.yaml','.csv').replace('.yml','csv')
    with open(outpath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == "__main__":
    main()
