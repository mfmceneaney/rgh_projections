#!/bin/bash

#SBATCH --job-name=rgh_simulation
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH -c 1
#SBATCH --mem-per-cpu=2000
#SBATCH --gres=disk:5000
#SBATCH --time=48:00:00

$RGH_PROJECTIONS_HOME/jobs/rgh_simulation/mc_rgh/job.sh
