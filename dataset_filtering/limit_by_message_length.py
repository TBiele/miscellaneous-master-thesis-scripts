"""
How to Use
----------
Put jsonl files into input directory
Run script

Result: Filtered jsonl files containing only messages of length below max_length in
    output directory
"""

import json
import os


def create_limited_files(max_length):
    input_dir = "dataset_filtering/input"
    json_files = [f for f in os.listdir(input_dir) if f.endswith(".jsonl")]
    for file_name in json_files:
        if not os.path.exists("dataset_filtering/output"):
            os.makedirs("dataset_filtering/output")
        file_name_prefix = file_name.split(".jsonl")[0]
        with open(
            f"dataset_filtering/output/{file_name_prefix}_limited.jsonl", "w"
        ) as f:
            for line in open(f"{input_dir}/{file_name}", "r"):
                message = json.loads(line)
                if len(message["full_text"]) > max_length:
                    continue
                f.write(json.dumps(message, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    create_limited_files(200)
