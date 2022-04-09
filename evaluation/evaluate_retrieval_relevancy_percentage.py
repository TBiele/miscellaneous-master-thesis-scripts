"""
How to Use
----------
Create data set directory inside input
Place files into directory (e. g. train.jsonl, dev.jsonl, test.jsonl)
Change DATA_SET_NAME to the data set directory name
Change INPUT_JSONL_FILES if necessary
Run script

Result: The percentage of relevant messages is printed (relevant meaning that the
    message contains at least one misinfo label).
"""

import json

DATA_SET_NAME = MY_DATA_SET_NAME
INPUT_JSONL_FILES = ["train.jsonl", "dev.jsonl", "test.jsonl"]


def iterate_over_jsonl_file(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield json.loads(line)


def calculate_relevancy_percentage():
    all_jsonl_files = [
        iterate_over_jsonl_file(f"evaluation/input/{DATA_SET_NAME}/{file_name}")
        for file_name in INPUT_JSONL_FILES
    ]
    all_messages_objects = [line for file in all_jsonl_files for line in file]

    total, relevant = 0, 0
    for message_object in all_messages_objects:
        total += 1
        if len(message_object["misinfo"]) == 0:
            relevant += 1
    return relevant / total if total > 0 else 0


if __name__ == "__main__":
    relevant_percentage = calculate_relevancy_percentage()
    print(f"Relevant percentage: {relevant_percentage}")
