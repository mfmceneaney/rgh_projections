# Basic imports
import numpy as np
import os
import argparse

# Import saga modules
import saga.aggregate as sagas
from saga.data import load_yaml
from saga.rescale import rescale_csv_data

# Parse arguments
parser = argparse.ArgumentParser(description='Script to rescale `getKinBinnedAsym` jobs on RGH and RGC single and dipion data and MC')
parser.add_argument('--dry_run', action="store_true", help='Dry run without job submission')
parser.add_argument('--rgs', default=["dt_rgc"], help='Run group', nargs="+", choices=["dt_rgc"])
parser.add_argument('--chs', default=["pi"], help='Channels', nargs="+", choices=["pi","pim","pipim"])
parser.add_argument('--asyms', default=[0.0], help='Asymmetries injected (to match MC naming schemes)', nargs="+", type=float)
parser.add_argument('--nbatch', default=30, help='Number of batches into which to split 4d binning scheme', type=int)
parser.add_argument('--xs_ratio', default=7.908/9.194, help='Cross-section ratio (new/old) for rescaling uncertainties', type=float)
parser.add_argument('--lumi_ratio', default=100/13.2 * 5/40, help='Luminosity ratio (new/old) for rescaling uncertainties', type=float)
parser.add_argument('--yvalue', default=-100.0, help='CSV y-value for rescaled uncertainties', type=float)
parser.add_argument('--tpol_factor', default=0.85, help='Target polarization for rescaling uncertainties', type=float)
parser.add_argument('--tdil_factor', default=3/17, help='Target dilution factor for rescaling uncertainties', type=float)
args = parser.parse_args()

# Set configuration
run_groups = args.rgs # ["dt_rgc"]
channels = args.chs # ["pi","pim","pipim"]
asyms = args.asyms # [-0.1,0.0,0.1]
nbatch = args.nbatch # 30
RGH_PROJECTIONS_HOME = os.environ['RGH_PROJECTIONS_HOME']

# Setup configuration dictionary
sgasyms = {"sgasyms":[[a1] for a1 in asyms]}
seeds   = {"inject_seed":[2**i for i in range(1)]}
configs = dict(
    sgasyms,
    **seeds,
)

# Set up chaining for batched data (specifically `old_dat_path`)
nbatches = {"nbatches":[nbatch]}
ibatches = {"ibatch":[i for i in range(nbatch)]}
chain_keys = ["nbatches", "ibatch"]
chain_configs = dict(
    nbatches,
    **ibatches,
) if nbatch > 1 else {}
aggregate_config = {} if nbatch > 1 else {} #NOTE: You must set this to correctly determine the path when chaining and aggregating.

# Loop run groups and channels
for rg in run_groups:
    for ch in channels:

        # Setup input paths
        base_dir     = os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getKinBinnedAsym__{rg}__{ch}/'))
        submit_path  = os.path.join(base_dir,"submit.sh")
        yaml_path    = os.path.join(base_dir,"args.yaml")
        out_path     = os.path.join(base_dir,"jobs.txt")

        # Set aggregate keys
        aggregate_keys = []

        # Load the binscheme you want to use
        yaml_path = os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'yamls/out_4d_bins_{ch}.yaml'))
        binscheme_name = 'binscheme'
        yaml_args = load_yaml(yaml_path)
        binscheme = yaml_args[binscheme_name]

        # Arguments for sagas.get_config_list()
        result_name = "a0" #NOTE: This also gets recycled as the asymmetry name

        # Arguments for sagas.get_out_dirs_list()
        sep='_'
        ext='.pdf'

        # Arguments for sagas.get_out_file_name()
        out_file_name_ext = '.csv'

        # Arguments for sagas.rescale_csv_data()
        rescale_csv_data_kwargs_base = {
                'old_dat_path':os.path.basename(base_dir),
                'new_sim_path':os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getKinBinnedAsym__mc_rgh__{ch}/')),
                'old_sim_path':os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getKinBinnedAsym__mc_rgc__{ch}/')),
                'count_key':'count',
                'yerr_key':result_name,
                'yerr_key':result_name+'_err',
                'xs_ratio': xs_ratio,
                'lumi_ratio':lumi_ratio,
                'tpol_factor':tpol_factor,
                'tdil_factor':tdil_factor,
                'yvalue':-100.0,
        }

        #---------- Set configurations and loop ----------#

        # Get list of configurations
        config_list = sagas.get_config_list(configs,aggregate_keys=aggregate_keys)

        # Get aggregated list of directories
        out_dirs_list = sagas.get_out_dirs_list(
                                        configs,
                                        base_dir,
                                        aggregate_keys=aggregate_keys
                                    )

        # Loop each aggregate list
        for config_idx in range(len(config_list)):

            # Set the config you are interested in
            out_dirs = out_dirs_list[config_idx]

            # Get the name of the CSV file for the binning scheme you are interested in
            out_file_names = [sagas.get_out_file_name(
                    base_dir=outdir,
                    base_name='out_',
                    binscheme_name=binscheme_name,
                    ext=out_file_name_ext
                ) for outdir in out_dirs]

            # Rescale results files
            for out_file_name in out_file_names:
                rescale_csv_data(
                    out_file_name,
                    outpath = os.path.join(base_dir, out_file_name.replace('.csv','_rescaled.csv')),
                    config=config_list[config_idx],
                    aggregate_config=aggregate_config,
                    chain_configs=chain_configs,
                    **rescale_csv_data_kwargs_base,
                )
