#!/bin/bash

# Parameters to be overridden by the script_builder
SIMULATION_ID=""
CONFIGURATION=""
OUTPUT_LOCATION=""

# Function definitions
copy_quafel() {
  cp -r "$HOME/Quafel" "$HOME/$SIMULATION_ID" &&
  cd "$HOME/Quafel" || return 1
}

write_configuration() {
  echo "$CONFIGURATION" > "conf/base/parameters/data_generation.yml"
}

# Change sbatch parameters as needed
run_kedro_pipelines() {
  poetry env use ~/.pyenv/versions/3.9.19/bin/python3 &&
  poetry run bash -c "cd $HOME/$SIMULATION_ID && kedro run --pipeline prepare" &&
  JOB_ID=$(poetry run bash -c 'cd $HOME/$SIMULATION_ID && sbatch --job-name=quafel --ntasks=30 --time=40:00:00 --partition=multiple --mem=80000MB --wrap="poetry run kedro run --pipeline measure --runner quafel.runner.Parallel"' | awk '{print $4}') &&
  echo "Submitted job with ID $JOB_ID" &&
  while squeue -j "$JOB_ID" > /dev/null 2>&1; do
    sleep 30
  done &&
  poetry run bash -c "cd $HOME/$SIMULATION_ID && kedro run --pipeline combine"
}

copy_output() {
  sshpass -p "password" scp -o StrictHostKeyChecking=no -r "$HOME/$SIMULATION_ID/data/07_evaluations_combined/evaluations_combined.csv" "user@output.server:$OUTPUT_LOCATION/$SIMULATION_ID"
}

cleanup() {
  rm -rf "$HOME/$SIMULATION_ID"
}

# Main execution flow
if copy_quafel && write_configuration && run_kedro_pipelines && copy_output; then
  cleanup
  exit 0
else
  echo "An error occurred."
  cleanup
  exit 1
fi
