# Basic imports
import numpy as np
import os
import sys

# Import saga modules
SAGA_HOME = os.environ['SAGA_HOME']
sys.path.append(os.path.abspath(os.path.join(SAGA_HOME,'py')))
import saga.aggregate as sagas

# Set base directory from environment
RGH_PROJECTIONS_HOME = os.environ['RGH_PROJECTIONS_HOME']

# Setup configuration dictionary
asyms = [-0.1,0.0,0.1]
sgasyms = {"sgasyms":[[a1] for a1 in asyms]}
seeds   = {"inject_seed":[2**i for i in range(1)]}
configs = dict(
    sgasyms,
    **seeds,
)

# Set up chaining for batched data (specifically `old_dat_path`)
nbatch = 30
nbatches = {"nbatches":[nbatch]}
ibatches = {"ibatch":[i for i in range(nbatch)]}
chain_keys = ["nbatches", "ibatch"]
chain_configs = dict(
    nbatches,
    **ibatches,
) if nbatch > 1 else {}
aggregate_config = {} if nbatch > 1 else {} #NOTE: You must set this to correctly determine the path when chaining and aggregating.

# Set and loop channels
channels = ['pi','pim','pipim']
for ch in channels:

    # Setup input paths
    base_dir     = os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getKinBinnedAsym__rgc_dt__{ch}/'))
    submit_path  = os.path.join(base_dir,"submit.sh")
    yaml_path    = os.path.join(base_dir,"args.yaml")
    out_path     = os.path.join(base_dir,"jobs.txt")

    # Set aggregate keys
    aggregate_keys = []

    # Load the binscheme you want to use
    yaml_path = os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'yamls/out_4d_bins_{ch}.yaml'))
    binscheme_name = 'binscheme'
    yaml_args = sagas.load_yaml(yaml_path)
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
            'xs_ratio': 7.908/9.194,
            'lumi_ratio':100/13.2 * 5/40, # <- RGH PROPOSAL / RGC NH3 FALL 22, RGH PROPOSAL / RGC NH3 SUMMER 22 -> 100/17.7 * 5/20, #NOTE: L_integrated = T * L_instant.
            'tpol_factor':0.85,
            'tdil_factor':3/17,
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
            sagas.rescale_csv_data(
                out_file_name,
                outpath = os.path.join(base_dir, out_file_name.replace('.csv','_rescaled.csv')),
                config=config_list[config_idx],
                aggregate_config=aggregate_config,
                chain_configs=chain_configs,
                **rescale_csv_data_kwargs_base,
            )
