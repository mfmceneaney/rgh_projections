#!/bin/bash                                                  

export INFILE='/path/test.hipo'
export OUTDIR="$RGH_PROJECTIONS_VOL_DIR/jobs/c12analysis/dt_rga"
export name=`echo $INFILE | xargs -n 1 basename`
mkdir -p $OUTDIR
cd $OUTDIR

$C12ANALYSIS/bin/run.sh $INFILE -ch 211 -be $BEAM_ENERGY_RGA -tpid $TPID_RGA -rn -en -ang -vtx -ik -f -out $OUTDIR/skim_pi_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch -211 -be $BEAM_ENERGY_RGA -tpid $TPID_RGA -rn -en -ang -vtx -ik -f -out $OUTDIR/skim_pim_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 211,-211 -be $BEAM_ENERGY_RGA -tpid $TPID_RGA -rn -en -ang -vtx -ik -f -out $OUTDIR/skim_pipim_${name}.root

echo DONE
