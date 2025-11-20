#!/bin/bash

#SBATCH --job-name=saga_getBinKinematicsTH2Ds
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH -c 4
#SBATCH --mem-per-cpu=2G
##SBATCH --gres=disk:1000
#SBATCH --time=24:00:00

export OUTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export YAML=args.yaml

echo $OUTDIR
echo $YAML

cd $OUTDIR
ls -lrth
pwd

# Run MC RGH jobs
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgh_1d_bins.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgh_2d_bins_px_py.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgh_2d_bins_px_py_sector4.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgh_2d_bins_px_py_sector4_any.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgh_2d_bins_px_py_onlysector4.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgh_2d_bins_px_py_onlysector4_pim.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgh_2d_bins_px_py_onlysector4_e.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgh_4d_bins.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgh_fullbin.yaml"

# Run MC RGC jobs
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgc_1d_bins.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgc_2d_bins_px_py.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgc_2d_bins_px_py_sector4.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgc_2d_bins_px_py_sector4_any.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgc_2d_bins_px_py_onlysector4.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgc_2d_bins_px_py_onlysector4_pim.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgc_2d_bins_px_py_onlysector4_e.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgc_4d_bins.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_mc_rgc_fullbin.yaml"

# Run DT RGC jobs
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_dt_rgc_1d_bins.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_dt_rgc_2d_bins_px_py.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_dt_rgc_2d_bins_px_py_sector4.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_dt_rgc_2d_bins_px_py_sector4_any.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_dt_rgc_2d_bins_px_py_onlysector4.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_dt_rgc_2d_bins_px_py_onlysector4_pim.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_dt_rgc_2d_bins_px_py_onlysector4_e.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_dt_rgc_4d_bins.yaml"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds args_dt_rgc_fullbin.yaml"

echo DONE
