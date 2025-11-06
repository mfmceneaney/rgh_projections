#!/bin/csh

#----- SET DEFAULT VARIABLES -----#

# Set variables for clasdis
setenv CLASDIS_HOME "/work/clas12/users/$USER/clasdis"
setenv CLASDIS_TARG proton
setenv CLASDIS_NMAX 10000
setenv CLASDIS_TRIG 10000000
setenv CLASDIS_POL 1
setenv CLASDIS_PREFIX out_tp_
setenv CLASDIS_GEN_PM 1

# Set beam energies and target lund pids for clasdis and CLAS12-Analysis
setenv BEAM_ENERGY_RGA 10.6
setenv TPID_RGA 2212
setenv BEAM_ENERGY_RGC 10.55
setenv TPID_RGC 2212
setenv BEAM_ENERGY_RGH 10.6
setenv TPID_RGH 2212
setenv BEAM_ENERGY_RGC_22GeV 22.0
setenv TPID_RGC_22GeV 2212
setenv BEAM_ENERGY_RGH_22GeV 22.0
setenv TPID_RGH_22GeV 2212

# Set target spin vectors for CLAS12-Analysis
setenv TSPIN_RGC "0 0 1"
setenv TSPIN_RGH "0 1 0"

# Set preexisting HIPO data paths for CLAS12-Analysis
setenv RGA_MC_DIR "/cache/clas12/rg-a/production/montecarlo/clasdis_pass1/fall2018/torus-1/v1/bkg45nA_10604MeV/*.hipo"
setenv RGC_MC_DIR_TP1 "/work/cebaf24gev/sidis/reconstructed/polarized-plus-10.5GeV-proton/hipo/"
setenv RGC_MC_DIR_TM1 "/work/cebaf24gev/sidis/reconstructed/polarized-minus-10.5GeV-proton/hipo/"
setenv RGA_DT_DIR "/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v1/dst/train/nSidis/"
setenv RGC_DT_DIR "/cache/clas12/rg-c/production/fall22/pass1/NH3/dst/train/sidisdvcs/"
setenv RGC_MC_DIR_TP1_22GeV "/work/cebaf24gev/sidis/reconstructed/polarized-plus-22GeV-proton/hipo/"
setenv RGC_MC_DIR_TM1_22GeV "/work/cebaf24gev/sidis/reconstructed/polarized-minus-22GeV-proton/hipo/"

# Set output directory for slurm job stdout and stderr
setenv RGH_PROJECTIONS_FARM_OUT "/farm_out/$USER"

# Set directory paths
setenv RGH_PROJECTIONS_VOL_DIR "/volatile/clas12/users/$USER/rgh_projections"

# Set variables for rgh_simulation
setenv RGH_SIM_HOME "/work/clas12/users/$USER/rgh_simulation"

# Set image paths
setenv RGH_PROJECTIONS_GEMC_IMG "gemc_dev-almalinux94/"
setenv RGH_PROJECTIONS_CCFA_IMG "analysis.sif"
setenv RGH_PROJECTIONS_C12A_IMG "clas12-analysis.sif"
setenv RGH_PROJECTIONS_SAGA_IMG "saga.sif"

#----- LOAD VARIABLES -----#
# Load and overwrite variables from env.txt
if (-e env.txt) then
    foreach line (`grep -v '^#' env.txt`)
        set var = `echo $line | cut -d= -f1`
        set val = `echo $line | cut -d= -f2-`
        setenv $var "$val"
    end
endif

#----- STATIC VARIABLES -----#
setenv RGH_PROJECTIONS_HOME "`pwd`"

#----- DEPENDENT VARIABLES -----#

setenv CLASDIS_PDF "$CLASDIS_HOME/pdf"
setenv RGH_CLADIS_COMMAND "$CLASDIS_HOME/clasdis"

alias RGH_GEMC_COMMAND "apptainer exec -B $RGH_PROJECTIONS_VOL_DIR,$RGH_PROJECTIONS_HOME $RGH_PROJECTIONS_GEMC_IMG bash -c \"module use /cvmfs/oasis.opensciencegrid.org/jlab/geant4/modules; module load gemc/5.11; gemc \!*\""
setenv RGH_RECON_UTIL_COMMAND "apptainer exec -B $RGH_PROJECTIONS_VOL_DIR,$RGH_PROJECTIONS_HOME $RGH_PROJECTIONS_CCFA_IMG bash /opt/coatjava/bin/recon-util"
setenv RGH_HIPO_UTILS_COMMAND "apptainer exec -B $RGH_PROJECTIONS_VOL_DIR,$RGH_PROJECTIONS_HOME $RGH_PROJECTIONS_CCFA_IMG bash /opt/coatjava/bin/hipo-utils"
setenv RGH_C12ANALYSIS_COMMAND "apptainer run -B $RGH_PROJECTIONS_VOL_DIR,$RGH_PROJECTIONS_HOME $RGH_PROJECTIONS_C12A_IMG"
alias RGH_SAGA_COMMAND "apptainer exec -B $RGH_PROJECTIONS_VOL_DIR,$RGH_PROJECTIONS_HOME $RGH_PROJECTIONS_SAGA_IMG bash -c \"\!*\""

# Set project HIPO data paths for CLAS12-Analysis
setenv RGH_MC_DIR "$RGH_PROJECTIONS_VOL_DIR/jobs/rgh_simulation/mc_rgh/dst"
setenv RGH_MC_DIR_22GeV "$RGH_PROJECTIONS_VOL_DIR/jobs/rgh_simulation/mc_rgh_22GeV/dst"

# Set path to target polarization csv for RGC data and saga
setenv RGC_TPOL_CSV "$RGH_PROJECTIONS_HOME/csvs/RGC_Tpol_maxLikelihood_fall22_4_16_2025.csv"
