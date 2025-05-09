#!/bin/bash                                                  

export INFILE='/path/test.hipo'
export OUTDIR="$RGH_PROJECTIONS_VOL_DIR/jobs/c12analysis/mc_rgh_22GeV"
export name=`echo $INFILE | xargs -n 1 basename`
mkdir -p $OUTDIR
cd $OUTDIR

# Check if this file has a target polarization sign
export TPOL_IS_M1=`echo $name | grep "${CLASDIS_PREFIX}-${CLASDIS_POL}_"`
if (($CLASDIS_GEN_PM)) && [ -n $TPOL_IS_M1 ]; then
    export TSPIN_SIGN=-1
else
    export TSPIN_SIGN=1
fi

$C12ANALYSIS/bin/run.sh $INFILE -ch 211 -be $BEAM_ENERGY_RGH_22GeV -tpid $TPID_RGH_22GeV -tspin $TSPIN_RGH -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -ak -f -out $OUTDIR/skim_pi_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch -211 -be $BEAM_ENERGY_RGH_22GeV -tpid $TPID_RGH_22GeV -tspin $TSPIN_RGH -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -ak -f -out $OUTDIR/skim_pim_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 211,-211 -be $BEAM_ENERGY_RGH_22GeV -tpid $TPID_RGH_22GeV -tspin $TSPIN_RGH -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -ak -f -out $OUTDIR/skim_pipim_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 321 -be $BEAM_ENERGY_RGH_22GeV -tpid $TPID_RGH_22GeV -tspin $TSPIN_RGH -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -ak -f -out $OUTDIR/skim_k_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch -321 -be $BEAM_ENERGY_RGH_22GeV -tpid $TPID_RGH_22GeV -tspin $TSPIN_RGH -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -ak -f -out $OUTDIR/skim_km_tp_${TSPIN_SIGN}_${name}.root
$C12ANALYSIS/bin/run.sh $INFILE -ch 321,-321 -be $BEAM_ENERGY_RGH_22GeV -tpid $TPID_RGH_22GeV -tspin $TSPIN_RGH -tspin_sign $TSPIN_SIGN -rn -en -ang -vtx -ik -ma -ak -f -out $OUTDIR/skim_kkm_tp_${TSPIN_SIGN}_${name}.root

echo DONE
