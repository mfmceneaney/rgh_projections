# Basic imports
import sys
import os

# Import saga modules
SAGA_HOME = os.environ['SAGA_HOME']
sys.path.append(os.path.abspath(os.path.join(SAGA_HOME,'py')))
from saga.orchestrate import create_jobs, submit_jobs
import saga.aggregate as sagas

# Set dry run to `False` once you are sure you want to submit.
dry_run=True

# Set base directories
run_groups = ["dt_rgc"]
channels = ["pi","pim"] #,"pipim"]
base_dirs = [
    os.path.abspath(os.path.join(os.environ['RGH_PROJECTIONS_HOME'],"jobs/saga/",f"test_getKinBinnedAsym__{rg}__{ch}/")) for rg in run_groups for ch in channels
]

# Loop base directories
for base_dir, yaml_path in zip(base_dirs,yaml_paths):

    # Create job submission structure
    asyms    = [0.0]
    sgasyms  = {"sgasyms":[[a1,a2,a3,a4,a5,a6,a7,a8,a9] for a1 in asyms for a2 in asyms for a3 in asyms for a4 in asyms for a5 in asyms for a6 in asyms for a7 in asyms for a8 in asyms for a9 in asyms]}
    seeds    = {"inject_seed":[2**i for i in range(1)]}
    nbatch   = 30 #NOTE: Split 4d bin schemes into batches since they are so large.
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
    create_jobs(configs,base_dir,submit_path,yaml_path,aliases=aliases)
    submit_jobs(configs,base_dir,submit_path,out_path,aliases=aliases,dry_run=dry_run)
