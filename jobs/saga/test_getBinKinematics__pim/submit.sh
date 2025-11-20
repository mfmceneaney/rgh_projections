#!/bin/bash

#SBATCH --job-name=saga_getBinKinematics_pim
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH -c 4
#SBATCH --mem-per-cpu=2G
##SBATCH --gres=disk:1000
#SBATCH --time=8:00:00

export OUTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo $OUTDIR

cd $OUTDIR
ls -lrth
pwd

# DT RGC Kinematics
RGH_SAGA_COMMAND "getBinKinematics args_dt_rgc_1d_bins.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_dt_rgc_2d_bins_x_Q2.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_dt_rgc_2d_bins_z_pT.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_dt_rgc_4d_bins.yaml"

# MC RGC Kinematics
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgc_1d_bins.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgc_2d_bins_x_Q2.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgc_2d_bins_z_pT.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgc_4d_bins.yaml"

# MC RGH Kinematics
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgh_1d_bins.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgh_2d_bins_x_Q2.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgh_2d_bins_z_pT.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgh_4d_bins.yaml"

# MC RGH Kinematics with sector 4
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgh_sector4_1d_bins.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgh_sector4_2d_bins_x_Q2.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgh_sector4_2d_bins_z_pT.yaml"
RGH_SAGA_COMMAND "getBinKinematics args_mc_rgh_sector4_4d_bins.yaml"

echo DONE
