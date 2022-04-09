"""
How to Use
----------
Place jsonl files into the input folder
Run the script

Result: For each jsonl file in the input directory the total number of characters in all
    message objects is printed
"""

import json
import os


def iterate_over_jsonl_file(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield json.loads(line)


def count_file_character(file_path):
    character_count = 0
    for message_object in iterate_over_jsonl_file(file_path):
        character_count += len(message_object["full_text"])
    print(str(character_count) + "\n")


def count(directory):
    jsonl_input_files = [
        file_name
        for file_name in os.listdir(f"dataset_analysis/{directory}")
        if file_name.endswith(".jsonl")
    ]
    for jsonl_file in jsonl_input_files:
        print(f"Character count for {jsonl_file}:")
        count_file_character(f"dataset_analysis/{directory}/{jsonl_file}")


if __name__ == "__main__":
    count("input")
