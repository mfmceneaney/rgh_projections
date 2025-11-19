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
export YAML=args_fullbin.yaml
export YAML2=args.yaml

echo $OUTDIR
echo $YAML

cd $OUTDIR
ls -lrth
pwd
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds $YAML"
RGH_SAGA_COMMAND "getBinKinematicsTH2Ds $YAML2"
echo DONE
