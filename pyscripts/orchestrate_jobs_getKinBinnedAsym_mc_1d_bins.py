# Basic imports
import os
import numpy as np
import argparse

# Import saga modules
from saga.orchestrate import create_jobs, submit_jobs

# Parse arguments
parser = argparse.ArgumentParser(description='Script to submit `getKinBinnedAsym` jobs on RGH and RGC single and dipion MC')
parser.add_argument('--dry_run', action="store_true", help='Dry run without job submission')
parser.add_argument('--rgs', default=["mc_rgc"], help='Run group', nargs="+", choices=["mc_rgh","mc_rgh_sector4","mc_rgc"])
parser.add_argument('--chs', default=["pi"], help='Channels', nargs="+", choices=["pi","pim","pipim"])
parser.add_argument('--asyms', default=[-0.1,0.0,0.1], help='Asymmetries injected', nargs="+", type=float)
parser.add_argument('--n_inject_seeds', default=1, help='Number of random injection seeds to use', type=int)
args = parser.parse_args()

# Set dry run to `False` once you are sure you want to submit.
dry_run=args.dry_run

# Set configuration
run_groups = args.rgs # ["mc_rgh","mc_rgh_sector4","mc_rgc"]
channels = args.chs # ["pi","pim","pipim"]
asyms = args.asyms # [-0.1,0.0,0.1]
n_inject_seeds = args.n_inject_seeds # 1
RGH_PROJECTIONS_HOME = os.environ['RGH_PROJECTIONS_HOME']

# Set base directories
base_dirs = [
    os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,"jobs/saga/",f"test_getKinBinnedAsym__{rg}__{ch}__1D/")) for rg in run_groups for ch in channels
]

# Loop base directories
for base_dir in base_dirs:

    # Create job submission structure #NOTE: RGC HAS 6 ASYMMETRIES, RGH HAS 9 so just filter the states that inject up to 3 asymmetries
    sgasyms = {"sgasyms":[[a1] for a1 in asyms]}
    #NOTE: Only use following block if injecting many simultaneous asymmetries
    # newsgasyms = {"sgasyms":[]}
    # for sgasym in sgasyms["sgasyms"]:
    #     if np.sum(np.abs(sgasym))<0.3:
    #         newsgasyms["sgasyms"].append(sgasym)
    # sgasyms = newsgasyms
    seeds   = {"inject_seed":[2**i for i in range(n_inject_seeds)]}

    # Set job file paths and configs
    submit_path =  os.path.join(base_dir,"submit.sh")
    yaml_path   =  os.path.join(base_dir,"args.yaml")
    out_path    =  os.path.join(base_dir,"jobs.txt")
    configs = dict(
        sgasyms,
        **seeds
    )

    # Create job directories and submit jobs
    create_jobs(configs,base_dir,submit_path,yaml_path)
    submit_jobs(configs,base_dir,submit_path,out_path,dry_run=dry_run)
