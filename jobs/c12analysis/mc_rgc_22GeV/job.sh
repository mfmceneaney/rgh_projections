#!/bin/bash                                                  

export INFILE='/path/test.hipo'
export OUTDIR="$RGH_PROJECTIONS_VOL_DIR/jobs/c12analysis/mc_rgc_22GeV"
export name=`echo $INFILE | xargs -n 1 basename`
mkdir -p $OUTDIR
cd $OUTDIR

export TSPIN_SIGN=1

$C12ANALYSIS/bin/run.sh $INFILE -ch 211 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -tspin $TSPIN_RGC -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_pi_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch -211 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -tspin $TSPIN_RGC -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_pim_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 211,-211 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -tspin $TSPIN_RGC -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_pipim_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 321 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -tspin $TSPIN_RGC -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_k_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch -321 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -tspin $TSPIN_RGC -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_km_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 321,-321 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -tspin $TSPIN_RGC -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_kkm_tp_${TSPIN_SIGN}_${name}.root

echo DONE
