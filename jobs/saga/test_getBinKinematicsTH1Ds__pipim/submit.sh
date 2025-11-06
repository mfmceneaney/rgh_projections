#!/bin/bash

#SBATCH --job-name=saga_getBinKinematicsTH1Ds
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH -c 4
#SBATCH --mem-per-cpu=2G
#SBATCH --gres=disk:1000
#SBATCH --time=24:00:00

export OUTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export YAML=args.yaml

echo $OUTDIR
echo $YAML

cd $OUTDIR
ls -lrth
pwd

# Run full bin jobs
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_fullbin.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_fullbin_sector4.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgc_fullbin.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_dt_rgc_fullbin.yaml

# Run 1D jobs
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_1d_bins.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_1d_bins_sector4.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgc_1d_bins.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_dt_rgc_1d_bins.yaml

# Run delta phi jobs
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_fullbin_dphi.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_fullbin_dphi_sector4.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_fullbin_dphi_nosector4.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_fullbin_dphi_JUST_sector4.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_fullbin_dphi_JUST_sector4_e.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_fullbin_dphi_JUST_sector4_pi.yaml
RGH_SAGA_COMMAND getBinKinematicsTH1Ds args_mc_rgh_fullbin_dphi_JUST_sector4_pim.yaml

echo DONE
