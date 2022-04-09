"""
How to Use
----------
Place jsonl files into the input folder
Run the script

Result: For each jsonl file in the input directory the counts for all labels in the
    message objects are printed
"""

import json
import os


def iterate_over_jsonl_file(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield json.loads(line)


def count():
    jsonl_input_files = [
        file_name
        for file_name in os.listdir("dataset_analysis/input")
        if file_name.endswith(".jsonl")
    ]
    for jsonl_file in jsonl_input_files:
        label_counts = {}
        file_path = os.path.join("dataset_analysis/input", jsonl_file)
        for message_object in iterate_over_jsonl_file(file_path):
            for label in message_object["misinfo"].keys():
                if label in label_counts:
                    label_counts[label] += 1
                else:
                    label_counts[label] = 1
        print(f"Label counts for {jsonl_file}:")
        print(sorted(label_counts.items(), key=lambda item: int(item[0])))
        print("\n")


if __name__ == "__main__":
    count()
