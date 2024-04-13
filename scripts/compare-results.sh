#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <container_id_or_name>"
    exit 1
fi

# Extract argument
CONTAINER_ID_OR_NAME=$1
REPO_DIR=$(git rev-parse --show-toplevel)

# Define the directory path inside the container where the CSV file is located
WORKSPACE_DIRECTORY=/home/scaleview/scaleview-core/workspace

# Get the CSV file name from the container
CSV_FILE=$(docker exec "$CONTAINER_ID_OR_NAME" find /home/scaleview/scaleview-core/workspace -maxdepth 1 -name '*.csv')

# Check if exactly one CSV file was found
if [ $(echo "$CSV_FILE" | wc -l) -ne 1 ]; then
    echo "Error: Expected exactly one CSV file in the container directory $WORKSPACE_DIRECTORY, found $(echo "$CSV_FILE" | wc -l) files."
    exit 1
fi

# Determine the base name of the CSV file (without the extension)
BASE_CSV_FILENAME=$(basename "$CSV_FILE" .csv)


# Define the directory path
USER_RESULTS_DIR="$REPO_DIR/user-results/"

# Check if the directory exists
if [ ! -d "$USER_RESULTS_DIR" ]; then
    # If it doesn't exist, create it
    mkdir -p "$USER_RESULTS_DIR"
    echo "Directory '$USER_RESULTS_DIR' created."
else
    echo "Directory '$USER_RESULTS_DIR' already exists."
fi


cd  $USER_RESULTS_DIR

# Remove existing directory if it exists
if [ -d "$BASE_CSV_FILENAME-32" ]; then
    echo "Removing existing directory: $BASE_CSV_FILENAME-32"
    rm -rf "$BASE_CSV_FILENAME"
fi

# Create a directory with the same name as the CSV file (without the extension)
mkdir -p "$BASE_CSV_FILENAME-32"

USER_DIR=$BASE_CSV_FILENAME-32

# Determine the output JSON file name based on the CSV file name
SDEPS_JSON=sdeps.json

# Copy the CSV file from the container to the host
docker cp "$CONTAINER_ID_OR_NAME":"$CSV_FILE" "$USER_DIR/"

# Copy the JSON file from the container to the host
docker cp "$CONTAINER_ID_OR_NAME":"$WORKSPACE_DIRECTORY/$SDEPS_JSON" "$USER_DIR/"

# Check if the copy was successful
if [ "$?" -eq 0 ]; then
    echo "CSV and JSON files copied from container to host."
else
    echo "Failed to copy CSV and JSON files from container to host."
    exit 1
fi

#!/bin/bash
REPO_DIR=$(git rev-parse --show-toplevel)

# Output a dashed line for visual separation
echo
echo "--------------------------------------------------------------------------------------------------"
echo "Expected Output"

# Run the first Python script
python3 $REPO_DIR/scripts/analyze-to-compare.py $USER_DIR 'evaluation-data/scaleview-outputs'

# Output a dashed line for visual separation
echo
echo "--------------------------------------------------------------------------------------------------"
echo "Processing Your Results"
# Run the second Python script
python3 $REPO_DIR/scripts/analyze-to-compare.py $REPO_DIR/user-results/$USER_DIR 'user-results'
echo "--------------------------------------------------------------------------------------------------"
echo

cd $REPO_DIR



