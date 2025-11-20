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
# Loop run groups, channels, and beam suffixes
for rg in rgs:
    for ch in chs:
        for beam_suffix in beam_suffixes:

            # Set binvars
            if ch=='pipim':
                binvars = ['x', 'mass', 'mx', 'z']
            else:
                binvars = ['x', 'mx', 'phperp', 'z']
            binvars = [el+f'_{ch}' for el in binvars]

            # Set binvar titles
            binvar_titles = {
                'x'        : 'x',
                'Q2'       : 'Q^{2}',
                'mx'       : 'M_{X '+ch_labels[ch]+'}',
                'phperp'   : 'P_{\\perp, '+ch_labels[ch]+'}',
                'mass'     : 'M_{'+ch_labels[ch]+'}',
                'z'        : 'z_{'+ch_labels[ch]+'}',
            }
            binvar_unit_titles = {
                'x'        : '',
                'Q2'       : ' (GeV$^{2}$)',
                'mx'       : ' (GeV)',
                'phperp'   : ' (GeV)',
                'mass'     : ' (GeV)',
                'z'        : '',
            }

            # Loop 1D bin variables
            for binvar in binvars:

                # Setup, modify these as needed for your specific binning scheme
                csv_path = os.path.abspath(
                    os.path.join(
                        RGH_PROJECTIONS_HOME,
                        f'jobs/saga/test_getBinKinematics/test_getBinKinematics__{ch}/out_{rg}_1d_bins_{binvar}_kinematics.csv'
                    )
                )
                hist_path = os.path.abspath(
                    os.path.join(
                        RGH_PROJECTIONS_HOME,
                        f'jobs/saga/test_getBinKinematicsTH2Ds__{ch}/out_{rg}_1d_bins_{binvar}_kinematics.root'
                    )
                )

                kinvar_x, kinvar_y = [f'z_{ch}', f'phperp2_{ch}']
                xlabels = {
                    f'phperp_{ch}'  : '$P_{\\perp, '+ch_labels[ch]+'}$ (GeV)',
                    f'phperp2_{ch}' : '$P^{2}_{\\perp, '+ch_labels[ch]+'}$ (GeV$^{2}$)',
                    f'z_{ch}'       : '$z_{'+ch_labels[ch]+'}$',
                    f'mass_{ch}'    : '$M_{'+ch_labels[ch]+'}$ (GeV)',
                }                    
                xlims = {
                    f'mass_{ch}'    : [0.0,3.0],
                    f'phperp_{ch}'  : [0.0,2.25] if beam_suffix=='_22GeV' else [0.0,1.25],
                    f'phperp2_{ch}' : [0.0,5.0] if beam_suffix=='_22GeV' else [0.0,1.6],
                    f'z_{ch}'       : [0.0,1.0],
                }
                hist_colors = {
                    f'mass_{ch}'.   : ['tab:blue'],
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

                # Load kinematics CSV
                df = pd.read_csv(csv_path)
                bin_ids = df['bin'].unique().tolist()

                # Set graph and plot_results arrays
                graph_array = [{} for j in range(len(bin_ids))]
                plot_results_kwargs_array = [
                        {
                            'hist_keys':[f'h2_bin{bin_id}_'+kinvar_x+'_'+kinvar_y],
                            'title':sagap.get_bin_kinematics_title(bin_id,df,cols=cols,col_titles=col_titles),
                            'xlims':xlims[kinvar_x],
                            'xlabel':xlabels[kinvar_x],
                            'ylims':xlims[kinvar_y],
                            'ylabel':xlabels[kinvar_y],
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

                # Set base kwargs
                plot_results_kwargs_base = {
                    'show_injected_asymmetries':False,
                    'hist_clone_axis':False,
                    'hist_paths':[hist_path],
                    'hist_labels':[f'{rg_labels[rg]}'],
                    'watermark':'',
                    'hist_density':False,
                    'axlinewidth':0,
                    'hist_dim':2,
                    'legend_loc':None #NOTE: Do not plot a legend since you are using 2d hists.
                }

                # Set additional kwargs
                figsize = (16*grid_shape[1],10*grid_shape[0])
                outpath = f'plot_TH2Ds__{rg}{beam_suffix}__{ch}__2d_{kinvar_x}_{kinvar_y}__1d_{binvar}.pdf'
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
