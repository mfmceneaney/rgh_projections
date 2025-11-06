#!/bin/bash

# Set paths in yaml files for saga
for file in $RGH_PROJECTIONS_HOME/jobs/*/*/*.yaml; do
    sed -i.bak "s;/RGH_PROJECTIONS_HOME;$RGH_PROJECTIONS_HOME;g" $file
    sed -i.bak "s;/RGH_PROJECTIONS_VOL_DIR;$RGH_PROJECTIONS_VOL_DIR;g" $file
    sed -i.bak "s;/RGC_TPOL_CSV;$RGC_TPOL_CSV;g" $file
done

# Fix for now so that job output directly can be set by saga python libraries
for file in $RGH_PROJECTIONS_HOME/jobs/saga/*/submit.sh; do
    sed -i.bak "s;\$RGH_PROJECTIONS_HOME;$RGH_PROJECTIONS_HOME;g" $file
    sed -i.bak "s;/farm_out/%u;$RGH_PROJECTIONS_FARM_OUT;g" $file
done

# Create output directories
mkdir -p $RGH_PROJECTIONS_FARM_OUT
mkdir -p $RGH_PROJECTIONS_VOL_DIR
