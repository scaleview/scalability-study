import json
import csv
import os
from decimal import Decimal
import sys


def get_highest_dimension(dimension_descriptors):
    highest_dimension = None

    if "super-linear" in dimension_descriptors:
        highest_dimension = "super-linear"
    elif "quasi-linear" in dimension_descriptors:
        highest_dimension = "super-linear"
    elif "linear" in dimension_descriptors:
        highest_dimension = "linear"
    elif "supra-linear" in dimension_descriptors:
        highest_dimension = "supra-linear"
    elif "bursty" in dimension_descriptors:
        highest_dimension = "bursty"

    return highest_dimension


def process_json(json_file, dependency_type):
    counts = {'total': 0, 'super-linear': 0,
              'linear': 0, 'supra-linear': 0, 'bursty': 0}

    with open(json_file, 'r') as file:
        data = json.load(file)

    for entry in data:
        if entry['dependencyType'] == dependency_type:

            method_name = entry['methodName']
            line_number = entry['lineNumber']
            dimension_descriptors = entry['dimensionDescriptors']

            # Initialize highest dimension descriptor as None
            highest_dimension = get_highest_dimension(dimension_descriptors)
            if highest_dimension is None:
                print("WARNING: Dimension is None")
            if highest_dimension.lower() != 'bursty':
                counts['total'] += 1
                counts[highest_dimension] += 1
    return counts


def count_lines_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        line_count = sum(1 for row in reader)
    return line_count


def find_files(directory):
    # Get the directory containing the Python script
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Navigate to the directory one level above the script directory
    parent_directory = os.path.abspath(
        os.path.join(script_directory, os.pardir))

    # Construct the full path to the specified directory
    full_directory = os.path.join(
        parent_directory, 'evaluation-data/scaleview-outputs', directory)

    # Change directory to the specified directory
    os.chdir(full_directory)

    # Initialize variables to store file paths
    json_file = None
    csv_file = None

    files = os.listdir()

    # Search for sdeps.json and CSV files
    for file in files:
        if file == 'sdeps.json':
            json_file = file
            print(f"Found JSON file: {json_file}")
        elif file.endswith('.csv'):
            csv_file = file
            print(f"Found CSV file: {csv_file}")

    # Return file paths
    return json_file, csv_file


if __name__ == "__main__":
    directory_name = sys.argv[1]+'-32'
    json_file, csv_file = find_files(directory_name)

    # Count lines in CSV file
    csv_line_count = count_lines_csv(csv_file)
    # print(f"Total number of loops found in CSV file: {csv_line_count}")

    # Specify the dependency type to filter entries
    dependency_type = "Loop"

    # Process JSON and print details of entries with the specified dependency type
    print(f"Searching for entries with dependency type '{dependency_type}':")
    counts = process_json(json_file, dependency_type)
    print("\nResults Summary: " +
        f"Total number of loops found in CSV file: {csv_line_count}")
    print("=" * 80)
    print("{:<20} {:<20} {:<20}".format("Metric", "Count", "Percentage"))
    print("-" * 80)
    print("{:<20} {:<20} {:<20.1%}".format(
        "Total", counts['total'], counts['total'] / csv_line_count))
    print("{:<20} {:<20} {:<20.1%}".format("Super-linear",
        counts['super-linear'], counts['super-linear'] / counts['total']))
    print("{:<20} {:<20} {:<20.1%}".format(
        "Linear", counts['linear'], counts['linear'] / counts['total']))
    print("{:<20} {:<20} {:<20.1%}".format("Supra-linear",
        counts['supra-linear'], counts['supra-linear'] / counts['total']))
    print("=" * 80)
