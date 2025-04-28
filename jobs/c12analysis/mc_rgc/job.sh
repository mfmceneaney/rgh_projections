#!/bin/bash                                                  

export INFILE='/path/test.hipo'
export OUTDIR="$RGH_PROJECTIONS_VOL_DIR/jobs/c12analysis/mc_rgc"
export name=`echo $INFILE | xargs -n 1 basename`
mkdir -p $OUTDIR
cd $OUTDIR

export TSPIN_SIGN=1

$C12ANALYSIS/bin/run.sh $INFILE -ch 211 -be $BEAM_ENERGY_RGC -tpid $TPID_RGC -tspin $TSPIN_RGC -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_pi_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch -211 -be $BEAM_ENERGY_RGC -tpid $TPID_RGC -tspin $TSPIN_RGC -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_pim_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 211,-211 -be $BEAM_ENERGY_RGC -tpid $TPID_RGC -tspin $TSPIN_RGC -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_pipim_tp_${TSPIN_SIGN}_${name}.root

echo DONE
