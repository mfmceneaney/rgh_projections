#!/bin/bash

# Set variables for this project
export RGH_PROJECTIONS_HOME=$PWD
export RGH_PROJECTIONS_VOL_DIR="/volatile/clas12/users/$USER/rgh_projections" #NOTE: CHANGE IF YOU ARE USER OR STAFF.

# Set variables for rgh_simulation
export RGH_SIM_HOME=/volatile/clas12/users/$USER/rgh_simulation #NOTE: CHANGE AS NEEDED. This is a path to your local repo of: https://github.com/mfmceneaney/rgh_simulation for gcard and service yaml files for `gemc` and `recon-util`.

# Set variables for saga
export SAGA_BUILD_DIR="/volatile/clas12/users/$USER/saga/build" #NOTE: CHANGE AS NEEDED. This is the build directory for your local repo of: https://github.com/mfmceneaney/saga

# Set prexisting HIPO data paths for CLAS12-Analysis #NOTE: CHANGE AS NEEDED
export RGA_MC_DIR="/cache/clas12/rg-a/production/montecarlo/clasdis_pass1/fall2018/torus-1/v1/bkg45nA_10604MeV/*.hipo"
export RGC_MC_DIR="/work/cebaf24gev/sidis/reconstructed/polarized-plus-10.5GeV-proton/hipo/"
export RGA_DT_DIR="/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v1/dst/train/nSidis/"
export RGC_DT_DIR="/cache/clas12/rg-c/production/fall22/pass1/NH3/dst/train/sidisdvcs/"
export RGC_MC_DIR_22GeV="/work/cebaf24gev/sidis/reconstructed/polarized-plus-22GeV-proton/hipo/"

# Set project HIPO data paths ffor CLAS12-Analysis #NOTE: CHANGE AS NEEDED
export RGH_MC_DIR="$RGH_PROJECTIONS_VOL_DIR/jobs/rgh_simulation/rgh_mc/dst"
export RGH_MC_DIR_22GeV="$RGH_PROJECTIONS_VOL_DIR/jobs/rgh_simulation/rgh_mc_22GeV/dst"

# Set beam energies and target lund pids for CLAS12-Analysis #NOTE: CHANGE AS NEEDED
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

# Set paths in yaml files for saga
for file in $RGH_PROJECTIONS_HOME/jobs/*/*/*.yaml; do
    sed -i.bak "s;/RGH_PROJECTIONS_HOME;$RGH_PROJECTIONS_HOME;g" $file
    sed -i.bak "s;/RGH_PROJECTIONS_WORK_DIR;$RGH_PROJECTIONS_WORK_DIR;g" $file
    sed -i.bak "s;/RGH_PROJECTIONS_VOL_DIR;$RGH_PROJECTIONS_VOL_DIR;g" $file
    sed -i.bak "s;/RGA_MC_DIR;$RGA_MC_DIR;g" $file
    sed -i.bak "s;/RGC_MC_DIR;$RGC_MC_DIR;g" $file
    sed -i.bak "s;/RGA_DT_DIR;$RGA_DT_DIR;g" $file
    sed -i.bak "s;/RGC_DT_DIR;$RGC_DT_DIR;g" $file
    sed -i.bak "s;/RGC_MC_DIR_22GeV;$RGC_MC_DIR_22GeV;g" $file
done

# Set paths in python scripts using saga outputs #TODO: JUST SET THESE FROM ENVIRONMENT VARIABLES. #TODO: COPY TO CSH SCRIPT TOO
for file in $RGH_PROJECTIONS_HOME/pyscripts/*.py; do
    sed -i.bak "s;/RGH_PROJECTIONS_HOME;$RGH_PROJECTIONS_HOME;g" $file
done
