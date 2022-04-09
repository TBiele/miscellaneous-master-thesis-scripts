"""
How to Use
----------
Put all jsonl files of messages that should be included in the data set into input/
If there are any files inside output/, remove them
Set TRAIN_RATIO and DEV_RATIO to the ratios of messages that should be assigned to the
    train and dev set, respectively. The remainder will be assigned to the test set.
Run script

Result: Files train.jsonl, dev.jsonl and test.jsonl in output/
"""

import json
import os
import random

if __name__ == "__main__":
    TRAIN_RATIO = 0.7
    DEV_RATIO = 0.1

    if not os.path.exists("training_data/output"):
        os.mkdir("training_data/output")
    # Check if there are already files inside output which would be modified
    jsonl_output_files = [
        file_name
        for file_name in os.listdir("training_data/output")
        if file_name.endswith(".jsonl")
    ]
    if len(jsonl_output_files) > 0:
        print(
            "Error: There are already files in the output directory which have to be "
            "removed before a new training data set can be created."
        )
        raise SystemExit(0)

    jsonl_input_files = [
        file_name
        for file_name in os.listdir("training_data/input")
        if file_name.endswith(".jsonl")
    ]
    for jsonl_input_file in jsonl_input_files:
        with open("training_data/input/" + jsonl_input_file, "r") as input_file:
            with open("training_data/output/train.jsonl", "a") as file_train:
                with open("training_data/output/dev.jsonl", "a") as file_dev:
                    with open("training_data/output/test.jsonl", "a") as file_test:
                        for line in input_file:
                            line_object = json.loads(line)
                            random_zero_to_one = random.random()
                            if random_zero_to_one < TRAIN_RATIO:
                                file_train.write(
                                    json.dumps(line_object, ensure_ascii=False) + "\n"
                                )
                            elif (
                                random_zero_to_one > TRAIN_RATIO
                                and random_zero_to_one < TRAIN_RATIO + DEV_RATIO
                            ):
                                file_dev.write(
                                    json.dumps(line_object, ensure_ascii=False) + "\n"
                                )
                            else:
                                file_test.write(
                                    json.dumps(line_object, ensure_ascii=False) + "\n"
                                )
