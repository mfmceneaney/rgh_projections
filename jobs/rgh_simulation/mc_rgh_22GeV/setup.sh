#!/bin/bash
cd $RGH_PROJECTIONS_HOME/jobs/rgh_simulation/mc_rgh_22GeV
i=1

export CLASDIS_TRIG_HALF=`echo "$CLASDIS_TRIG/2" | bc`
if (($CLASDIS_TRIG_HALF<$CLASDIS_NMAX)); then
    export NITERATIONS=2
else
    export NITERATIONS=`echo "$CLASDIS_TRIG/$CLASDIS_NMAX" | bc`
fi
export NEVENTS=$CLASDIS_NMAX
export NITERATIONS_HALF=`echo "$NITERATIONS/2" | bc`

# Loop number of files
while [ $i -le $NITERATIONS ]
do
echo "$i > $PWD/submit$i.sh"
echo

# Copy scripts
cp job.sh job$i.sh
cp submit.sh submit$i.sh

# Replace clasdis file prefix and gemc gcard depending on if the lund file has positive or negative target polarization
if ((!$CLASDIS_GEN_PM || $i<=$NITERATIONS_HALF)); then #NOTE: ASSUME THAT POSITIVE POLARIZATIONS ARE FIRST THEN NEGATIVE.
    sed -i "s;out_tp_CLASDIS_POL_;${CLASDIS_PREFIX}${CLASDIS_POL}_idx_;g" job$i.sh
else
    sed -i "s;out_tp_CLASDIS_POL_;${CLASDIS_PREFIX}-${CLASDIS_POL}_idx_;g" job$i.sh
fi

# Replace the other variables
sed -i "s;MCINDEX=0;MCINDEX=$i;g" job$i.sh
sed -i "s;NEVENTS=100;NEVENTS=$NEVENTS;g" job$i.sh
sed -i "s;job.sh;job$i.sh;g" submit$i.sh

# Submit job
sbatch submit$i.sh
((i++))
done
