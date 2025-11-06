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

# Run full bin jobs
RGH_SAGA_COMMAND getBinKinematicsTH2Ds args_fullbin.yaml
RGH_SAGA_COMMAND getBinKinematicsTH2Ds args_px_py.yaml
RGH_SAGA_COMMAND getBinKinematicsTH2Ds args_px_py_sector4.yaml
RGH_SAGA_COMMAND getBinKinematicsTH2Ds args_px_py_nosector4.yaml
RGH_SAGA_COMMAND getBinKinematicsTH2Ds args_px_py_JUST_sector4.yaml
RGH_SAGA_COMMAND getBinKinematicsTH2Ds args_px_py_JUST_sector4_e.yaml
RGH_SAGA_COMMAND getBinKinematicsTH2Ds args_px_py_JUST_sector4_pi.yaml

# Run 4d jobs
RGH_SAGA_COMMAND getBinKinematicsTH2Ds args.yaml

echo DONE
