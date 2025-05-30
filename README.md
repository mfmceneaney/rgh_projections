# RGH Projections

This is a storage repository for yamls and scripts used to create the RGH $\delta A_{UT}$ uncertainty projections.

# Prerequisites
* Assumedly, you are working on ifarm and can use slurm to submit jobs
* [rgh_simulation](https://github.com/mfmceneaney/rgh_simulation.git)
* [CLAS12-Analysis](https://github.com/mfmceneaney/CLAS12-Analysis.git)
* [saga](https://github.com/mfmceneaney/saga.git)

# Installation

Begin by cloning the repository:
```bash
git clone https://github.com/mfmceneaney/rgh_projections.git
```

Make sure all the paths in the environment script&mdash;[bin/env.sh](bin/env.sh) or [bin/env.csh](bin/env.csh)&mdash;are correct for you.
In particular, you will need to manually set these variables in the environment script depending on your local installation paths and the paths for existing data and MC samples you wish to use:
`RGH_PROJECTIONS_VOL_DIR`, `RGH_SIM_HOME`,`SAGA_BUILD_DIR`, `RG?_MC_DIR*`.
Yaml paths will be set based on the paths given in the environment script.

After configuring your environment script, add the following to your (bash) startup script:
```bash
# Set up RGH projections https://github.com/mfmceneaney/rgh_projections.git
pushd /path/to/rgh_projections >> /dev/null
source bin/env.sh
popd >> /dev/null
```

# Overview

First you must produce RGH simulation HIPO files using the directories in `jobs/rgh_simulation/`.
To submit the simulation jobs, cd into the relevant directory and run:
```bash
touch jobs.txt
sbatch clasdis_submit.sh >> jobs.txt
```
Once this job has finished, run:
```bash
touch jobs.txt
./setup.sh >> jobs.txt
```

Then, you have to produce channel-specific event-level ROOT files using the directories in `jobs/c12analysis/`.
Make sure to update the paths to existing simulation and data directories for, e.g. RGA or RGC, in your environment script.
To submit these jobs, cd into the relevant directory and run:
```bash
touch jobs.txt
./setup.sh >> jobs.txt
```

Configure yamls for jobs running [saga](https://github.com/mfmceneaney/saga.git) by running `$RGH_PROJECTIONS_HOME/bin/setup.sh`.

Run kinematics jobs by going into each directory and manually submitting:
```bash
for file in jobs/saga/test_getBinKinematics*; do
    echo $file
    cd $file
    touch jobs.txt
    sbatch $PWD/submit.sh >> jobs.txt
    cd -
    echo
done
```
Then, run injection studies using the `pyscripts/orchestrate*.py` files.

Finally, aggregate results from injection studies, rescale uncertainty projections, and plot kinematics and bin schemes with the remaining scripts in `pyscripts`.

# What you can do

Here are some examples of the plots you can produce with the python scripts.

You can plot your bin schemes with average kinematics marked for each bin:

![figs/binscheme2d_x_Q2_pi.png](./figs/binscheme2d_x_Q2_pi.png)
![figs/binscheme2d_z_pT_pi.png](./figs/binscheme2d_z_pT_pi.png)

Or plot ratios of, e.g. acceptance ratios between different detector configurations, for example excluding particles from sector 4 or not. 

![figs/acceptance_ratios_x_pi.png](./figs/acceptance_ratios_x_pi.png)

And, most importantly, you can plot rescaled uncertainty projections and show the relevant kinematics distributions in the background.

![figs/projections_x_pi.png](./figs/projections_x_pi.png)

#

Contact: matthew.mceneaney@duke.edu
