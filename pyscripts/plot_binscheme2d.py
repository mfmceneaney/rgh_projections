# Basic imports
import numpy as np
import os
import sys
import uproot as ur
import matplotlib.pyplot as plt
from matplotlib import colors

# Import saga modules
from saga.aggregate import get_binscheme_cuts_and_ids
from saga.data import load_yaml, load_th1, load_csv
from saga.plot import (
    set_default_plt_settings,
    plot_th2,
    get_lims_coords,
    plot_lines,
    get_bin_centers,
    plot_bin_ids,
)

# Set base directory from environment
RGH_PROJECTIONS_HOME = os.environ['RGH_PROJECTIONS_HOME']

# Set channels and beam suffixes to loop
chs = ['pi','pim','pipim','k','km']
ch_labels = {'pi':'\\pi^{+}','pim':'\\pi^{-}','pipim':'\\pi^{+}}\\pi^{-}','k':'K^{+}','km':'K^{-}'}
beam_suffixes = ['','_22GeV']

# Loop channels and beam suffixes
for ch in chs:
    for beam_suffix in beam_suffixes:

        # Set bin variable labels and limits inside loop since they depend on channel and energy
        binvar_labels = {
            'x':'$x$','Q2':'$Q^{2}$ (GeV)$^{2}$',
            f'z_{ch}':'$z_{'+ch_labels[ch]+'}$',f'phperp_{ch}':'$P_{\\perp, '+ch_labels[ch]+'}$ (GeV)',f'phperp2_{ch}':'$P^{2}_{\\perp, '+ch_labels[ch]+'}$ (GeV$^{2}$)'
        }
        binvar_lims = {
            'x':[0.0,1.0],
            'Q2':[1.0,22.0] if beam_suffx=='_22GeV' else [1.0,11.0],
            f'z_{ch}':[0.0,1.0],
            f'phperp_{ch}':[0.0,2.25] if beam_suffx=='_22GeV' else [0.0,1.25],
            f'phperp2_{ch}':[0.0,5.0] if beam_suffx=='_22GeV' else [0.0,1.6],
        }

        # Set bin scheme variable pairs to loop
        binvars_pairs = [['x','Q2'],[f'z_{ch}', f'phperp_{ch}']]
        binvars_pairs_simple = [['x','Q2'],[f'z', 'pT']]

        for binvars, binvars_simple in zip(binvars_pairs, binvars_pairs_simple):

            # Setup, modify these as needed for your specific binning scheme
            sep             = '_'
            kinematics_path = os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getBinKinematics__{ch}{beam_suffix}/out_{sep.join(binvars_simple)}_binscheme_kinematics.csv'))
            yaml_path       = os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'yamls/out_2d_bins_{ch}_{sep.join(binvars_simple)}{beam_suffix}.yaml'))
            hist_path       = os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,f'jobs/saga/test_getBinKinematicsTH2Ds__{ch}{beam_suffix}/out_{rg}{beam_suffix}_fullbin_kinematics.root'))
            hist_name       = 'h2_bin0_'+sep.join(binvars)
            binscheme_name  = 'binscheme' #NOTE: Use `binscheme_grid` in the example yaml to plot some grid bin scheme limits.
            outpath         = f'binscheme2d_{binvars[0]}_{binvars[1]}_{ch}{beam_suffix}.pdf'
            var_keys        = binvars #NOTE: This should only be set in the case of a 2D grid scheme.
            start_idx       = 0
            id_key          = 'bin_id'

            # Read bin scheme from YAML
            yaml_args = load_yaml(yaml_path)
            binscheme = yaml_args[binscheme_name]

            # Load TH2 histogram with uproot
            h2 = load_th1(hist_path,name=hist_name)

            # Set plt settings
            set_default_plt_settings()

            # Open the figure
            f, ax = plt.subplots(figsize=(16,10))

            # Plot the 2D distribution
            plot_th2(h2, ax, norm=colors.LogNorm())
            ax.set_xlabel(binvar_labels[binvars[0]],usetex=True)
            ax.set_ylabel(binvar_labels[binvars[1]],usetex=True)
            ax.set_title(f'${ch_labels[ch]}$ Bin Scheme',usetex=True)

            # Get the bin limit line coordinates and plot
            lims_coords = get_lims_coords(binscheme, binvar_lims[binvars[0]], binvar_lims[binvars[1]], var_keys=var_keys)
            plot_lines(ax, lims_coords, linecolor='red', linewidth=1)

            # Get bin scheme cuts and ids
            cuts, _, _, _ = get_binscheme_cuts_and_ids(
                                                                binscheme,
                                                                start_idx=start_idx,
                                                                id_key=id_key,
                                                                binvar_titles=None,
                                                            )

            # Get the bin centers
            bin_centers, bin_widths = get_bin_centers(cuts,swap_axes=False)

            # # Plot the bin ids
            # plot_bin_ids(
            #         ax,
            #         bin_centers, 
            #         bin_widths=bin_widths,
            #         size=25,
            #         color='red',
            #         alpha=1.0,
            #     )

            # Load average kinematics in each bin and plot
            kinematics = load_csv(kinematics_path)
            bin_centers_x = [kinematics[binvars[0]][idx].item() for idx in bin_ids[id_key]]
            bin_centers_y = [kinematics[binvars[1]][idx].item() for idx in bin_ids[id_key]]
            ax.scatter(bin_centers_x, bin_centers_y, s=150, linewidth=4, color='black', marker='x',label='Bin Means')
            ax.legend(loc='upper left' if binvars[0] == 'x' else 'upper right')

            # Save the figure
            f.savefig(outpath)
