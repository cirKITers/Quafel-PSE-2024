#!/bin/bash

# These are replaced by the script-builder
CONFIGURATION=""  # yml configuration file for quafel/kedro
OUTPUT_LOCATION=""  # the output user, host and folder the data will be saved to (used by scp)

# copy quafel to another location
# this location will be used for all inputs and outputs
# the location is deleted after the script is done
# the build of the actual quafel will be used for the script
scp -r ~/Quafel "$HOME/$OUTPUT_LOCATION"

cd Quafel

# write the configuration file
echo "$CONFIGURATION" > "$HOME/$OUTPUT_LOCATION/conf/base/parameters/data_generation.yml"

# run the quafel pipeline
poetry run bash -c "cd $HOME/$OUTPUT_LOCATION && kedro run --pipeline prepare"
PREPARE_STATUS=$?
if [ $PREPARE_STATUS -ne 0 ]; then
  exit 1
fi

poetry run bash -c "cd $HOME/$OUTPUT_LOCATION && kedro run --pipeline measure"  # TODO: parallel runner
MEASURE_STATUS=$?
if [ $MEASURE_STATUS -ne 0 ]; then
  exit 1
fi

poetry run bash -c "cd $HOME/$OUTPUT_LOCATION && kedro run --pipeline combine"
COMBINE_STATUS=$?
if [ $COMBINE_STATUS -ne 0 ]; then
  exit 1
fi

# copy the output to the output folder
sshpass -p "password" scp -o StrictHostKeyChecking=no -r "$HOME/$OUTPUT_LOCATION/data/07_evaluations_combined/evaluations_combined.csv" "user@server_side:~/$OUTPUT_LOCATION"
# TODO: remove the working directory


exit 0
