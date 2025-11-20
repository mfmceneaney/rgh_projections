# Python scripts

To run the following scripts source your virtual environment after installing saga.

First run the 1d asymmetry injection jobs with the orchestration scripts.
```
orchestrate_jobs_getKinBinnedAsym_dt_1d_bins.py
orchestrate_jobs_getKinBinnedAsym_mc_1d_bins.py
```
Then, once those jobs have all finished successfully run the aggregation scripts for the 1d asymmetries.
```
aggregate_jobs_getKinBinnedAsym_dt_1d_bins.py
aggregate_jobs_getKinBinnedAsym_mc_1d_bins.py
```

Similarly, for the 4d asymmetries, use the following two scripts to orchestrate jobs.
```
orchestrate_jobs_getKinBinnedAsym_mc_4d_bins.py
orchestrate_jobs_getKinBinnedAsym_dt_4d_bins.py
```
Then, rescale those asymmetries with the following script.
```
rescale_jobs_getKinBinnedAsym_dt_4d_bins.py
```

To plot acceptance ratios in 1d bin schemes for RGH run the following script after successful completion of the 1d asymmetry injection jobs, and after running the data aggregations script for the 1d jobs which will also run the rescaling.
```
plot_acceptance_ratios_dt_1d_bins.py
```

To plot the 2d binschemes in $x$ and $Q^2$ and $z$ and $p_{T}$, run the following script after running the `getBinKinematicsTH2Ds` jobs.
```
plot_binscheme2d.py
```

To plot select 1d and 2d kinematic distributions after running the `getBinKinematics`, `getBinKinematicsTH1Ds`, and `getBinKinematicsTH2Ds` jobs, run the following scripts.
```
plot_TH1Ds.py
plot_TH2Ds.py
```

To aggregate output from `getBinKinematics`, `getBinKinematicsTH1Ds`, and `getBinKinematicsTH2Ds` jobs for 22GeV into csv files use the following.
```
convert_root_to_csv_getKinBinnedAsym_rgh_mc_22GeV.py
```

To generate formulas for dihadron asymmetries use the following.
```
create_dihadron_formulas.py
create_theta_integrated_dihadron_formulas.py
```




README.md
rescale_jobs_getKinBinnedAsym_dt_4d_bins.py

#

Contact: matthew.mceneaney@duke.edu
