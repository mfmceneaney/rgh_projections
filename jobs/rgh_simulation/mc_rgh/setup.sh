#!/bin/bash
cd $RGH_PROJECTIONS_HOME/jobs/rgh_simulation/mc_rgh
i=1

export NITERATIONS=`echo "$CLASDIS_TRIG/$CLASDIS_NMAX" | bc`
export NEVENTS=$CLASDIS_NMAX
export NITERATIONS_HALF=`echo "$NITERATIONS/2" | bc`

while [ $i -le $NITERATIONS ]
do
echo "$i > $PWD/submit$i.sh"
echo

# Copy scripts
cp job.sh job$i.sh
cp submit.sh submit$i.sh

# Replace clasdis file prefix and gemc gcard depending on if the lund file has positive or negative target polarization
if ((!$CLASDIS_GEN_PM || $i<$NITERATIONS_HALF)); then
    sed -i "s;out_tp_CLASDIS_POL_;out_tp_${CLASDIS_POL}_idx_;g" job$i.sh
else
    sed -i "s;out_tp_CLASDIS_POL_;out_tp_-${CLASDIS_POL}_idx_;g" job$i.sh
fi

# Replace the other variables
sed -i "s;MCINDEX=0;MCINDEX=$i;g" job$i.sh
sed -i "s;NEVENTS=100;NEVENTS=$NEVENTS;g" job$i.sh
sed -i "s;job.sh;job$i.sh;g" submit$i.sh

# Submit job
sbatch submit$i.sh
((i++))
done
