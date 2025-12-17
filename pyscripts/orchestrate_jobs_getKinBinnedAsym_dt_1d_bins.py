# Basic imports
import os
import argparse

# Import saga modules
from saga.orchestrate import create_jobs, submit_jobs
from saga.data import load_yaml

# Parse arguments
parser = argparse.ArgumentParser(description='Script to submit `getKinBinnedAsym` jobs on RGC single and dipion data')
parser.add_argument('--dry_run', action="store_true", help='Dry run without job submission')
parser.add_argument('--rgs', default=["dt_rgc"], help='Run group', nargs="+", choices=["dt_rgc"])
parser.add_argument('--chs', default=["pi"], help='Channels', nargs="+", choices=["pi","pim","pipim"])
parser.add_argument('--asyms', default=[-0.1,0.0,0.1], help='Asymmetries injected (to match MC naming schemes)', nargs="+", type=float)
args = parser.parse_args()

# Set dry run to `False` once you are sure you want to submit.
dry_run=args.dry_run

# Set configuration
run_groups = args.rgs # ["dt_rgc"]
channels = args.chs # ["pi","pim","pipim"]
asyms = args.asyms # [-0.1,0.0,0.1]
RGH_PROJECTIONS_HOME = os.environ['RGH_PROJECTIONS_HOME']
YAML_DIR = os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,'yamls'))

# Set base directories
base_dirs = [
    os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,"jobs/saga/",f"test_getKinBinnedAsym__{rg}__{ch}__1D/")) for rg in run_groups for ch in channels
]

# Set paths for 1D bin scheme yaml for splitting
yaml_paths = [
    os.path.join(YAML_DIR,f'out_1d_bins_{ch}.yaml') for rg in run_groups for ch in channels
]

# Loop base directories
for base_dir, yaml_path in zip(base_dirs,yaml_paths):

    # Create job submission structure
    sgasyms = {"sgasyms":[[a1] for a1 in args.asyms]}
    seeds   = {"inject_seed":[2**i for i in range(1)]}

    # Split binschemes with aliases
    binschemes = load_yaml(yaml_path)
    binschemes = {"binschemes":[{el:binschemes[el]} for el in binschemes]}
    aliases    = {"binschemes":{
                        str(el):list(el.keys())[0]+"_binscheme"
                        for el in binschemes["binschemes"]
                    }
                }

    # Set job file paths and configs
    submit_path = os.path.join(base_dir,"submit.sh")
    yaml_path   = os.path.join(base_dir,"args.yaml")
    out_path    = os.path.join(base_dir,"jobs.txt")
    configs = dict(
        sgasyms,
        **binschemes,
        **seeds
    )

    # Create job directories and submit jobs
    create_jobs(configs,base_dir,submit_path,yaml_path,aliases=aliases)
    submit_jobs(configs,base_dir,submit_path,out_path,aliases=aliases,dry_run=dry_run)
