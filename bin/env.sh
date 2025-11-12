#!/bin/bash

#----- SET DEFAULT VARIABLES -----#

# Set variables for clasdis
export CLASDIS_HOME="/work/clas12/users/$USER/clasdis"
export CLASDIS_TARG=proton
export CLASDIS_NMAX=10000 #NOTE: Maximum number of MC events per file
export CLASDIS_TRIG=10000000 #NOTE: Maximum number of MC events to trigger
export CLASDIS_TRIG_HALF=5000000
export CLASDIS_NJOBS=1000 #NOTE: This should be the trigger / nmax
export CLASDIS_NJOBS_HALF=500
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
export TSPIN_RGH="0 1 0"

# Set prexisting HIPO data paths for CLAS12-Analysis #NOTE: CHANGE AS NEEDED
export RGA_MC_DIR="/cache/clas12/rg-a/production/montecarlo/clasdis_pass1/fall2018/torus-1/v1/bkg45nA_10604MeV/*.hipo"
export RGC_MC_DIR_TP1="/work/cebaf24gev/sidis/reconstructed/polarized-plus-10.5GeV-proton/hipo/"
export RGC_MC_DIR_TM1="/work/cebaf24gev/sidis/reconstructed/polarized-minus-10.5GeV-proton/hipo/"
export RGA_DT_DIR="/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v1/dst/train/nSidis/"
export RGC_DT_DIR="/cache/clas12/rg-c/production/fall22/pass1/NH3/dst/train/sidisdvcs/"
export RGC_MC_DIR_TP1_22GeV="/work/cebaf24gev/sidis/reconstructed/polarized-plus-22GeV-proton/hipo/"
export RGC_MC_DIR_TM1_22GeV="/work/cebaf24gev/sidis/reconstructed/polarized-minus-22GeV-proton/hipo/"

# Set output directory for slurm job stdout and stderr
export RGH_PROJECTIONS_FARM_OUT="/farm_out/$USER"

# Set directory paths
export RGH_PROJECTIONS_VOL_DIR="/volatile/clas12/users/$USER/rgh_projections" #NOTE: CHANGE AS NEEDED.

# Set variables for rgh_simulation
export RGH_SIM_HOME="/work/clas12/users/$USER/rgh_simulation" #NOTE: CHANGE AS NEEDED. This is a path to your local repo of: https://github.com/mfmceneaney/rgh_simulation for gcard and service yaml files for `gemc` and `recon-util`.

# Set image paths
export RGH_PROJECTIONS_GEMC_IMG="gemc_dev-almalinux94/"
export RGH_PROJECTIONS_CCFA_IMG="analysis_latest.sif"
export RGH_PROJECTIONS_C12A_IMG="clas12-analysis.sif"
export RGH_PROJECTIONS_SAGA_IMG="saga.sif"

# Set the HPC partition on which you wish to run
export RGH_HPC_PARTITION="production"
export RGH_HPC_ACCOUNT="clas12"

#----- LOAD VARIABLES -----#

# Load and overwrite variables from env.txt
if [ -f env.txt ]; then
    # ignore lines starting with # and blank lines
    export $(grep -v '^#' env.txt | xargs)
fi

#----- STATIC VARIABLES -----#

# Set variables for this project
export RGH_PROJECTIONS_HOME="$PWD"

#----- DEPENDENT VARIABLES -----#

export CLASDIS_PDF="$CLASDIS_HOME/pdf"
export RGH_CLADIS_COMMAND="$CLASDIS_HOME/clasdis"

# Set command for gemc
RGH_GEMC_COMMAND() {
    apptainer exec -B $RGH_PROJECTIONS_VOL_DIR,$RGH_PROJECTIONS_HOME,$RGH_SIM_HOME $RGH_PROJECTIONS_GEMC_IMG bash -c "module use /cvmfs/oasis.opensciencegrid.org/jlab/geant4/modules; module load gemc/5.10; gemc $@" -- "$@"
}
export -f RGH_GEMC_COMMAND

# Set variables for clas12 container forge analysis image
export RGH_RECON_UTIL_COMMAND="apptainer exec -B $RGH_PROJECTIONS_VOL_DIR,$RGH_PROJECTIONS_HOME $RGH_PROJECTIONS_CCFA_IMG bash /opt/coatjava/bin/recon-util"
export RGH_HIPO_UTILS_COMMAND="apptainer exec -B $RGH_PROJECTIONS_VOL_DIR,$RGH_PROJECTIONS_HOME $RGH_PROJECTIONS_CCFA_IMG bash /opt/coatjava/bin/hipo-utils"

# Set variables for clas12-analysis
export RGH_C12ANALYSIS_COMMAND="apptainer run -B $RGH_PROJECTIONS_VOL_DIR,$RGH_PROJECTIONS_HOME $RGH_PROJECTIONS_C12A_IMG"

# Set variables for saga
RGH_SAGA_COMMAND() {
    apptainer exec -B $RGH_PROJECTIONS_VOL_DIR,$RGH_PROJECTIONS_HOME $RGH_PROJECTIONS_SAGA_IMG bash -c "$@" -- "$@"
}
export -f RGH_SAGA_COMMAND

# Set project HIPO data paths for CLAS12-Analysis #NOTE: CHANGE AS NEEDED
export RGH_MC_DIR="$RGH_PROJECTIONS_VOL_DIR/jobs/rgh_simulation/mc_rgh/dst"
export RGH_MC_DIR_22GeV="$RGH_PROJECTIONS_VOL_DIR/jobs/rgh_simulation/mc_rgh_22GeV/dst"

# Set path to target polarization csv for RGC data and saga
export RGC_TPOL_CSV="$RGH_PROJECTIONS_HOME/csvs/RGC_Tpol_maxLikelihood_fall22_4_16_2025.csv"
