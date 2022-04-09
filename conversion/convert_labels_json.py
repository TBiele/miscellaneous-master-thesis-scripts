"""
How to Use
----------
Place into input directory:
    1) message_index.json which maps message hashes to message content
    2) Json file(s) from the Web labeling interface (MessageMisconception-DATE.json).
        Each label object contains a message hash (key=MESSAGE_HASH_KEY) and a
        misconception label for this message (key=MISCONCEPTION_LABEL_KEY).
        Each message hash needs to be contained in message_index.json.
Run script

Result: Jsonl file using the data format from the CoVaxLies paper is created in output
    directory. It contains one json line for each message which includes all
    misconception labels.
"""

import json
import os


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
        return json.loads(data)


if __name__ == "__main__":
    MESSAGE_HASH_KEY = "message"
    MISCONCEPTION_LABEL_KEY = "misconception"
    MERGE_STRATEGY = "combine"

    try:
        message_index = load_json("conversion/input/message_index.json")
    except FileNotFoundError:
        print(
            "Error: Please create a file message_index.json which maps message hashes "
            "to message content and place it inside the directory conversion/input."
        )
        raise SystemExit(0)
    json_input_files = [
        file_name
        for file_name in os.listdir("conversion/input")
        if file_name.startswith("MessageMisconception")
    ]
    # Convert each json input file to a jsonl file
    for json_input_file in json_input_files:
        json_file_label_objects = load_json("conversion/input/" + json_input_file)
        output_file_name = json_input_file.split(".json")[0] + ".jsonl"
        output_collection_object = {}
        for single_label_object in json_file_label_objects:
            message_hash = single_label_object[MESSAGE_HASH_KEY]
            if message_hash not in output_collection_object.keys():
                # First time a label for this message is encountered
                misconception_id = single_label_object[MISCONCEPTION_LABEL_KEY]
                output_collection_object[message_hash] = []
                if misconception_id != "":
                    output_collection_object[message_hash].append(misconception_id)
            else:
                # At least one label has already been added for this message
                if MERGE_STRATEGY == "combine":
                    misconception_id = single_label_object[MISCONCEPTION_LABEL_KEY]
                    if (
                        misconception_id not in output_collection_object[message_hash]
                        and misconception_id != ""
                    ):
                        output_collection_object[message_hash].append(misconception_id)
                else:
                    # If you do not want to simply combine all labels, you might have
                    # to take into account the user property
                    print("Error: Merge strategy", MERGE_STRATEGY, "is not implemented")
                    raise SystemExit(0)
        with open("conversion/output/" + output_file_name, "w") as output_file:
            for (
                message_hash,
                message_misconceptions,
            ) in output_collection_object.items():
                message_misconceptions_weinzierl_object = {
                    misconception: "agree" for misconception in message_misconceptions
                }
                message_object = {
                    "id": message_hash,
                    "misinfo": message_misconceptions_weinzierl_object,
                    "full_text": message_index[message_hash],
                }
                output_file.write(json.dumps(message_object, ensure_ascii=False) + "\n")
