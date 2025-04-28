#!/bin/bash

# Set paths in yaml files for saga
for file in $RGH_PROJECTIONS_HOME/jobs/*/*/*.yaml; do
    sed -i.bak "s;/RGH_PROJECTIONS_HOME;$RGH_PROJECTIONS_HOME;g" $file
    sed -i.bak "s;/RGH_PROJECTIONS_VOL_DIR;$RGH_PROJECTIONS_VOL_DIR;g" $file
    sed -i.bak "s;/RGC_TPOL_CSV;$RGC_TPOL_CSV;g" $file
done
