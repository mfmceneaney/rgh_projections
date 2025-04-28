#!/bin/bash

#SBATCH --job-name=rgh_clasdis
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=4000
#SBATCH --gres=disk:1000
#SBATCH --time=24:00:00
#SBATCH --mail-user=%u@jlab.org

export OUTDIR=$RGH_PROJECTIONS_VOL_DIR/jobs/rgh_simulation/mc_rgh_22GeV/lund
export CLASDIS_TRIG_HALF=`echo "$CLASDIS_TRIG/2" | bc`

# Create output directory
mkdir -p $OUTDIR
cd $OUTDIR

# Single target polarization sign
if ((!$CLASDIS_GEN_PM)); then

    # Run clasdis event generation 
    nohup clasdis --zpos -4.5 --zwidth 5.0 --targ $CLASDIS_TARG --nont --nmax $CLASDIS_NMAX --parj21 0.6 --beam $BEAM_ENERGY_RGH_22GeV --raster 1.8 --trig $CLASDIS_TRIG --pol $CLASDIS_POL --path ${CLASDIS_PREFIX}

    # Move files to numbered prefix names for ease of use
    i=1
    for file in *.dat
    do
        echo $file
        export NEWFILENAME=`echo $file | sed "s;${CLASDIS_PREFIX}clasdis;${CLASDIS_PREFIX}_idx_${i}clasdis;g"`
        echo NEWFILENAME $NEWFILENAME
        mv $file $NEWFILENAME
        ((i++))
    done

# Positive and negative target polarization split
else

    # Run clasdis event generation for both positive and negative polarization
    nohup clasdis --zpos -4.5 --zwidth 5.0 --targ $CLASDIS_TARG --nont --nmax $CLASDIS_NMAX --parj21 0.6 --beam $BEAM_ENERGY_RGH_22GeV --raster 1.8 --trig $CLASDIS_TRIG_HALF --pol $CLASDIS_POL --path ${CLASDIS_PREFIX}${CLASDIS_POL}_
    nohup clasdis --zpos -4.5 --zwidth 5.0 --targ $CLASDIS_TARG --nont --nmax $CLASDIS_NMAX --parj21 0.6 --beam $BEAM_ENERGY_RGH_22GeV --raster 1.8 --trig $CLASDIS_TRIG_HALF --pol -$CLASDIS_POL --path ${CLASDIS_PREFIX}-${CLASDIS_POL}_

    # Move files to numbered prefix names for ease of use
    i=1

    # Loop positive polarizations
    for file in ${CLASDIS_PREFIX}${CLASDIS_POL}_*.dat
    do
        echo $file
        export NEWFILENAME=`echo $file | sed "s;${CLASDIS_PREFIX}${CLASDIS_POL}_clasdis;${CLASDIS_PREFIX}${CLASDIS_POL}_idx_${i}_clasdis;g"`
        echo NEWFILENAME $NEWFILENAME
        mv $file $NEWFILENAME
        ((i++))
    done

    # Then negative polarizations
    for file in ${CLASDIS_PREFIX}-${CLASDIS_POL}_*.dat
    do
        echo $file
        export NEWFILENAME=`echo $file | sed "s;${CLASDIS_PREFIX}-${CLASDIS_POL}_clasdis;${CLASDIS_PREFIX}-${CLASDIS_POL}_idx_${i}_clasdis;g"`
        echo NEWFILENAME $NEWFILENAME
        mv $file $NEWFILENAME
        ((i++))
    done
fi
