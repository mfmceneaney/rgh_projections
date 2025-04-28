#!/bin/bash

# Set variables for this project
export RGH_PROJECTIONS_HOME=$PWD
export RGH_PROJECTIONS_VOL_DIR="/volatile/clas12/users/$USER/rgh_projections" #NOTE: CHANGE AS NEEDED.

# Set variables for rgh_simulation
export RGH_SIM_HOME=/work/clas12/users/$USER/rgh_simulation #NOTE: CHANGE AS NEEDED. This is a path to your local repo of: https://github.com/mfmceneaney/rgh_simulation for gcard and service yaml files for `gemc` and `recon-util`.

# Set variables for coatjava==11.0.1
export MYCLASDIRBIN="/work/clas12/users/$USER/coatjava/coatjava/bin"
export CLAS12DIR="/work/clas12/users/$USER/coatjava/coatjava/bin"

# Set variables for saga
export SAGA_HOME="/work/clas12/users/$USER/saga" #NOTE: CHANGE AS NEEDED. This is a path to your local repo of: https://github.com/mfmceneaney/saga
export SAGA_BUILD_DIR="$SAGA_HOME/build"

# Set variables for clasdis
export CLASDIS_TARG=proton
export CLASDIS_NMAX=10000
export CLASDIS_TRIG=10000000
export CLASDIS_POL=1
export CLASDIS_PREFIX=out_tp_
export CLASDIS_GEN_PM=1

# Set beam energies and target lund pids for clasdis and CLAS12-Analysis #NOTE: CHANGE AS NEEDED
export BEAM_ENERGY_RGA=10.6
export TPID_RGA=2212
export BEAM_ENERGY_RGC=10.55
export TPID_RGC=2212
export BEAM_ENERGY_RGH=10.6
export TPID_RGH=2212
export BEAM_ENERGY_RGC_22GeV=22.0
export TPID_RGC_22GeV=2212
export BEAM_ENERGY_RGH_22GeV=22.0
export TPID_RGH_22GeV=2212

# Set target spin vectors for CLAS12-Analysis
export TSPIN_RGC="0 0 1"
export TSPIN_RGH="1 0 0"

# Set prexisting HIPO data paths for CLAS12-Analysis #NOTE: CHANGE AS NEEDED
export RGA_MC_DIR="/cache/clas12/rg-a/production/montecarlo/clasdis_pass1/fall2018/torus-1/v1/bkg45nA_10604MeV/*.hipo"
export RGC_MC_DIR_TP1="/work/cebaf24gev/sidis/reconstructed/polarized-plus-10.5GeV-proton/hipo/"
export RGC_MC_DIR_TM1="/work/cebaf24gev/sidis/reconstructed/polarized-minus-10.5GeV-proton/hipo/"
export RGA_DT_DIR="/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v1/dst/train/nSidis/"
export RGC_DT_DIR="/cache/clas12/rg-c/production/fall22/pass1/NH3/dst/train/sidisdvcs/"
export RGC_MC_DIR_TP1_22GeV="/work/cebaf24gev/sidis/reconstructed/polarized-plus-22GeV-proton/hipo/"
export RGC_MC_DIR_TM1_22GeV="/work/cebaf24gev/sidis/reconstructed/polarized-minus-22GeV-proton/hipo/"

# Set project HIPO data paths for CLAS12-Analysis #NOTE: CHANGE AS NEEDED
export RGH_MC_DIR="$RGH_PROJECTIONS_VOL_DIR/jobs/rgh_simulation/mc_rgh/dst"
export RGH_MC_DIR_22GeV="$RGH_PROJECTIONS_VOL_DIR/jobs/rgh_simulation/mc_rgh_22GeV/dst"

# Set path to target polarization csv for RGC data and saga
export RGC_TPOL_CSV="/work/clas12/users/gmat/RGC_Tpol_maxLikelihood_fall22_4_16_2025.csv"
