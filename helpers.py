import csv
import json

def loadParams(file_path, row_index):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for current_index, row in enumerate(reader):
            if current_index == row_index:
                return dict(row)
    return None  # Return None or raise an error if the index is not found