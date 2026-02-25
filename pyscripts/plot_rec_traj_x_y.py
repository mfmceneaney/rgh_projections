#!/usr/bin/env python3

import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import hipopy.hipopy as hipopy
import awkward as ak

import saga.plot as sagap
sagap.set_default_plt_settings()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Read REC::Traj bank and plot x-y distribution with MC matching and particle info."
    )

    parser.add_argument("input", nargs="?", default=None,
                        help="Input HIPO file path or glob pattern")
    parser.add_argument("--output", default="traj_xy.pdf",
                        help="Output PDF filename")
    parser.add_argument("--bins", type=int, default=200,
                        help="Number of bins")
    parser.add_argument("--save", default="traj_xy_data.npz",
                        help="Save extracted data (.npz or .csv)")
    parser.add_argument("--load", default=None,
                        help="Load saved data instead of reading HIPO")

    # Plot titles and axis titles
    parser.add_argument("--title", type=str)
    parser.add_argument("--xtitle", type=str)
    parser.add_argument("--ytitle", type=str)

    # Axis limits
    parser.add_argument("--xmin", type=float)
    parser.add_argument("--xmax", type=float)
    parser.add_argument("--ymin", type=float)
    parser.add_argument("--ymax", type=float)

    # Detector / layer selection
    parser.add_argument("--detector", type=int,
                        help="Select detector ID")
    parser.add_argument("--layer", type=int,
                        help="Select layer ID")

    # MC filter: zero / nonzero
    parser.add_argument("--mczero", choices=["zero", "nonzero"],
                        help="Filter hits by MC index being zero or nonzero")

    # Particle selection
    parser.add_argument("--pid", type=int,
                        help="Select hits corresponding to particle PID")
    parser.add_argument("--charge", type=int,
                        help="Select hits corresponding to particle charge")

    return parser.parse_args()


def filter_finite(x, y, detector, layer, pindex, mcindex, pid, charge):
    mask = np.isfinite(x) & np.isfinite(y)
    removed = len(x) - np.count_nonzero(mask)
    if removed > 0:
        print(f"Removed {removed} non-finite (NaN/Inf) entries")
    return x[mask], y[mask], detector[mask], layer[mask], pindex[mask], mcindex[mask], pid[mask], charge[mask]


def apply_limits(x, y, detector, layer, pindex, mcindex, pid, charge, xmin, xmax, ymin, ymax):
    mask = np.ones(len(x), dtype=bool)
    if xmin is not None:
        mask &= x >= xmin
    if xmax is not None:
        mask &= x <= xmax
    if ymin is not None:
        mask &= y >= ymin
    if ymax is not None:
        mask &= y <= ymax
    removed = len(x) - np.count_nonzero(mask)
    if removed > 0:
        print(f"Removed {removed} entries outside limits")
    return x[mask], y[mask], detector[mask], layer[mask], pindex[mask], mcindex[mask], pid[mask], charge[mask]


def apply_selection(x, y, detector, layer, pindex, mcindex, pid, charge,
                    det_select, layer_select, mczero, pid_select, charge_select):
    mask = np.ones(len(x), dtype=bool)
    if det_select is not None:
        mask &= detector == det_select
    if layer_select is not None:
        mask &= layer == layer_select
    if mczero == "zero":
        mask &= mcindex == 0
    elif mczero == "nonzero":
        mask &= mcindex != 0
    if pid_select is not None:
        mask &= pid == pid_select
    if charge_select is not None:
        mask &= charge == charge_select
    removed = len(x) - np.count_nonzero(mask)
    if removed > 0:
        print(f"Removed {removed} entries due to selection/filter")
    return x[mask], y[mask], detector[mask], layer[mask], pindex[mask], mcindex[mask], pid[mask], charge[mask]


def load_data(filename):
    print(f"Loading data from {filename}")
    if filename.endswith(".npz"):
        data = np.load(filename)
        x = data["x"]
        y = data["y"]
        detector = data["detector"]
        layer = data["layer"]
        pindex = data["pindex"]
        mcindex = data["mcindex"]
        pid = data["pid"]
        charge = data["charge"]
    elif filename.endswith(".csv"):
        data = np.loadtxt(filename, delimiter=",", skiprows=1)
        x = data[:, 0]
        y = data[:, 1]
        detector = data[:, 2].astype(int)
        layer = data[:, 3].astype(int)
        pindex = data[:, 4].astype(int)
        mcindex = data[:, 5].astype(int)
        pid = data[:, 6].astype(int)
        charge = data[:, 7].astype(int)
    else:
        print("Unsupported file format.")
        sys.exit(1)
    return x, y, detector, layer, pindex, mcindex, pid, charge


def save_data(filename, x, y, detector, layer, pindex, mcindex, pid, charge):
    print(f"Saving data to {filename}")
    if filename.endswith(".npz"):
        np.savez(filename,
                 x=x, y=y,
                 detector=detector, layer=layer,
                 pindex=pindex, mcindex=mcindex,
                 pid=pid, charge=charge)
    elif filename.endswith(".csv"):
        data = np.column_stack((x, y, detector, layer, pindex, mcindex, pid, charge))
        np.savetxt(filename, data, delimiter=",",
                   header="x,y,detector,layer,pindex,mcindex,pid,charge", comments="")
    else:
        print("Unsupported save format.")
        sys.exit(1)


def main():
    args = parse_arguments()

    # -----------------------------
    # Load existing data
    # -----------------------------
    if args.load is not None:
        x_all, y_all, detector_all, layer_all, pindex_all, mcindex_all, pid_all, charge_all = load_data(args.load)

    # -----------------------------
    # Read HIPO files
    # -----------------------------
    elif args.input is not None:

        x_all, y_all = [], []
        detector_all, layer_all = [], []
        pindex_all, mcindex_all = [], []
        pid_all, charge_all = [], []

        print(f"Iterating over: {args.input}")

        try:
            for batch in hipopy.iterate(args.input):

                required_keys = ["REC::Traj_x", "REC::Traj_y",
                                 "REC::Traj_detector", "REC::Traj_layer", "REC::Traj_pindex",
                                 "MC::RecMatch_pindex", "MC::RecMatch_mcindex",
                                 "REC::Particle_pid", "REC::Particle_charge"]

                if not all(k in batch for k in required_keys):
                    continue

                n_events = len(batch["REC::Traj_x"])

                for evt_idx in range(n_events):
                    # per-event hit arrays
                    traj_x = batch["REC::Traj_x"][evt_idx]
                    traj_y = batch["REC::Traj_y"][evt_idx]
                    traj_detector = batch["REC::Traj_detector"][evt_idx]
                    traj_layer = batch["REC::Traj_layer"][evt_idx]
                    traj_pindex = batch["REC::Traj_pindex"][evt_idx]

                    # per-event MC mapping
                    mc_pindex = batch["MC::RecMatch_pindex"][evt_idx]
                    mc_mcindex = batch["MC::RecMatch_mcindex"][evt_idx]
                    mc_map = dict(zip(mc_pindex, mc_mcindex))
                    hit_mcindex = np.array([mc_map.get(p, 0) for p in traj_pindex])

                    # per-event particle mapping
                    particle_pid = batch["REC::Particle_pid"][evt_idx]
                    particle_charge = batch["REC::Particle_charge"][evt_idx]
                    hit_pid = np.array([particle_pid[p] for p in traj_pindex])
                    hit_charge = np.array([particle_charge[p] for p in traj_pindex])

                    # append to global lists
                    x_all.extend(traj_x)
                    y_all.extend(traj_y)
                    detector_all.extend(traj_detector)
                    layer_all.extend(traj_layer)
                    pindex_all.extend(traj_pindex)
                    mcindex_all.extend(hit_mcindex)
                    pid_all.extend(hit_pid)
                    charge_all.extend(hit_charge)

        except Exception as e:
            print(f"Error while reading files: {e}")
            sys.exit(1)

        if len(x_all) == 0:
            print("No data found.")
            sys.exit(1)

        x_all = np.array(x_all)
        y_all = np.array(y_all)
        detector_all = np.array(detector_all)
        layer_all = np.array(layer_all)
        pindex_all = np.array(pindex_all)
        mcindex_all = np.array(mcindex_all)
        pid_all = np.array(pid_all)
        charge_all = np.array(charge_all)

        x_all, y_all, detector_all, layer_all, pindex_all, mcindex_all, pid_all, charge_all = filter_finite(
            x_all, y_all, detector_all, layer_all, pindex_all, mcindex_all, pid_all, charge_all)

        print(f"Collected {len(x_all)} total trajectory points")

        if args.save is not None:
            save_data(args.save, x_all, y_all,
                      detector_all, layer_all,
                      pindex_all, mcindex_all,
                      pid_all, charge_all)

    else:
        print("No input or --load specified.")
        sys.exit(1)

    # -----------------------------
    # Apply selections
    # -----------------------------
    x_all, y_all, detector_all, layer_all, pindex_all, mcindex_all, pid_all, charge_all = apply_selection(
        x_all, y_all, detector_all, layer_all,
        pindex_all, mcindex_all, pid_all, charge_all,
        args.detector, args.layer, args.mczero, args.pid, args.charge
    )

    # -----------------------------
    # Apply axis limits
    # -----------------------------
    x_all, y_all, detector_all, layer_all, pindex_all, mcindex_all, pid_all, charge_all = apply_limits(
        x_all, y_all, detector_all, layer_all,
        pindex_all, mcindex_all, pid_all, charge_all,
        args.xmin, args.xmax, args.ymin, args.ymax
    )

    if len(x_all) == 0:
        print("No entries left after selection.")
        sys.exit(1)

    hist_range = None
    if None not in (args.xmin, args.xmax, args.ymin, args.ymax):
        hist_range = [[args.xmin, args.xmax], [args.ymin, args.ymax]]

    # -----------------------------
    # Plot
    # -----------------------------
    plt.figure(figsize=(16, 10))
    plt.hist2d(x_all, y_all,
               bins=args.bins,
               range=hist_range,
               cmap="viridis",
               norm=LogNorm())
    plt.colorbar(label="Counts")
    plt.xlabel(args.xtitle if args.xtitle is not None else "x", usetex=True)
    plt.ylabel(args.ytitle if args.ytitle is not None else "y", usetex=True)

    title = "REC::Traj x-y" if args.title is None else args.title
    if args.title is None:
        if args.detector is not None:
            title += f" | detector={args.detector}"
        if args.layer is not None:
            title += f" | layer={args.layer}"
        if args.mczero is not None:
            title += f" | MC={args.mczero}"
        if args.pid is not None:
            title += f" | PID={args.pid}"
        if args.charge is not None:
            title += f" | charge={args.charge}"

    plt.title(title, usetex=True, pad=20)
    plt.tight_layout()
    plt.savefig(args.output)
    print(f"Saved histogram to {args.output}")


if __name__ == "__main__":
    main()
