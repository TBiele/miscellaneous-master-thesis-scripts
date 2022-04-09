"""
How to Use
----------
Create data set directory inside input
Place files into directory
- train.jsonl, dev.jsonl
- train-bm25-scores.json, dev-bm25-scores.json, ...
- misinfo.json
Change DATA_SET_NAME to the data set directory name
Change MISCONCEPTION_LABEL_IDS, if necessary
Comment out the method you do not want to see from the main function
Run script

Result: Prints the hits@1, hits@5 and hits@10 scores for each misconception when using
    the scores of the given method for the specified method.
"""

import json

DATA_SET_NAME = MY_DATA_SET_NAME
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


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
        return json.loads(data)


def get_misinfo_title(misinfo_json, misinfo_id):
    return misinfo_json[misinfo_id]["title"]


def get_positive_examples_for_misconception(input_file, misconception_id):
    """
    Get positive instances of the specified misconception from the given jsonl file.

    Args:
        input_file (str): Name of the jsonl file, i. e. train.jsonl or dev.jsonl
        misconception_id (str): Misconception id to search for in the jsonl file

    Returns:
        list: List of message ids
    """
    positive_examples = []
    with open(input_file, "r") as f:
        for line in f:
            line_object = json.loads(line)
            if misconception_id in line_object["misinfo"].keys():
                positive_examples.append(line_object["id"])
    return positive_examples


def evaluate(retrieval_method, print_as_latex_table=False):
    """
    Calculate hits@1, hits@5 and hits@10 using the scores of the given retrieval method.
    Print the results.

    Args:
        retrieval_method (str): 'bm25' or 'bert'
        print_as_latex_table (bool, optional): Whether to print the results formatted as
            LaTeX table rows that can be copied into a document. Defaults to False.
    """
    misinfo_json = load_json("evaluation/input/" + DATA_SET_NAME + "/misinfo.json")
    for misconception_id in MISCONCEPTION_LABEL_IDS:
        number_of_misconceptions = len(MISCONCEPTION_LABEL_IDS)
        # Get positive example messages for misconception
        misconception_messages_list = (
            get_positive_examples_for_misconception(
                "evaluation/input/" + DATA_SET_NAME + "/train.jsonl", misconception_id
            )
            + get_positive_examples_for_misconception(
                "evaluation/input/" + DATA_SET_NAME + "/dev.jsonl", misconception_id
            )
            + get_positive_examples_for_misconception(
                "evaluation/input/" + DATA_SET_NAME + "/test.jsonl", misconception_id
            )
        )

        # Get dictionary of prediction rankings for each message
        train_scores = load_json(
            "evaluation/input/"
            + DATA_SET_NAME
            + f"/train-{retrieval_method}-scores.json"
        )
        dev_scores = load_json(
            "evaluation/input/" + DATA_SET_NAME + f"/dev-{retrieval_method}-scores.json"
        )
        test_scores = load_json(
            "evaluation/input/"
            + DATA_SET_NAME
            + f"/test-{retrieval_method}-scores.json"
        )
        scores = {
            k: v for d in [train_scores, dev_scores, test_scores] for k, v in d.items()
        }
        correct_positions_in_rankings = []
        for message_hash in misconception_messages_list:
            # sort scores dict by value
            sorted_scores = sorted(
                scores[message_hash].items(), key=lambda x: x[1], reverse=True
            )
            message_misconception_ranking = list(map(lambda x: x[0], sorted_scores))
            misconception_position_in_ranking = (
                message_misconception_ranking.index(misconception_id) + 1
                if misconception_id in message_misconception_ranking
                else number_of_misconceptions
            )
            correct_positions_in_rankings.append(misconception_position_in_ranking)
        relevant_misconception_examples = len(correct_positions_in_rankings)
        # calculate hits@1,5,10
        if relevant_misconception_examples > 0:
            hits_at_1 = (
                sum([1 for pos in correct_positions_in_rankings if pos == 1])
                / relevant_misconception_examples
                * 100
            )
            hits_at_5 = (
                sum([1 for pos in correct_positions_in_rankings if pos <= 5])
                / relevant_misconception_examples
                * 100
            )
            hits_at_10 = (
                sum([1 for pos in correct_positions_in_rankings if pos <= 10])
                / relevant_misconception_examples
                * 100
            )
        else:
            hits_at_1, hits_at_5, hits_at_10 = 0, 0, 0

        if print_as_latex_table:
            print(
                str(get_misinfo_title(misinfo_json, misconception_id))
                + " & "
                + str(relevant_misconception_examples)
                + " & "
                + str(round(hits_at_1, 2))
                + " & "
                + str(round(hits_at_5, 2))
                + " & "
                + str(round(hits_at_10, 2))
                + " \\\\"
            )
        else:
            print(
                "Result for misconception",
                get_misinfo_title(misinfo_json, misconception_id),
                f"({relevant_misconception_examples} examples)",
            )
            print("hits@1   hits@5  hits@10")
            print(f"{hits_at_1}     {hits_at_5}    {hits_at_10}")
            print("")


def evaluate_bm25(print_as_latex_table=False):
    evaluate("bm25", print_as_latex_table)


def evaluate_bertscore(print_as_latex_table=False):
    evaluate("bert", print_as_latex_table)


if __name__ == "__main__":
    evaluate_bm25()
    # evaluate_bertscore()
