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
csv_path = os.path.abspath('/Users/mfm45/drop/test_getBinKinematics/test_getBinKinematics__1_24_25__pipim_22GeV/out_binscheme_kinematics.csv')
hist_path = os.path.abspath('/Users/mfm45/drop/test_getBinKinematics/test_getBinKinematicsTH1Ds__1_24_25__pipim_22GeV/out_binscheme_kinematics.root')
kinvars = ['phperp_pipim','phperp2_pipim','z_pipim', 'mx_pipim', 'mass_pipim']
xlabels = {'mx_pipim':'$M_{X,\\pi^{+}\\pi^{-}}$ (GeV)','mass_pipim':'$M_{\\pi^{+}\\pi^{-}}$ (GeV)','phperp_pipim':'$P_{\\perp, \\pi^{+}\\pi^{-}}$ (GeV)','phperp2_pipim':'$P^{2}_{\\perp, \\pi^{+}\\pi^{-}}$ (GeV$^{2}$)','z_pipim':'$z_{\\pi^{+}\\pi^{-}}$'}
xlims = {'mx_pipim':[0.0,5.5],'mass_pipim':[0.0,3.0],'phperp_pipim':[0.0,3.0],'phperp2_pipim':[0.0,3.0],'z_pipim':[0.0,1.0]}
hist_colors = {'mx_pipim':['tab:green'],'mass_pipim':['tab:blue'],'phperp_pipim':['tab:red'],'phperp2_pipim':['tab:red'],'z_pipim':['tab:orange']}

# Load kinematics CSV
df = pd.read_csv(csv_path)
bin_ids = df['bin'].unique().tolist()

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
        'ylims':[0.0,0.07 if not 'mass' in kinvar else 0.15] if 'phperp2' not in kinvar else [1e-4,0.20],
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
    outpath = 'rgh_kinematics_pipim_22GeV/rgh_kinematics_'+kinvar+'_22GeV.pdf'
    use_default_plt_settings = True
    use_grid_titles = False
    use_grid_xlabels = True

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
