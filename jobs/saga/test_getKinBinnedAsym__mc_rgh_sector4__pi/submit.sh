#!/bin/bash

#SBATCH --job-name=saga_getKinBinnedAsym
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH -c 1
#SBATCH --mem-per-cpu=2G
#SBATCH --gres=disk:1000
#SBATCH --time=1:00:00

export MYEXECUTABLE=$SAGA_BUILD_DIR/saga/getKinBinnedAsym
export OUTDIR=$RGH_PROJECTIONS_HOME/jobs/saga/test_getKinBinnedAsym__mc_rgh_sector4__pi
export YAML=args.yaml

echo $MYEXECUTABLE
echo $OUTDIR
echo $YAML

cd $OUTDIR
ls -lrth
pwd
$MYEXECUTABLE $YAML
echo DONE
