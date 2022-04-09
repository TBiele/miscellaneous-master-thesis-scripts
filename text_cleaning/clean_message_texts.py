"""
How to Use
----------
Place jsonl files into the input folder
Run the script

Result: Jsonl files with cleaned text (urls and line break characters removed) are
    put into the output folder
"""

import json
import os
import re


def iterate_over_jsonl_file(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield json.loads(line)


def clean_message_texts():
    jsonl_input_files = [
        file_name
        for file_name in os.listdir("text_cleaning/input")
        if file_name.endswith(".jsonl")
    ]
    for jsonl_file in jsonl_input_files:
        file_path = os.path.join("text_cleaning/input", jsonl_file)
        with open(f"text_cleaning/output/{jsonl_file}", "w") as f:
            for message_object in iterate_over_jsonl_file(file_path):
                # Remove urls from message text
                message_object["full_text"] = re.sub(
                    r"http\S+", "", message_object["full_text"]
                )
                message_object["full_text"] = message_object["full_text"].replace(
                    "\n\n", " "
                )
                message_object["full_text"] = message_object["full_text"].replace(
                    "\n", " "
                )
                if (
                    message_object["full_text"] != ""
                    and not message_object["full_text"].isspace()
                ):
                    f.write(json.dumps(message_object, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    clean_message_texts()
