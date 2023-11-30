import json  # Import the json module
import tkinter as tk
from tkinter import filedialog
import csv  # Import csv for handling CSV files
import re  # Import the regular expressions module
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_json_structure(technique_ids, score):
    techniques = []
    for tid in technique_ids:
        technique = {
            "techniqueID": tid,
            "color": "",
            "score": score,  # Use the input score here
            "comment": "",
            "enabled": True,
            "metadata": [],
            "links": [],
            "showSubtechniques": False
        }
        techniques.append(technique)

    return techniques
    
def get_technique_ids_from_csv(file_path):
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            technique_ids = [row[0] for row in reader]
            logging.info(f"Successfully read {len(technique_ids)} techniques from CSV file.")
            return technique_ids
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        exit()
        
def is_valid_technique_id(tid):
    """Check if the technique ID follows the pattern 'T####' or 'T####.0##'"""
    return re.match(r"T\d{4}(\.0\d{2})?$", tid) is not None

def get_valid_technique_ids_from_user():
    """Prompt the user for technique IDs and validate them"""
    while True:
        user_input = input("Enter technique IDs separated by commas: ")
        technique_ids = [tid.strip() for tid in user_input.split(',')]

        if all(is_valid_technique_id(tid) for tid in technique_ids):
            return technique_ids
        else:
            print("One or more technique IDs are invalid. Please enter valid MITRE ATT&CK technique IDs (e.g., T1027).")

# Prompt for ATT&CK Navigator version
while True:
    try:
        attack_version_input = int(input("What version of ATT&CK Navigator are you using? (Enter a number between 4 and 14): "))
        if 4 <= attack_version_input <= 14:
            break
        else:
            print("Please enter a number between 4 and 14.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Provided JSON structure with dynamic ATT&CK version
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

root = tk.Tk()
root.withdraw()  # Create a single Tkinter root instance and hide the main window

# User input for technique IDs or CSV file selection
input_method = input("Enter '1' to select a CSV file or '2' to input technique IDs manually: ")

if input_method == '1':
    # GUI to select CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        technique_ids_input = get_technique_ids_from_csv(file_path)
    else:
        print("No file selected, exiting.")
        exit()
elif input_method == '2':
    technique_ids_input = get_valid_technique_ids_from_user()
else:
    print("Invalid input, exiting.")
    exit()

# Prompt for score and ensure it's a valid integer
try:
    score_input = int(input("Enter a score for the techniques: "))
except ValueError:
    print("Invalid score input. Defaulting to 1.")
    score_input = 1  # Default score if input is not a valid integer

# Get the techniques and update the base structure with them
base_structure["techniques"] = generate_json_structure(technique_ids_input, score_input)

# Convert the Python dictionary to a JSON-formatted string
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

root.destroy()  # Properly close the Tkinter window

input("Press any key to continue...")
