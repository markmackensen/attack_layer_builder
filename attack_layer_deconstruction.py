import json
import csv
import tkinter as tk
from tkinter import filedialog

# Tkinter setup for file dialog
root = tk.Tk()
root.withdraw()

# File dialog to select the exported JSON file
file_path = filedialog.askopenfilename(title="Select the exported JSON file", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
if not file_path:
    print("No file selected. Exiting.")
    exit()

# Read and load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract techniques and their scores
ttps_scores = [(technique["techniqueID"], technique["score"]) for technique in data.get("techniques", []) if "score" in technique]

# Sort the TTPs based on score in descending order
sorted_ttps_scores = sorted(ttps_scores, key=lambda x: x[1], reverse=True)

# File dialog to save the CSV file
csv_file_path = filedialog.asksaveasfilename(title="Save the CSV file", defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
if not csv_file_path:
    print("No save file selected. Exiting.")
    exit()

# Write the sorted TTPs and scores to a CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Technique ID", "Score"])  # Header
    writer.writerows(sorted_ttps_scores)

print(f"CSV file successfully saved to {csv_file_path}")

# Clean up Tkinter window
root.destroy()
