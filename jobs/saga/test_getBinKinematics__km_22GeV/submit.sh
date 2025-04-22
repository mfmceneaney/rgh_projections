#!/bin/bash

#SBATCH --job-name=saga_getBinKinematics
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH -c 4
#SBATCH --mem-per-cpu=2G
#SBATCH --gres=disk:1000
#SBATCH --time=8:00:00

export MYEXECUTABLE=$SAGA_BUILD_DIR/saga/getBinKinematics
export OUTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export YAML=args.yaml
export YAML2=args_x_Q2.yaml
export YAML3=args_z_pT.yaml

echo $MYEXECUTABLE
echo $OUTDIR
echo $YAML

cd $OUTDIR
ls -lrth
pwd
$MYEXECUTABLE $YAML
$MYEXECUTABLE $YAML2
$MYEXECUTABLE $YAML3
echo DONE
