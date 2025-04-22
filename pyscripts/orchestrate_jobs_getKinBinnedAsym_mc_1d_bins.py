# Basic imports
import sys

# Import saga modules
SAGA_HOME = os.environ['SAGA_HOME']
sys.path.append(os.path.abspath(os.path.join(SAGA_HOME,'py')))
from saga.orchestrate import create_jobs, submit_jobs

# Set dry run to `False` once you are sure you want to submit.
dry_run=True

# Set base directories
run_groups = ["mc_rgh","mc_rgh_sector4","mc_rgc"]
channels = ["pi","pim","pipim"]
base_dirs = [
    f"test_getKinBinnedAsym__{rg}__{ch}__1D/" for rg in run_groups for ch in channels
]

# Loop base directories
for base_dir in base_dirs:

    # Create job submission structure
    asyms = [-0.1,0.0,0.1]
    sgasyms = {"sgasyms":[[a1] for a1 in asyms]}
    seeds   = {"inject_seed":[2**i for i in range(1)]}

    # Set job file paths and configs
    submit_path = base_dir+"submit.sh"
    yaml_path   = base_dir+"args.yaml"
    out_path    = base_dir+"jobs.txt"
    configs = dict(
        sgasyms,
        **seeds
    )

    # Create job directories and submit jobs
    create_jobs(configs,base_dir,submit_path,yaml_path)
    submit_jobs(configs,base_dir,submit_path,out_path,dry_run=dry_run)
