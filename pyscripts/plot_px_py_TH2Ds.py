# Basic imports
import numpy as np
import os
import sys
import uproot as ur
import matplotlib.pyplot as plt
from matplotlib import colors
import argparse

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
    plot_watermark,
)

parser = argparse.ArgumentParser(description='Script to plot 2d px py plots from `getBinKinematicsTH2Ds` jobs for RGC and RGH single and dipion data and MC.')
parser.add_argument('--watermark', action="store_true", help='Plot watermark on plots')
parser.add_argument('--rgs', default=["dt_rgc"], help='Run group', nargs="+", choices=['dt_rgc','mc_rgc','mc_rgh'])
parser.add_argument('--chs', default=["pi"], help='Channels', nargs="+", choices=['pi','pim','pipim','k','km'])
args = parser.parse_args()

# Set base directory from environment
RGH_PROJECTIONS_HOME = os.environ['RGH_PROJECTIONS_HOME']

# Set channels and beam suffixes to loop
chs = args.chs #['pi','pim','pipim']#,'k','km']
ch_labels = {'e':'e^{-}','pi':'\\pi^{+}','pim':'\\pi^{-}','pipim':'\\pi^{+}\\pi^{-}','k':'K^{+}','km':'K^{-}'}
beam_suffixes = ['']#,'_22GeV']
rgs = args.rgs #['dt_rgc','mc_rgc','mc_rgh', 'mc_rgh_sector4']
rg_labels = {'dt_rgc':'Data RGC','mc_rgc':'MC RGC','mc_rgh':'MC RGH','mc_rgh_sector4':'MC RGH with Sector 4'}
ps = {
    "pi":["e","pi"],
    "pi":["e","pi"],
    "pipim":["e","pi","pim"],
}
plims = {
    "pi": {
        "e":  [-2.0,2.0],
        "pi": [-1.25,1.25],
    },
    "pim": {
        "e":  [-2.0,2.0],
        "pim": [-1.25,1.25],
    },
    "pipim": {
        "e":  [-2.0,2.0],
        "pi": [-1.25,1.25],
        "pim": [-1.25,1.25],
    },
}
sector4_configs = {
    "pi":[
        "_onlysector4_e",
        "_onlysector4_pi",
        "_onlysector4",
        "_sector4_any",
        "_sector4",
        "",
    ],
    "pim":[
        "_onlysector4_e",
        "_onlysector4_pim",
        "_onlysector4",
        "_sector4_any",
        "_sector4",
        "",
    ],
    "pipim":[
        "_onlysector4_e",
        "_onlysector4_pi",
        "_onlysector4_pim",
        "_onlysector4",
        "_sector4_any",
        "_sector4",
        "",
    ],
}
# Loop run groups, channels, and beam suffixes
for rg in rgs:
    for ch in chs:
        for beam_suffix in beam_suffixes:
            for p in ps[ch]:
                for sector4_config in sector4_configs[ch]:

                    # Set bin variable labels and limits inside loop since they depend on channel and energy
                    binvar_labels = {
                        f'px_{p}':'$p_{x'+ch_labels[p]+'}$ (GeV)',
                        f'py_{p}':'$p_{y'+ch_labels[p]+'}$ (GeV)'
                    }
                    binvar_lims = {
                        f'px_{p}': plims[ch][p],
                        f'py_{p}': plims[ch][p],
                    }

                    # Set bin scheme variable pairs to loop
                    binvars_pairs = [[f'px_{p}', f'py_{p}']]
                    binvars_pairs_simple = [['px', 'py']]

                    for binvars, binvars_simple in zip(binvars_pairs, binvars_pairs_simple):

                        # Setup, modify these as needed for your specific binning scheme
                        sep = '_'
                        hist_path = os.path.abspath(
                            os.path.join(
                                RGH_PROJECTIONS_HOME,
                                f'jobs/saga/test_getBinKinematicsTH2Ds__{ch}{beam_suffix}/',
                                f'out_{rg}_2d_bins_{sep.join(binvars_simple)}{sector4_config}_binscheme_kinematics.root'
                            )
                        )
                        hist_name       = 'h2_bin0_'+sep.join(binvars)
                        binscheme_name  = 'binscheme' #NOTE: Use `binscheme_grid` in the example yaml to plot some grid bin scheme limits.
                        outpath         = f'plot_px_py_TH2Ds_{binvars[0]}_{binvars[1]}_{rg}_{ch}{beam_suffix}{sector4_config}.pdf'
                        var_keys        = binvars #NOTE: This should only be set in the case of a 2D grid scheme.
                        start_idx       = 0
                        id_key          = 'bin_id'

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
                        ax.set_title(f'{rg_labels[rg]} ${ch_labels[ch]}$',usetex=True)

                        # Plot watermark
                        if args.watermark:
                            watermark = "CLAS12 Preliminary"
                            plot_watermark(
                                watermark,
                                size=75,
                                rotation=25.0,
                                color="gray",
                                alpha=0.5,
                            )

                        # Save the figure
                        f.savefig(outpath)

                        # Close the plots
                        plt.close('all')
