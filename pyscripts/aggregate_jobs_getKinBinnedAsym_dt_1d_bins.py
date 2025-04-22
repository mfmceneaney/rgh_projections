# Basic imports
import numpy as np
import matplotlib.pyplot as plt
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
nbatch = 1
nbatches = {"nbatches":[nbatch]}
ibatches = {"ibatch":[i for i in range(nbatch)]}
chain_keys = ["nbatches", "ibatch"]
chain_configs = dict(
    nbatches,
    **ibatches,
) if nbatch > 1 else {}

# Set base directories to aggregate
run_groups = ['dt_rgc']
channels   = ['pi','pim','pipim']
base_dirs  = [
    os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getKinBinnedAsym__{rg}__{ch}__1D/')) for rg in run_groups for ch in channels
]

# Set list of channels for each base directory
chs = [ch for rg in run_groups for ch in channels]

# Set channel label for each base directory
ch_sgasym_labels = {
    'pi':'$\mathcal{A}_{UT}^{\sin{\phi_{\pi^{+}}}}$',
    'pim':'$\mathcal{A}_{UT}^{\sin{\phi_{\pi^{-}}}}$',
    'pipim':'$\mathcal{A}_{UT}^{\sin{\phi_{R_{T}}}\sin{\\theta}}$',
}
ch_sgasym_labels = [ch_sgasym_labels[ch] for rg in run_groups for ch in channels]

# Set x-axis labels for kinematic variables in all channels
xlabel_map = {
    'Q2':'$Q^{2}$ (GeV$^{2}$)', 'W':'$W$ (GeV)', 'x':'$x$', 'y':'$y$',
    'z_pi':'$z_{\pi^{+}}$', 'mx_pi':'$M_{X, \pi^{+}}$ (GeV)', 'phperp_pi':'$P_{\pi^{+}, \perp}$ (GeV)',
    'z_pim':'$z_{\pi^{-}}$', 'mx_pim':'$M_{X, \pi^{-}}$ (GeV)', 'phperp_pim':'$P_{\pi^{-}, \perp}$ (GeV)',
    'z_pipim':'$z_{\pi^{+}\pi^{-}}$', 'mx_pipim':'$M_{X, \pi^{+}\pi^{-}}$ (GeV)', 'phperp_pipim':'$P_{\pi^{+}\pi^{-}, \perp}$ (GeV)', 'mass_pipim':'$M_{X, \pi^{+}\pi^{-}}$ (GeV)',
}

# Loop base directories
for base_dir, ch_sgasym_label, ch in zip(base_dirs,ch_sgasym_labels,chs):

    # Setup input paths
    submit_path  = os.path.join(base_dir,"submit.sh")
    yaml_path    = os.path.join(base_dir,"args.yaml")
    out_path     = os.path.join(base_dir,"jobs.txt")
    #NOTE: Set the bin migration path below since this is binscheme dependent

    # Set aggregate keys
    aggregate_keys = []

    # Load the binschemes from the path specified in the job yaml assuming there is only one given path and it is an absolute path
    binschemes_paths_name = "binschemes_paths"
    yaml_path = sagas.load_yaml(yaml_path)[binschemes_names][0]
    binschemes = sagas.load_yaml(yaml_path)

    # Arguments for sagas.get_config_list()
    result_name = "a0" #NOTE: This also gets recycled as the asymmetry name

    # Arguments for sagas.get_out_dirs_list()
    sep='_'
    ext='.pdf'

    # Arguments for sagas.get_out_file_name()
    out_file_name_ext = '.csv'
    bin_mig_base_name="bin_mig_mat_"

    # Arguments for sagas.apply_bin_mig()
    use_bin_mig = False
    id_gen_key='binid_gen'
    id_rec_key='binid_rec'
    mig_key='mig'
    results_keys = [result_name] #NOTE: You can apply bin migration to multiple dataframe entries in one go.

    # Arguments for sagas.get_graph_data()
    id_key = 'bin_id'

    # Arguments for sagas.get_graph_data()
    count_key  = 'count'
    asym_key   = result_name #NOTE: This is set from above
    err_ext    = '_err'

    # Arguments for sagas.plot_results()
    plot_results_kwargs_base = {
        'ylims':[-0.05,0.2],
        'sgasyms':[0.0,0.1,0.0],
        'sgasym_idx':0,
        'sgasym_labels':[ch_sgasym_label],
        'sg_colors':['blue','red','green'],
        'bgasyms':[],
        'bgasym_labels':[],
        'bg_colors':[],
        'show_injected_asymmetries':False,
        'hist_paths':[],
        'hist_colors':[
            'tab:orange',
            'tab:red',
            'tab:blue',
        ],
        'hist_keys':[], #TODO: Set this and bin limits below...
        'hist_labels':[
            'RGH MC',
            'RGC MC',
            'RGC Data',
        ],
        'hist_clone_axis':True,
        'hist_ylims':[0.0,0.06],
        'old_dat_path':None
    }

    # Additional useful parameters for plotting
    figsize = (16,10)
    #NOTE: Set outpath within the loop for unique naming
    use_default_plt_settings = True

    # If you want to rescale your results using results from other base directories set the following arguments
    rescale = False
    if rescale:
        plot_results_kwargs_base = dict(
            plot_results_kwargs_base,
            **{
                'old_dat_path':os.path.basename(base_dir),
                'new_sim_path':os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getKinBinnedAsym__mc_rgh__{ch}__1D/')),
                'old_sim_path':os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getKinBinnedAsym__mc_rgc__{ch}__1D/')),
                'count_key':'count',
                'yerr_key':'',
                'xs_ratio': 7.908/9.194,
                'lumi_ratio':100/13.2 * 5/40, # <- RGC NH3 FALL 22, RGC NH3 SUMMER 22 -> 100/17.7 * 5/20, #NOTE: L_integrated = T * L_instant.
                'graph_yvalue':0.1,
                'tpol_factor':0.85,
                'tdil_factor':3/17, 
            },
        )

    #---------- Set configurations ----------#
    # Get list of configurations
    config_list = sagas.get_config_list(configs,aggregate_keys=aggregate_keys)

    # Get aggregated list of directories
    out_dirs_list = sagas.get_out_dirs_list(
                                    configs,
                                    base_dir,
                                    aggregate_keys=aggregate_keys
                                )

    #---------- Loop bin schemes ----------#
    for binscheme_idx, binscheme_name in enumerate(binschemes.keys()):

        # Get the bin scheme
        binscheme = binschemes[binscheme_name]
        proj_var  = list(binscheme.keys())[0] #NOTE: Assume projection variable is the only variable in the bin scheme
        nbins = len(binscheme[proj_var])-1

        # Arguments for sagas.get_graph_data()
        xvar_keys = [proj_var]

        # Set some bin scheme dependent plotting parameters
        binlims = binscheme[proj_var]
        plot_results_kwargs_base['xlims'] = [binlims[0],binlims[-1]]
        plot_results_kwargs_base['xlabel'] = xlabel_map[binscheme_name]
        plot_results_kwargs_base['binlims'] = binlims
        plot_results_kwargs_base['hist_paths'] = [
            os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getBinKinematicsTH1Ds__{ch}/out_mc_rgh_1d_bins_binscheme_kinematics.root')),
            os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getBinKinematicsTH1Ds__{ch}/out_mc_rgc_1d_bins_binscheme_kinematics.root')),
            os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getBinKinematicsTH1Ds__{ch}/out_dt_rgc_1d_bins_binscheme_kinematics.root')),
        ]
        plot_results_kwargs_base['hist_keys'] = ['h1_bin0_'+binscheme_name for i in range(len(plot_results_kwargs_base['hist_paths']))]

        # Get the bin migration path
        bin_mig_path = sagas.get_out_file_name(
            base_dir=base_dir,
            base_name=bin_mig_base_name,
            binscheme_name=binscheme_name,
            ext=out_file_name_ext
        )

        # Load bin migration matrix and invert
        bin_mig_df, bin_mig_mat, inv_bin_mig_mat = None, None, None
        if use_bin_mig:
            bin_mig_df = sagas.load_csv(bin_mig_path)
            bin_mig_mat = sagas.get_bin_mig_mat(
                bin_mig_df,
                id_gen_key=id_gen_key,
                id_rec_key=id_rec_key,
                mig_key=mig_key,
            )
            sagas.save_bin_mig_mat_to_csv(
                bin_mig_mat,
                base_dir='./',
                basename=binscheme_name,
                delimiter=",",
                header=None,
                fmt=None,
                comments='',
            )
            inv_bin_mig_mat = np.linalg.inv(bin_mig_mat)

        #---------- Loop configurations ----------#
        # Loop each aggregate list
        for config_idx in range(len(config_list)):

            # Set the config you are interested in
            config = config_list[config_idx]
            out_dirs = out_dirs_list[config_idx]

            # Set the output path basename for this config
            config_out_path = sagas.get_config_out_path(
                    base_dir,
                    aggregate_keys,
                    binscheme_name+sep+rgh_mc_name+sep+result_name,
                    config,
                    sep=sep,
                    ext=ext,
                )
            config_out_path = os.path.join(base_dir,config_out_path)

            # Get the name of the CSV file for the binning scheme you are interested in
            out_file_names = [sagas.get_out_file_name(
                    base_dir=outdir,
                    base_name='out_',
                    binscheme_name=binscheme_name,
                    ext=out_file_name_ext
                ) for outdir in out_dirs]

            # Load pandas dataframes from the files
            dfs = [sagas.load_csv(out_file_name,config=config,chain_configs=chain_configs) for out_file_name in out_file_names]

            # Apply bin migration correction
            if use_bin_mig:
                for df in dfs:
                    sagas.apply_bin_mig(df,inv_bin_mig_mat,results_keys=results_keys) #NOTE: THIS MODIFIES THE DATAFRAMES IN PLACE

            # Get an aggregate graph
            proj_ids = [i for i in range(nbins)]#NOTE: Assume bin scheme indices are simple
            sgasym_idx = plot_results_kwargs_base['sgasym_idx'] #NOTE: Assume this is in the kwargs base dictionary
            sgasym = config['sgasyms'][sgasym_idx] if 'sgasyms' in config else 0.0
            plot_results_kwargs_base['sgasyms'] = config['sgasyms']#NOTE: TODO:
            aggregate_graph = sagas.get_aggregate_graph(
                [
                    sagas.get_graph_data(
                                df,
                                proj_ids,
                                id_key=id_key,
                                count_key=count_key,
                                xvar_keys=xvar_keys,
                                asym_key=asym_key,
                                err_ext=err_ext
                    ) for df in dfs
                ],
                xvar_keys=xvar_keys,
                sgasym=sgasym
            )

            # Use default plotting settings
            if use_default_plt_settings: sagas.set_default_plt_settings()

            # Create figure and axes
            f, ax = plt.subplots(figsize=figsize)

            # Set additional arguments for saga.aggregate.plot_results()
            plot_results_kwargs_base['sgasyms'] = config['sgasyms']
            plot_results_kwargs_base['outpath'] = config_out_path

            # Plot the graph
            sagas.plot_results(ax,**aggregate_graph,**plot_results_kwargs_base)

            # Save the graph
            f.savefig(config_out_path)
