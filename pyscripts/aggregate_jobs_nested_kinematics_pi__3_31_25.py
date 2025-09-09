# Basic imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Import saga modules
SAGA_HOME = os.environ['SAGA_HOME']
sys.path.append(os.path.abspath(os.path.join(SAGA_HOME,'py')))
import saga.aggregate as sagas

# Setup, modify these as needed for your specific binning scheme
csv_path = os.path.abspath('/Users/mfm45/drop/test_getBinKinematics/test_getBinKinematics__1_24_25__pipim/out_binscheme_kinematics.csv')
hist_path = os.path.abspath('/Users/mfm45/drop/test_getBinKinematics/test_getBinKinematicsTH1Ds__1_24_25__pipim/out_binscheme_kinematics.root')
kinvars = ['phperp_pipim','phperp2_pipim','z_pipim', 'mx_pipim', 'mass_pipim']
xlabels = {'mx_pipim':'$M_{X,\\pi^{+}\\pi^{-}}$ (GeV)','mass_pipim':'$M_{\\pi^{+}\\pi^{-}}$ (GeV)','phperp_pipim':'$P_{\\perp, \\pi^{+}\\pi^{-}}$ (GeV)','phperp2_pipim':'$P^{2}_{\\perp, \\pi^{+}\\pi^{-}}$ (GeV$^{2}$)','z_pipim':'$z_{\\pi^{+}\\pi^{-}}$'}
xlims = {'mx_pipim':[0.0,3.5],'mass_pipim':[0.0,3.0],'phperp_pipim':[0.0,1.25],'phperp2_pipim':[0.0,1.6],'z_pipim':[0.0,1.0]}
hist_colors = {'mx_pipim':['tab:green'],'mass_pipim':['tab:blue'],'phperp_pipim':['tab:red'],'phperp2_pipim':['tab:red'],'z_pipim':['tab:orange']}

# Load kinematics CSV
df = pd.read_csv(csv_path)
bin_ids = df['bin'].unique().tolist()
print(df)

# Setup, modify these as needed for your specific binning scheme
yaml_path = os.path.abspath('/Users/mfm45/drop/test_getBinKinematics/test_findBinLims__1_24_25__pipim/out_4d_bins_pipim.yaml')

# Read bin scheme from YAML
binscheme_name = 'binscheme'
yaml_args = sagas.load_yaml(yaml_path)
binscheme = yaml_args[binscheme_name]
print("DEBUGGING: binscheme = ",binscheme)

# #TODO: Loop innermost variable in binscheme so for example you get a grid in x and Q2 and a graph in z or phperp FOREACH z or phperp bin?!?!?!

# Get bin scheme cuts and ids
start_idx = 0
id_key = 'bin_id'
binvar_titles = None
binscheme_cuts, binscheme_cut_titles, binscheme_ids, nested_grid_shape = sagas.get_binscheme_cuts_and_ids( #TODO: RETURN GRID SHAPE FROM THIS GUY...
                                                    binscheme,
                                                    start_idx=start_idx,
                                                    id_key=id_key,
                                                    binvar_titles=binvar_titles,
                                                )

print("DEBUGGING: binscheme_cuts = ",binscheme_cuts)
print("DEBUGGING: nested_grid_shape = ",nested_grid_shape)#TODO: FIGURE OUT HOW TO DEAL WITH THIS!?!?!?!?!

# Get projection bin ids
proj_vars = ['phperp_pipim','z_pipim']
arr_vars = ['x','Q2']
arr_var_bins = {}
all_proj_ids, arr_vars, all_proj_arr_var_ids = sagas.get_projection_ids(
        binscheme_ids,
        proj_vars,
        arr_vars = arr_vars,
        id_key=id_key,
        arr_var_bins=arr_var_bins,#TODO: ADD CHECK HERE FOR OTHER ARR VAR BINS SPECIFIED
        nested_grid_shape=nested_grid_shape,
    )

print("DEBUGGING: all_proj_ids = ", all_proj_ids)

print("DONE")
sys.exit(0)

# # Get projection bin ids
# all_proj_ids, arr_vars, all_proj_arr_var_ids = sagas.get_projection_ids(
#         binscheme_ids,
#         proj_vars,
#         arr_vars = arr_vars,
#         id_key=id_key,
#         arr_var_bins=arr_var_bins,#TODO: ADD CHECK HERE FOR OTHER ARR VAR BINS SPECIFIED
#         nested_grid_shape=nested_grid_shape,
#     )

# # Open a single graph
# graph_data = sagas.get_graph_data(
#                         dfs[0],
#                         all_proj_ids[0][0],
#                         id_key=id_key,
#                         count_key=count_key,
#                         xvar_keys=xvar_keys,
#                         asym_key=asym_key,
#                         err_ext=err_ext
#             )

# # Open an array of graphs with the shape of the projection ids array
# graph_array = sagas.get_graph_array(
#         dfs,
#         all_proj_ids,
#         id_key=id_key,
#         count_key=count_key,
#         xvar_keys=xvar_keys,
#         asym_key=asym_key,
#         err_ext=err_ext,
#         sgasym=sgasym,
#     )

# # Get a list of bin scheme ids
# bin_ids = binscheme_ids[id_key].unique().tolist()

for kinvar in kinvars:

    # Set graph and plot_results arrays
    graph_array = [{} for j in range(len(bin_ids))]
    plot_results_kwargs_array = [
            {
                'hist_keys':[f'h1_bin{bin_id}_'+kinvar],
                'title':sagas.get_bin_kinematics_title(bin_id,df),
                'xlims':xlims[kinvar],
                'xlabel':xlabels[kinvar],
                'hist_colors':hist_colors[kinvar],
            }
            for bin_id in bin_ids
    ]

    def reshape_grid(grid_array, grid_shape):
        # Reshape the grid array to match the specified shape
        reshaped_grid = []
        for i in range(grid_shape[0]):
            el = grid_array[i * grid_shape[1]:min(len(bin_ids),(i + 1) * grid_shape[1])]
            if len(el) < grid_shape[1]:
                el.extend([None for _ in range(grid_shape[1] - len(el))])
            reshaped_grid.append(el)
        return reshaped_grid

    grid_shape = (2,7)
    graph_array = reshape_grid(graph_array, grid_shape)
    plot_results_kwargs_array = reshape_grid(plot_results_kwargs_array, grid_shape)

    # Set base kwargs
    plot_results_kwargs_base = {
        'ylims':[0.0,0.05 if not 'mass' in kinvar and not 'mx' in kinvar else 0.12] if 'phperp2' not in kinvar else [1e-4,0.10],
        'show_injected_asymmetries':False,
        'hist_clone_axis':False,
        'hist_paths':[hist_path],
        'hist_labels':['RGH MC'],
        'hist_linewidth':10,
        'ylabel': 'Density',
        'watermark':'',
        'hist_density':True,
        'hist_log':True if 'phperp2' in kinvar else False,
    }

    # Set additional kwargs
    figsize = (16*grid_shape[1],10*grid_shape[0])
    outpath = 'rgh_kinematics_pipim/rgh_kinematics_'+kinvar+'.pdf'
    use_default_plt_settings = True
    use_grid_titles = False
    use_grid_xlabels = False

    # Plot an array of graphs
    sagas.plot_results_array(
            graph_array,
            plot_results_kwargs_array,
            plot_results_kwargs_base = plot_results_kwargs_base,
            figsize = figsize,
            outpath = outpath,
            use_default_plt_settings = use_default_plt_settings,
            use_grid_titles = use_grid_titles,
            use_grid_xlabels = use_grid_xlabels, #NOTE: Since you plot different x-axis variables in each row make sure that the labels are not dropped for rows below the top row.
        )
