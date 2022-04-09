"""
Obsolete

How to Use
----------
Put all jsonl files of messages that should be included in the data set into input/
If there are any files inside output/, remove them
Run script

Result: CSV file of labeled messages in output/
"""

import json
import nltk
import os
import pandas as pd


def get_labeled_messages_data_frame(
    input_file_name, misconception_ids_list, remove_stop_words=True
):
    df_labeled_messages = pd.DataFrame(columns=["content"] + misconception_ids_list)
    with open("training_data/input/" + input_file_name, "r") as input_file:
        for line_json in input_file:
            # Add message line to data frame
            line_object = json.loads(line_json)
            message_id = line_object["id"]
            message_content = line_object["full_text"]
            zeros = [0 for i in range(len(misconception_ids_list))]
            if remove_stop_words:
                # Remove stop words
                german_stop_words = nltk.corpus.stopwords.words("german")
                input_message_split = message_content.split()
                processed_message = " ".join(
                    [w for w in input_message_split if w not in german_stop_words]
                )
                df_labeled_messages.loc[message_id] = [processed_message] + list(zeros)
            else:
                df_labeled_messages.loc[message_id] = [message_content] + list(zeros)
            # Set labels
            for label_id in line_object["misinfo"].keys():
                if label_id not in misconception_ids_list:
                    print(
                        f"Skipping label {label_id} which is not in the list of label"
                        "ids"
                    )
                    continue
                df_labeled_messages.loc[message_id, label_id] = 1
        return df_labeled_messages


if __name__ == "__main__":
    MISCONCEPTION_LABEL_IDS = [
        "1",
        "2",
        "3",
        "4",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
    ]

    jsonl_input_files = [
        file_name
        for file_name in os.listdir("training_data/input")
        if file_name.endswith(".jsonl")
    ]
    # Inizialize dataframe
    df_labeled_messages = pd.DataFrame(columns=["content"] + MISCONCEPTION_LABEL_IDS)
    for jsonl_input_file_name in jsonl_input_files:
        df_labeled_messages = pd.concat(
            [
                df_labeled_messages,
                get_labeled_messages_data_frame(
                    jsonl_input_file_name, MISCONCEPTION_LABEL_IDS
                ),
            ]
        )
    df_labeled_messages.index.name = "message_hash"
    df_labeled_messages.to_csv("training_data/output/labeled_messages.csv")
