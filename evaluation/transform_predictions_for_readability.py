"""
How to Use
----------
Create data set directory inside input
Place files into directory
- misinfo.json
- bm25-predictions.jsonl, bertscore-predictions.jsonl
Change DATA_SET_NAME to the data set directory name
Run script

Result: More readable files showing the prediction results for each message are created
    and saved in the output directory. Hint: For better readability, copy a line into
    an online json formatter.
"""

import json
import os

DATA_SET_NAME = MY_DATA_SET_NAME


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
        return json.loads(data)


def get_misinfo_title(misinfo_json, misinfo_id):
    return misinfo_json[misinfo_id]["title"]


def transform_predictions_file(file_name):
    if not os.path.exists("evaluation/output"):
        os.mkdir("evaluation/output")
    # Check if there are already files inside output which would be modified
    jsonl_output_files = [
        output_file_name
        for output_file_name in os.listdir("evaluation/output")
        if output_file_name.startswith(file_name)
        and output_file_name.endswith(".jsonl")
    ]
    if len(jsonl_output_files) > 0:
        print(
            "Error: There are already files in the output directory which have to be "
            "removed before a new training data set can be created."
        )
        raise SystemExit(0)

    misinfo_json = load_json("evaluation/input/" + DATA_SET_NAME + "/misinfo.json")
    output_object = {}
    with open("evaluation/input/" + DATA_SET_NAME + "/" + file_name, "r") as input_file:
        output_file_name = file_name.split(".jsonl")[0] + "-readable.jsonl"
        for line in input_file:
            line_object = json.loads(line)
            message_id = line_object["tweet_id"]
            if message_id not in output_object:
                output_object[message_id] = {
                    "labels": [],
                    "preds": [],
                    "text": line_object["text"],
                }
            if "labels" not in output_object[message_id]:
                output_object[message_id]["labels"] = []
            if line_object["m_label"] == 1:
                misinfo_title = get_misinfo_title(misinfo_json, line_object["m_id"])
                output_object[message_id]["labels"].append(misinfo_title[0])
            if line_object["m_pred"] == 1:
                misinfo_title = get_misinfo_title(misinfo_json, line_object["m_id"])
                output_object[message_id]["preds"].append(misinfo_title[0])
    with open("evaluation/output/" + output_file_name, "a") as output_file:
        for message_id in output_object.keys():
            new_line_object = output_object[message_id]
            new_line_object["id"] = message_id
            output_file.write(
                json.dumps(output_object[message_id], ensure_ascii=False) + "\n"
            )


if __name__ == "__main__":
    transform_predictions_file("bm25-predictions.jsonl")
    transform_predictions_file("bertscore-predictions.jsonl")
