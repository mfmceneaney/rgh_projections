#!/bin/bash

#SBATCH --job-name=mc_rgc_c12analysis
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH -c 2
#SBATCH --mem-per-cpu=2000
#SBATCH --gres=disk:1000
#SBATCH --time=6:00:00

$RGH_PROJECTIONS_HOME/jobs/c12analysis/mc_rgc/job.sh
