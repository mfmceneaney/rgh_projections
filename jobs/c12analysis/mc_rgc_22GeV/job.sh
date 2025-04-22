#!/bin/bash                                                  

export INFILE='/path/test.hipo'
export OUTDIR="$RGH_PROJECTIONS_VOL_DIR/jobs/c12analysis/mc_rgc_22GeV"
export name=`echo $INFILE | xargs -n 1 basename`
mkdir -p $OUTDIR
cd $OUTDIR

$C12ANALYSIS/bin/run.sh $INFILE -ch 211 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_pi_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch -211 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_pim_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 211,-211 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_pipim_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 321 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_k_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch -321 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_km_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 321,-321 -be $BEAM_ENERGY_RGC_22GeV -tpid $TPID_RGC_22GeV -rn -en -ang -vtx -ik -ma -f -out $OUTDIR/skim_kkm_${name}.root

echo DONE
