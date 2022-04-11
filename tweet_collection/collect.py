"""
How to Use
----------
Set BEARER_TOKEN to your Twitter API bearer token.
Create data set directory inside input
Put jsonl files into data set directory (e. g. train.jsonl, dev.jsonl, test.jsonl)
Set DATA_SET_NAME and JSON_FILE_NAME
Run script

Result: Jsonl file with full tweet text is saved in output directory
"""

import csv
import json
import os
import pandas as pd
import time
import tweepy

BEARER_TOKEN = YOUR_BEARER_TOKEN

DATA_SET_NAME = "v2"
JSONL_FILE_NAME = "test.jsonl"

client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)


def build_multilabel_csv_from_jsonl(jsonl_title):
    with open("tweet_collection/input/misinfo.json", "r", encoding="utf-8") as file:
        misinfo_categories = json.load(file)
    misinfo_titles = [misinfo["title"] for misinfo in list(misinfo_categories.values())]
    misinfo_id_to_index = {
        misinfo_id: index for index, misinfo_id in enumerate(misinfo_categories.keys())
    }
    zeros = [0 for i in range(len(misinfo_titles))]
    df = pd.DataFrame(columns=["message_hash", "content"] + misinfo_titles)
    df = df.set_index("message_hash")
    with open(f"tweet_collection/input/{jsonl_title}.jsonl") as file:
        for line in file:
            line_object = json.loads(line)
            relevant_misinfo = 0
            misinfo_vector = list(zeros)
            for misinfo_id in line_object["misinfo"].keys():
                if line_object["misinfo"][misinfo_id] == "agree":
                    relevant_misinfo = 1
                    misinfo_vector[misinfo_id_to_index[misinfo_id]] = 1
            if relevant_misinfo == 1:
                tweet_id = line_object["id"]
                time.sleep(0.5)
                tweet_text = get_tweet_text(tweet_id)
                if tweet_text is not None:
                    df.loc[tweet_id] = [tweet_text] + misinfo_vector
    df.to_csv(f"{jsonl_title}.csv", index_label="tweet_id")


def build_full_tweet_dataset(version, jsonl_file_name):
    if not os.path.exists(f"tweet_collection/output/{version}"):
        os.mkdir(f"tweet_collection/output/{version}")

    with open(f"tweet_collection/input/{version}/{jsonl_file_name}") as input_file:
        with open(f"tweet_collection/output/{version}/{jsonl_file_name}", "w") as output_file:
            for line in input_file:
                line_object = json.loads(line)
                tweet_id = line_object["id"]
                tweet_text = get_tweet_text(tweet_id)
                if tweet_text is not None:
                    line_object["full_text"] = tweet_text
                    output_file.write(json.dumps(line_object) + "\n")


def build_full_covid_lies_dataset():
    if not os.path.exists("tweet_collection/output/"):
        os.mkdir("tweet_collection/output/")

    with open("tweet_collection/input/covid_lies.csv") as input_file:
        with open("tweet_collection/output/covid_lies.jsonl", "w") as output_file:
            csv_reader = csv.reader(input_file, delimiter=",")
            next(csv_reader)
            for line in csv_reader:
                if line[3] == "pos":
                    tweet_id = line[2]
                    tweet_text = get_tweet_text(tweet_id)
                    if tweet_text is not None:
                        line_object = {
                            "id": tweet_id,
                            "misconception_id": line[0],
                            "full_text": tweet_text,
                        }
                        output_file.write(json.dumps(line_object) + "\n")


def get_tweet_text(tweet_id):
    tweet = client.get_tweet(tweet_id)
    if tweet.data is not None:
        return tweet.data.text
    else:
        if tweet.errors is not None:
            for error in tweet.errors:
                print(error["detail"])
        else:
            print(f"Tweet with id {tweet_id} not found. Response invalid.")
        return None


if __name__ == "__main__":
    build_full_tweet_dataset(DATA_SET_NAME, JSONL_FILE_NAME)
