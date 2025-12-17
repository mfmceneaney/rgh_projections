# Basic imports
import os
import argparse

# Import saga modules
from saga.orchestrate import create_jobs, submit_jobs

# Parse arguments
parser = argparse.ArgumentParser(description='Script to submit `getKinBinnedAsym` jobs on RGC single and dipion data')
parser.add_argument('--dry_run', action="store_true", help='Dry run without job submission')
parser.add_argument('--rgs', default=["dt_rgc"], help='Run group', nargs="+", choices=["dt_rgc"])
parser.add_argument('--chs', default=["pi"], help='Channels', nargs="+", choices=["pi","pim","pipim"])
parser.add_argument('--asyms', default=[0.0], help='Asymmetries injected (to match MC naming schemes)', nargs="+", type=float)
parser.add_argument('--nbatch', default=30, help='Number of batches into which to split 4d binning scheme', type=int)
args = parser.parse_args()

# Set dry run to `False` once you are sure you want to submit.
dry_run=args.dry_run

# Set configuration
run_groups = args.rgs # ["dt_rgc"]
channels = args.chs # ["pi","pim","pipim"]
asyms = args.asyms # [-0.1,0.0,0.1]
RGH_PROJECTIONS_HOME = os.environ['RGH_PROJECTIONS_HOME']

# Set base directories
base_dirs = [
    os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,"jobs/saga/",f"test_getKinBinnedAsym__{rg}__{ch}/")) for rg in run_groups for ch in channels
]

# Loop base directories
for base_dir in base_dirs:

    # Create job submission structure
    sgasyms  = {"sgasyms":[[a1] for a1 in asyms]}
    seeds    = {"inject_seed":[2**i for i in range(1)]}
    nbatch   = args.nbatch #NOTE: Split 4d bin schemes into batches since they are so large.
    nbatches = {"nbatches":[nbatch]}
    ibatches = {"ibatch":[i for i in range(nbatch)]}

    # Set job file paths and configs
    submit_path =  os.path.join(base_dir,"submit.sh")
    yaml_path   =  os.path.join(base_dir,"args.yaml")
    out_path    =  os.path.join(base_dir,"jobs.txt")
    configs = dict(
        sgasyms,
        **nbatches,
        **ibatches,
        **seeds
    )

    # Create job directories and submit jobs
    create_jobs(configs,base_dir,submit_path,yaml_path)
    submit_jobs(configs,base_dir,submit_path,out_path,dry_run=dry_run)
