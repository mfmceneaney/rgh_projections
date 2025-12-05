# Basic imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Import saga modules
import saga.plot as sagap

# Set base directory from environment
RGH_PROJECTIONS_HOME = os.environ['RGH_PROJECTIONS_HOME']

# Set channels and beam suffixes to loop
chs = ['pi','pim','pipim']#,'k','km']
ch_labels = {'pi':'\\pi^{+}','pim':'\\pi^{-}','pipim':'\\pi^{+}}\\pi^{-}','k':'K^{+}','km':'K^{-}'}
beam_suffixes = ['']#,'_22GeV']
rgs = ['dt_rgc','mc_rgc','mc_rgh', 'mc_rgh_sector4']
rg_labels = {'dt_rgc':'Data RGC','mc_rgc':'MC RGC','mc_rgh':'MC RGH','mc_rgh_sector4':'MC RGH with Sector 4'}
binvars = None
ylims_by_rg = {
    'dt_rgc': (0.0, 10000.0),
    'mc_rgc': (0.0, 1000.0),
    'mc_rgh': (0.0, 1000.0),
    'mc_rgh_sector4': (0.0, 1000.0),
}
# Loop run groups, channels, and beam suffixes
for rg in rgs:
    for ch in chs:
        for beam_suffix in beam_suffixes:

            # Set y limits
            ylims = ylims_by_rg[rg]

            # Set binvars
            if ch=='pipim':
                binvars = ['x', 'mass', 'mx', 'z']
            else:
                binvars = ['x', 'mx', 'phperp', 'z']
            binvars = [el+(f'_{ch}' if el!='x' else '') for el in binvars]

            # Set binvar titles
            binvar_titles = {
                'x'            : 'x',
                'Q2'           : 'Q^{2}',
                f'mx__{ch}'    : 'M_{X '+ch_labels[ch]+'}',
                f'phperp_{ch}' : 'P_{'+ch_labels[ch]+'\\perp}',
                f'mass_{ch}'   : 'M_{'+ch_labels[ch]+'}',
                f'mx_{ch}'     : 'M_{X '+ch_labels[ch]+'}',
                f'z_{ch}'      : 'z_{'+ch_labels[ch]+'}',
            }
            binvar_unit_titles = {
                'x'            : '',
                'Q2'           : ' (GeV$^{2}$)',
                f'mx_{ch}'     : ' (GeV)',
                f'phperp_{ch}' : ' (GeV)',
                f'mass_{ch}'   : ' (GeV)',
                f'mx_{ch}'     : ' (GeV)',
                f'z_{ch}'      : '',
            }

            # Loop 1D bin variables
            for binvar in binvars:

                # Setup, modify these as needed for your specific binning scheme
                csv_path = os.path.abspath(
                    os.path.join(
                        RGH_PROJECTIONS_HOME,
                        f'jobs/saga/test_getBinKinematics__{ch}/out_{rg}_1d_bins_{binvar}_kinematics.csv'
                    )
                )
                hist_path = os.path.abspath(
                    os.path.join(
                        RGH_PROJECTIONS_HOME,
                        f'jobs/saga/test_getBinKinematicsTH1Ds__{ch}/out_{rg}_1d_bins_{binvar}_kinematics.root'
                    )
                )
                print(f"INFO: csv_path: {csv_path}")
                print(f"INFO: hist_path: {csv_path}")

                # Set kinematic variable pairs to plot
                kinvars = binvars.copy()
                kinvars.remove(binvar)

                # Loop kinematic variable pairs
                for kinvar_x in kinvars:

                    # Grab kinematic variables and set related info
                    xlabels = {
                        'x'             : '$x$',
                        'Q2'            : '$Q^{2}$ (GeV$^{2}$)',
                        f'mx_{ch}'      : '$M_{X '+ch_labels[ch]+'}$ (GeV)',
                        f'phperp_{ch}'  : '$P_{'+ch_labels[ch]+'\\perp}$ (GeV)',
                        f'phperp2_{ch}' : '$P^{2}_{'+ch_labels[ch]+'\\perp}$ (GeV$^{2}$)',
                        f'z_{ch}'       : '$z_{'+ch_labels[ch]+'}$',
                        f'mass_{ch}'    : '$M_{'+ch_labels[ch]+'}$ (GeV)',
                    }                    
                    xlims = {
                        'x'             : [0.0,1.0],
                        'Q2'            : [1.0,20.0] if beam_suffix=='_22GeV' else [1.0,10.0],
                        f'mx_{ch}'      : [0.0,5.0],
                        f'mass_{ch}'    : [0.0,3.0],
                        f'phperp_{ch}'  : [0.0,2.25] if beam_suffix=='_22GeV' else [0.0,1.25],
                        f'phperp2_{ch}' : [0.0,5.0]  if beam_suffix=='_22GeV' else [0.0,1.6],
                        f'z_{ch}'       : [0.0,1.0],
                    }
                    hist_colors = {
                        'x'             : ['tab:purple'],
                        'Q2'            : ['tab:cyan'],
                        f'mx_{ch}'      : ['tab:olive'],
                        f'mass_{ch}'    : ['tab:blue'],
                        f'phperp_{ch}'  : ['tab:red'],
                        f'phperp2_{ch}' : ['tab:green'],
                        f'z_{ch}'       : ['tab:orange'],
                    }

                    # Only add bin variable values above plots for now
                    cols = [
                        binvar,
                    ]
                    col_titles = {
                        binvar:binvar_titles[binvar],
                    }
                    col_unit_titles = {
                        binvar:binvar_unit_titles[binvar],
                    }

                    # Load kinematics CSV
                    df = pd.read_csv(csv_path)
                    bin_ids = df['bin'].unique().tolist()

                    # Set graph and plot_results arrays
                    graph_array = [{} for j in range(len(bin_ids))]
                    plot_results_kwargs_array = [
                            {
                                'hist_keys':[f'h1_bin{bin_id}_'+kinvar_x],
                                'title':sagap.get_bin_kinematics_title(
                                        bin_id,df,
                                        cols=cols,
                                        col_titles=col_titles,
                                        col_unit_titles=col_unit_titles
                                    ),
                                'xlims':xlims[kinvar_x],
                                'xlabel':xlabels[kinvar_x],
                                'ylims':ylims,
                                'ylabel':'Counts',
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
                    print("INFO: graph_array = ",graph_array)
                    print("INFO: plot_results_kwargs_array = ", plot_results_kwargs_array)

                    # Set base kwargs
                    plot_results_kwargs_base = {
                        'show_injected_asymmetries':False,
                        'hist_clone_axis':False,
                        'hist_paths':[hist_path],
                        'hist_labels':[f'{rg_labels[rg]}'],
                        'watermark':'CLAS12 Preliminary',
                        'hist_density':False,
                        'axlinewidth':0,
                        'hist_dim':1,
                        'legend_loc':'best' #NOTE: Do not plot a legend if you are using 2d hists.
                    }

                    # Set additional kwargs
                    figsize = (16*grid_shape[1],10*grid_shape[0])
                    outpath = f'plot_TH1Ds__{rg}{beam_suffix}__{ch}__1d_{kinvar_x}__1d_{binvar}.pdf'
                    use_default_plt_settings = True
                    use_grid_titles = False
                    use_grid_xlabels = True

                    # Plot an array of graphs
                    sagap.plot_results_array(
                        graph_array,
                        plot_results_kwargs_array,
                        plot_results_kwargs_base = plot_results_kwargs_base,
                        figsize = figsize,
                        outpath = outpath,
                        use_default_plt_settings = use_default_plt_settings,
                        use_grid_titles = use_grid_titles,
                        use_grid_xlabels = use_grid_xlabels, #NOTE: Since you plot different x-axis variables in each row make sure that the labels are not dropped for rows below the top row.
                    )

                    # Close the figures to conserve memory
                    plt.close('all')
