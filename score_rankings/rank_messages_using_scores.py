"""
How to Use
----------
Place files into the input directory
- misinfo.json
- Score json files, e. g. train-bm25-scores.json
Set INPUT_FILE_NAME to the name of the file you want to use
Run script

Result: One json file for each misconception which contains a ranking of messages (ids)
    according to the scores from the file in the input directory.
"""

import json
import os

INPUT_FILE_NAME = "train-bert-scores.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as input_file:
        return json.load(input_file)


def store_json(file_path, dictionary):
    output_file = open(file_path, "w", encoding="utf-8")
    json.dump(
        dictionary,
        output_file,
        indent=4,
        sort_keys=True,
        ensure_ascii=False,
        default=str,
    )
    output_file.close()


def rank_message_relevancy_by_misconception_scores(input_file_name):
    if not os.path.exists("score_rankings/output/"):
        os.makedirs("score_rankings/output/")

    misconceptions = load_json("score_rankings/input/misinfo.json")
    scores = load_json(f"score_rankings/input/{input_file_name}")
    # Create ranking for each misconception consisting of a list of tuples
    # (message_id, score)
    for misconception_id in misconceptions:
        misconception_values = [
            (key, values[str(misconception_id)])
            for key, values in scores.items()
            if str(misconception_id) in values.keys()
        ]
        misconception_ranking = sorted(
            misconception_values, key=lambda item: item[1], reverse=True
        )
        file_prefix = input_file_name.split(".json")[0]
        if not os.path.exists(f"score_rankings/output/{file_prefix}"):
            os.makedirs(f"score_rankings/output/{file_prefix}")
        title_no_slashes = misconceptions[misconception_id]["title"].replace("/", "|")
        store_json(
            f"score_rankings/output/{file_prefix}/" + f"{title_no_slashes}.json",
            misconception_ranking,
        )


def create_misconception_message_retrieval_rankings():
    """
    Create a ranking of messages for each misconception according to the scores in the
    input directory.
    """
    scores_json_files = [
        input_file_name
        for input_file_name in os.listdir("score_rankings/input")
        if input_file_name.endswith("scores.json")
    ]

    for file_name in scores_json_files:
        rank_message_relevancy_by_misconception_scores(file_name)


def rank_message_relevancy_by_cumulative_scores(
    scores_object, output_dir, output_file_name
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cumulative_scores = {}
    for key, value in scores_object.items():
        cumulative_scores[key] = sum(score for _, score in value.items())

    cumulative_ranking = sorted(
        cumulative_scores.items(), key=lambda item: item[1], reverse=True
    )
    store_json(
        f"{output_dir}/{output_file_name}.json",
        cumulative_ranking,
    )


def create_cumulative_message_retrieval_ranking(
    scores_path="data/scores", scoring_method="bm25"
):
    """
    Create a ranking by calculating the cumulative relevancy scores of each message in
    the data set for each misconception (these need to be computed beforehand using BM25
    or BERT and stored as json files in the given path).

    Args:
        scores_path (str, optional): Where the scores json files are stored.
            Defaults to "data/scores".
        scoring_method (str, optional): Either "bm25" or "bert". Defaults to "bm25".
    """
    for file_name in os.listdir(scores_path):
        if file_name.split("-")[1] == scoring_method:
            scores = load_json(f"{scores_path}/{file_name}")
            rank_message_relevancy_by_cumulative_scores(
                scores,
                "data/message_rankings/cumulative_rankings",
                f"{file_name.split('-')[0]}-cumulative-{scoring_method}-ranking",
            )


if __name__ == "__main__":
    # create_cumulative_message_retrieval_ranking()
    # create_misconception_message_retrieval_rankings()
    rank_message_relevancy_by_misconception_scores(INPUT_FILE_NAME)
