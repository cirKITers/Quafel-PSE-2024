#!/sandbox/bash

# This script pulls the output from the remote server to the local machine
# The pull_output script is run on the local machine
# The local machine has to support bash, ssh, sshpass and scp

REMOTE_HOST=""
REMOTE_PORT=""
REMOTE_USERNAME=""
REMOTE_PASSWORD=""

SIMULATION_ID=""
OUTPUT_LOCATION=""
INPUT_LOCATION="outputs"


echo "Starting to pull output from the remote server..."

# Create the input directory if it does not exist
if [ ! -d "$INPUT_LOCATION" ]; then
    mkdir -p "$INPUT_LOCATION"
    echo "Created input directory at $INPUT_LOCATION."
fi

# Pull the output from the remote server to the local machine
if sshpass -p "$REMOTE_PASSWORD" scp -r -P "$REMOTE_PORT" "$REMOTE_USERNAME@$REMOTE_HOST:$OUTPUT_LOCATION/$SIMULATION_ID" "$INPUT_LOCATION/$SIMULATION_ID"; then
    echo "Successfully pulled output to $INPUT_LOCATION/$SIMULATION_ID."
else
    echo "Failed to pull output from the remote server."
    exit 1
fi

# Delete the output from the remote server
if sshpass -p "$REMOTE_PASSWORD" ssh -p "$REMOTE_PORT" "$REMOTE_USERNAME@$REMOTE_HOST" "rm -rf $OUTPUT_LOCATION/$SIMULATION_ID"; then
    echo "Successfully deleted remote output."
else
    echo "Failed to delete remote output."
    exit 1
fi

echo "Operation completed successfully."
exit 0
