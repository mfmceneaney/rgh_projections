# Basic imports
import os

# Import saga modules
from saga.orchestrate import create_jobs, submit_jobs
from saga.data import load_yaml

# Set dry run to `False` once you are sure you want to submit.
dry_run=True

# Set base directories
run_groups = ["dt_rgc"]
channels = ["pi","pim"] #,"pipim"]
base_dirs = [
    os.path.abspath(os.path.join(os.environ['RGH_PROJECTIONS_HOME'],"jobs/saga/",f"test_getKinBinnedAsym__{rg}__{ch}__1D/")) for rg in run_groups for ch in channels
]

# Set paths for 1D bin scheme yaml for splitting
YAML_DIR = os.path.abspath(os.path.join(os.environ['RGH_PROJECTIONS_HOME'],'yamls'))
yaml_paths = [
    os.path.join(YAML_DIR,f'out_1d_bins_{ch}.yaml') for rg in run_groups for ch in channels
]

# Loop base directories
for base_dir, yaml_path in zip(base_dirs,yaml_paths):

    # Create job submission structure
    asyms   = [0.0]
    sgasyms = {"sgasyms":[[a1,a2,a3,a4,a5,a6,a7,a8,a9] for a1 in asyms for a2 in asyms for a3 in asyms for a4 in asyms for a5 in asyms for a6 in asyms for a7 in asyms for a8 in asyms for a9 in asyms]}
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
