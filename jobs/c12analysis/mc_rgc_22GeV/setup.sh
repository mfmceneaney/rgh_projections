#!/bin/bash
cd $RGH_PROJECTIONS_HOME/jobs/c12analysis/mc_rgc_22GeV
i=1

# First loop positive target polarization
for file in $RGC_MC_DIR_TP1_22GeV/*.hipo;
do
echo "$i > $file"
echo
cp job.sh job$i.sh
cp submit.sh submit$i.sh
sed -i "s;TSPIN_SIGN=1;TSPIN_SIGN=1;g" job$i.sh
sed -i "s;/path/test.hipo;$file;g" job$i.sh
sed -i "s;job.sh;job$i.sh;g" submit$i.sh
sbatch submit$i.sh
((i++))
done

# Then negative target polarization
for file in $RGC_MC_DIR_TM1_22GeV/*.hipo;
do
echo "$i > $file"
echo
cp job.sh job$i.sh
cp submit.sh submit$i.sh
sed -i "s;TSPIN_SIGN=1;TSPIN_SIGN=-1;g" job$i.sh
sed -i "s;/path/test.hipo;$file;g" job$i.sh
sed -i "s;job.sh;job$i.sh;g" submit$i.sh
sbatch submit$i.sh
((i++))
done
