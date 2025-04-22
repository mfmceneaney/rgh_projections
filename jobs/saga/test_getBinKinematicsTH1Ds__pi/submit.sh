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

export MYEXECUTABLE=$SAGA_BUILD_DIR/saga/getBinKinematicsTH1Ds
export OUTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export YAML=args.yaml

echo $MYEXECUTABLE
echo $OUTDIR
echo $YAML

cd $OUTDIR
ls -lrth
pwd

# Run full bin jobs
$MYEXECUTABLE args_mc_rgh_fullbin.yaml
$MYEXECUTABLE args_mc_rgh_fullbin_sector4.yaml
$MYEXECUTABLE args_mc_rgc_fullbin.yaml
$MYEXECUTABLE args_dt_rgc_fullbin.yaml

# Run 1D jobs
$MYEXECUTABLE args_mc_rgh_1d_bins.yaml
$MYEXECUTABLE args_mc_rgh_1d_bins_sector4.yaml
$MYEXECUTABLE args_mc_rgc_1d_bins.yaml
$MYEXECUTABLE args_dt_rgc_1d_bins.yaml

# Run delta phi jobs
$MYEXECUTABLE args_mc_rgh_fullbin_dphi.yaml
$MYEXECUTABLE args_mc_rgh_fullbin_dphi_sector4.yaml
$MYEXECUTABLE args_mc_rgh_fullbin_dphi_nosector4.yaml
$MYEXECUTABLE args_mc_rgh_fullbin_dphi_JUST_sector4.yaml
$MYEXECUTABLE args_mc_rgh_fullbin_dphi_JUST_sector4_e.yaml
$MYEXECUTABLE args_mc_rgh_fullbin_dphi_JUST_sector4_pi.yaml

echo DONE
