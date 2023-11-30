import json  # Import the json module
import tkinter as tk
from tkinter import filedialog
import csv  # Import csv for handling CSV files


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
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader]  # Assumes Technique IDs are in the first column

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
    technique_ids_input = input("Enter technique IDs separated by commas: ").split(',')
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
    with open(file_path, 'w') as file:
        file.write(json_result)

root.destroy()  # Properly close the Tkinter window

input("Press any key to continue...")
