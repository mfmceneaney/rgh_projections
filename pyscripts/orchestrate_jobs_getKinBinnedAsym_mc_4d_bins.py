# Basic imports
import sys
import os

# Import saga modules
SAGA_HOME = os.environ['SAGA_HOME']
sys.path.append(os.path.abspath(os.path.join(SAGA_HOME,'py')))
from saga.orchestrate import create_jobs, submit_jobs

# Set dry run to `False` once you are sure you want to submit.
dry_run=True

# Set base directories
run_groups = ["mc_rgh","mc_rgh_sector4","mc_rgc"]
channels = ["pi","pim"] #,"pipim"]
base_dirs = [
    os.path.abspath(os.path.join(os.environ['RGH_PROJECTIONS_HOME'],"jobs/saga/",f"test_getKinBinnedAsym__{rg}__{ch}/")) for rg in run_groups for ch in channels
]

# Loop base directories
for base_dir in base_dirs:

    # Create job submission structure #NOTE: RGC HAS 6 ASYMMETRIES, RGH HAS 9 so just filter the states that inject up to 3 asymmetries
    asyms = [-0.1,0.0,0.1]
    sgasyms = {"sgasyms":[[a1,a2,a3,a4,a5,a6,a7,a8,a9] for a1 in asyms for a2 in asyms for a3 in asyms for a4 in asyms for a5 in asyms for a6 in asyms for a7 in asyms for a8 in asyms for a9 in asyms]}
    newsgasyms = {"sgasyms":[]}
    for sgasym in sgasyms["sgasyms"]:
        if np.sum(np.abs(sgasym))<0.3:
            newsgasyms["sgasyms"].append(sgasym)
    sgasyms = newsgasyms
    seeds   = {"inject_seed":[2**i for i in range(1)]}

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
