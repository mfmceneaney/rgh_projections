# Basic imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Import saga modules
SAGA_HOME = os.environ['SAGA_HOME']
sys.path.append(os.path.abspath(os.path.join(SAGA_HOME,'py')))
from saga.aggregate import set_default_plt_settings

# Set base directory from environment
RGH_PROJECTIONS_HOME = os.environ['RGH_PROJECTIONS_HOME']

# Set plt settings
set_default_plt_settings()

# Set csv keys
xkey = 'x'
ratio_key = 'acceptanceratio'

# Set plotting parameters
figsize = (16,10)
title = 'Ratio of Acceptance Rates'
ylabel = '$R_{S \\neq 4}/R_{All}$'
ylims = [0.0,1.1]

# Set input directories
rgh_mc_names = ['_sector4',''] #NOTE: ORDER IS OLD/DENOMINATOR (Sector4) , NEW/NUMERATOR (No Sector4)
dir_old = os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,'jobs/saga/test_getKinBinnedAsym__rgc_dt__'+ch+'__1D'))
dir_new = os.path.abspath(os.path.join(RGH_PROJECTIONS_HOME,'jobs/saga/test_getKinBinnedAsym__rgc_dt__'+ch+'__1D'))

# Set channels and labels
channels = ['pi', 'pim', 'pipim']
ch_labels = ['\\pi^{+}', '\\pi^{-}', '\\pi^{+}\\pi^{-}']

# Loop channels
for ch, ch_label in zip(channels, ch_labels):

    # Set info for kinematic variables
    kinvars = [
        'x',
        'z_'+ch,
        'mx_'+ch,
        'phperp_'+ch,
    ]
    if 'pipim' == ch: kinvars.append('mass_'+ch)

    kinvar_labels = [
        '$x$',
        '$z_{'+ch_label+'}$',
        '$M_{X,'+ch_label+'}$ (GeV)',
        '$P_{\perp, '+ch_label+'}$ (GeV)',
        '$M_{'+ch_label+'}$ (GeV)',
    ]

    kinvar_lims = [
        [0,1],
        [0,1],
        [1.5,3.5],
        [0.0,1.25],
        [0,3],
    ]

    # Set file names
    file_names_old = [
        f'aggregate______inject_seed_1__sgasyms_0.1___{kinvar}'+rgh_mc_names[0]+'_a0.pdf_rescaled.csv' for kinvar in kinvars
    ]
    file_names_new = [
        f'aggregate______inject_seed_1__sgasyms_0.1___{kinvar}'+rgh_mc_names[1]+'_a0.pdf_rescaled.csv' for kinvar in kinvars
    ]

    # Load dataframes
    dfs_old = [
        pd.read_csv(os.path.join(dir_old,file_name)) for file_name in file_names_old
    ]
    dfs_new = [
        pd.read_csv(os.path.join(dir_new,file_name)) for file_name in file_names_new
    ]

    # Loop kinvars and plot and save
    for kinvar, kinvar_label, kinvar_lim, df_old, df_new in zip(kinvars, kinvar_labels, kinvar_lims, dfs_old, dfs_new):

        # Open plot
        fig, ax = plt.subplots(figsize=figsize)

        # Set titles and limits
        ax.set_title(title,usetex=True)
        ax.set_xlabel(kinvar_label,usetex=True)
        ax.set_ylabel(ylabel,usetex=True)
        ax.set_ylim(ylims)
        ax.set_xlim(kinvar_lim)

        # Plot axis line
        ax.axhline(1.0, color='black',linestyle='-',linewidth=1.0)

        # Plot ratios
        ratios = np.divide(df_new[ratio_key], df_old[ratio_key])
        ax.errorbar(
            df_new[xkey],ratios,xerr=None,yerr=None,
                        elinewidth=0, capsize=0,
                        color='tab:blue', marker='o', alpha=1.0,
                        linewidth=0, markersize=20)
        
        # Save and close figure
        ratio_name = '_'.join(rgh_mc_names)
        outpath = os.path.join(dir_new, ratio_key+f'_ratio__{ratio_name}__{kinvar}.pdf')
        print("INFO: outpath = ",outpath)
        fig.savefig(outpath)
        plt.close(fig)
