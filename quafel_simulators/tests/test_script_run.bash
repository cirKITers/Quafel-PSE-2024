#!/bin/bash

# These are replaced by the script-builder
CONFIGURATION=""  # yml configuration file for quafel/kedro
OUTPUT_LOCATION=""  # the output folder the data will be saved to

cd Quafel

# write the configuration file
echo "$CONFIGURATION" > conf/base/parameters/data_generation.yml

# run the quafel pipeline
poetry run kedro run --pipeline prepare
PREPARE_STATUS=$?
if [ $PREPARE_STATUS -ne 0 ]; then
  exit 1
fi

poetry run kedro run --pipeline measure
MEASURE_STATUS=$?
if [ $MEASURE_STATUS -ne 0 ]; then
  exit 1
fi

poetry run kedro run --pipeline combine
COMBINE_STATUS=$?
if [ $COMBINE_STATUS -ne 0 ]; then
  exit 1
fi

# copy the output to the output folder
# TODO

exit 0
