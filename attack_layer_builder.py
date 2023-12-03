"""
MITRE ATT&CK Navigator Layer Generator

This script generates a JSON file for use with the MITRE ATT&CK Navigator.
It allows users to input ATT&CK technique IDs either via a CSV file or manually,
and sets a score for each technique. The output is a JSON file representing
a layer for the ATT&CK Navigator.

Usage:
1. Run the script.
2. Choose to input technique IDs via CSV file or manually.
3. Input the desired score for the techniques.
4. Save the generated JSON to a file.
"""

# Default value for MITRE ATT&CK Navigator version
DEFAULT_ATTACK_VERSION = "14"

# Imports

import json  # Import the json module
import tkinter as tk
from tkinter import filedialog
import csv  # Import csv for handling CSV files
import re  # Import the regular expressions module
import logging

# Set up logging for tracking actions and errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate the JSON structure for the techniques
def generate_json_structure(technique_ids, score):
    techniques = []
    for tid in technique_ids:
        technique = {
            "techniqueID": tid.upper(),  # Convert to uppercase
            "color": "",
            "score": score,
            "comment": "",
            "enabled": True,
            "metadata": [],
            "links": [],
            "showSubtechniques": False
        }
        techniques.append(technique)

    return techniques
    
# Function to find and import technique IDs from a CSV file
def find_and_import_technique_ids(csv_path):
    technique_id_pattern = re.compile(r"[Tt]1\d{3}(\.0\d{2})?$")
    techniques = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for cell in row:
                if technique_id_pattern.match(cell):
                    techniques.append(cell)
    return techniques
        
# Function to check if a technique ID is valid
def is_valid_technique_id(tid):
    """Check if the technique ID follows the pattern 'T1###' or 'T1###.0##'"""
    return re.match(r"T1\d{3}(\.0\d{2})?$", tid) is not None


# Function to prompt the user for technique IDs and validate them
def get_valid_technique_ids_from_user():
    """Prompt the user for technique IDs and validate them"""
    while True:
        user_input = input("Enter technique IDs separated by commas: ")
        technique_ids = [tid.strip() for tid in user_input.split(',')]

        if all(is_valid_technique_id(tid) for tid in technique_ids):
            return technique_ids
        else:
            print("One or more technique IDs are invalid. Please enter valid MITRE ATT&CK technique IDs (e.g., T1027).")

# Main script execution starts here
# Prompt for MITRE ATT&CK Navigator version with a default value
attack_version_input = input(f"What version of MITRE ATT&CK Navigator are you using? (Enter a number between 4 and 14 or press Enter for default v{DEFAULT_ATTACK_VERSION}): ")
if not attack_version_input.strip():
    attack_version_input = DEFAULT_ATTACK_VERSION
else:
    try:
        attack_version_input = int(attack_version_input)
        if not 4 <= attack_version_input <= 14:
            print(f"Invalid input. Using default version {DEFAULT_ATTACK_VERSION}.")
            attack_version_input = DEFAULT_ATTACK_VERSION
    except ValueError:
        print(f"Invalid input. Using default version {DEFAULT_ATTACK_VERSION}.")
        attack_version_input = DEFAULT_ATTACK_VERSION

# Ensure the version is a string for JSON structure
attack_version_input = str(attack_version_input)

# Provided JSON structure with dynamic MITRE ATT&CK version
base_structure = {
    "name": "Custom ATT&CK Layer",
    "versions": {
        "attack": str(attack_version_input),  # Dynamic version based on user input
        "navigator": "4.9.1",
        "layer": "4.5"
    },
    "domain": "enterprise-attack",
    "description": "Custom Layer for User Provided TTPs",
    "layout": {
        "layout": "side",
        "aggregateFunction": "average",
        "showID": False,
        "showName": True,
        "showAggregateScores": False,
        "countUnscored": False
    },
    "hideDisabled": True,
    "techniques": []  # Empty techniques list, to be filled later
}

# Tkinter setup for file dialog
root = tk.Tk()
root.withdraw()

# User input for CSV file selection or  technique IDs
while True:
    input_method = input("Enter '1' to select a CSV file or '2' to input technique IDs manually: ")

    if input_method == '1':
        # GUI to select CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            technique_ids_input = find_and_import_technique_ids(file_path)
            if technique_ids_input:
                break
            else:
                print("No valid technique IDs found in the file. Please try again.")
        else:
            print("No file selected. Please try again.")
    elif input_method == '2':
        technique_ids_input = get_valid_technique_ids_from_user()
        break
    else:
        print("Invalid input. Please enter '1' or '2'.")

# Prompt for score and ensure it's a valid integer
try:
    score_input = int(input("Enter a score for the techniques: "))
except ValueError:
    print("Invalid score input. Defaulting to 1.")
    score_input = 1  # Default score if input is not a valid integer

# Process and update the base structure with the techniques
base_structure["techniques"] = generate_json_structure(technique_ids_input, score_input)

# Convert the Python dictionary to a JSON-formatted string and print it
json_result = json.dumps(base_structure, indent=4)  # Makes the output more readable
print(json_result)

# GUI "Save As" dialog to save the result to a .json file
file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])

# Save the data if a file location is selected
if file_path:
    try:
        with open(file_path, 'w') as file:
            file.write(json_result)
            logging.info(f"JSON file saved successfully to {file_path}.")
    except Exception as e:
        logging.error(f"Error writing JSON file: {e}")

# Clean up Tkinter window
root.destroy()

# Final user prompt to conclude the script execution
input("Press any key to continue...")
