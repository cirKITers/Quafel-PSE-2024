#!/bin/bash

# Check if an email argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <email>"
    exit 1
fi

EMAIL="$1"

# Paste email in the JSON file
sed -i "s/\"pk\": \"[^\"]*\"/\"pk\": \"${EMAIL}\"/" ./quafelweb/simulation_data/fixtures/login_data.json
if [ $? -ne 0 ]; then
    echo "Error: Failed to paste email in login_data.json"
    exit 1
fi
echo "Updated login_data.json with email: ${EMAIL}"

# Copy the JSON file to the container
docker cp ./quafelweb/simulation_data/fixtures/login_data.json quafel-pse-2024-webapp.server-1:/app/quafelweb/simulation_data/fixtures/
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy login_data.json to the container"
    exit 1
fi
echo "Copied login_data.json to the container"

# Load data inside the container
docker exec -it quafel-pse-2024-webapp.server-1 sh -c "poetry run python manage.py loaddata login_data"
if [ $? -ne 0 ]; then
    echo "Error: Failed to load data in the container"
    exit 1
fi
echo "Data loaded successfully in the container"
