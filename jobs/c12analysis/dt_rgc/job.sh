#!/bin/bash                                                  

export INFILE='/path/test.hipo'
export OUTDIR="$RGH_PROJECTIONS_VOL_DIR/jobs/c12analysis/dt_rgc"
export name=`echo $INFILE | xargs -n 1 basename`
mkdir -p $OUTDIR
cd $OUTDIR

$C12ANALYSIS/bin/run.sh $INFILE -ch 211 -be $BEAM_ENERGY_RGC -tpid $TPID_RGC -tspin $TSPIN_RGC -rn -en -ang -vtx -ik -f -out $OUTDIR/skim_pi_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch -211 -be $BEAM_ENERGY_RGC -tpid $TPID_RGC -tspin $TSPIN_RGC -rn -en -ang -vtx -ik -f -out $OUTDIR/skim_pim_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 211,-211 -be $BEAM_ENERGY_RGC -tpid $TPID_RGC -tspin $TSPIN_RGC -rn -en -ang -vtx -ik -f -out $OUTDIR/skim_pipim_${name}.root

echo DONE
