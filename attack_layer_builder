import json  # Import the json module
import tkinter as tk
from tkinter import filedialog

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

# Provided JSON structure
base_structure = {
    "name": "Custom ATT&CK Layer",
    "versions": {
        "attack": "11", # Target version of MITRE ATT&CK - Update if using a different version
        "navigator": "4.8.0",
        "layer": "4.4"
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

# Prompt the user for technique IDs
technique_ids_input = input("Enter technique IDs separated by commas: ").split(',')

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
root = tk.Tk()
root.withdraw()  # Hide the main tkinter window

# Open "Save As" dialog with .json as the default extension
file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])

# If a file location is selected, save the data
if file_path:
    with open(file_path, 'w') as file:
        file.write(json_result)

input("Press any key to continue...")
