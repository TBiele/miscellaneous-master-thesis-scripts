"""
How to Use
----------
Put json with labels in the input folder (exported table MessageMisconception of the Web
    labeling interface)
Set EXCLUDE_CLEARLY_IRRELEVANT_MESSAGES to True or False, depending on whether messages
    that were labeled as irrelevant (i. e. no label applies) by every annotator should
    be counted.
Run script

Result: Print the messages and labelings of messages that were labeled by two or three
    users. Then print the inter-rater agreement percentages for messages labeled by two
    and three users, respectively.
"""

import json
import os

EXCLUDE_CLEARLY_IRRELEVANT_MESSAGES = True


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
        return json.loads(data)


# Credit: https://stackoverflow.com/a/66763499
# This function transforms a list of json objects into a tree structure where
# properties are nested in a certain order and values of the objects are grouped
# together based on common values of the properties in the current path of the tree
def groupBy(vetor, campos, pos):
    if pos >= len(campos):
        return vetor
    gmx = campos[pos]
    agrupado = gmx["field"]
    kx = gmx["gbkey"]
    agrupados = {}
    saida = {}
    retorno = []
    for l in vetor:
        lmf = {}
        for k, s in l.items():
            val_agrupado = l[agrupado]
            if not (val_agrupado in agrupados):
                agrupados[val_agrupado] = []
            if agrupado != k:
                lmf[k] = s
        agrupados[val_agrupado].append(lmf)
    for l in agrupados:
        agrup = agrupados[l]
        if len(campos) > 1:
            agrup = groupBy(agrup, campos, pos + 1)
        saida = {}
        saida[agrupado] = l
        saida[kx] = agrup
        retorno.append(saida)
    return retorno


def get_labels_list(message_labels_from_user):
    return [
        label_object["misconception"]
        for label_object in message_labels_from_user["labels"]
    ]


if __name__ == "__main__":
    json_input_files = [
        file_name
        for file_name in os.listdir("evaluation/input")
        if file_name.endswith(".json")
    ]
    if len(json_input_files) != 1:
        print(
            "Please put exactly one json file into input/ which contains the labels "
            "from the Web interface"
        )
    # Get messages labeled by two people
    # What percentage have the same labelings?
    label_objects = load_json("evaluation/input/" + json_input_files[0])

    labels_nested = groupBy(
        label_objects,
        [
            {"field": "message", "gbkey": "labelings"},
            {"field": "user", "gbkey": "labels"},
        ],
        0,
    )
    overlap_two_agree = 0
    overlap_two_disagree = 0
    overlap_three_agree = 0
    overlap_three_disagree = 0
    for message_labels_object in labels_nested:
        user_labelings_as_lists_of_labels_ids = message_labels_object["labelings"]
        if len(user_labelings_as_lists_of_labels_ids) > 1:
            user_labelings_lists_of_labels_ids = [
                get_labels_list(user_labeling)
                for user_labeling in user_labelings_as_lists_of_labels_ids
            ]
            [
                get_labels_list(user_labeling)
                for user_labeling in user_labelings_as_lists_of_labels_ids
            ]
            print(
                f"{message_labels_object['message']} was labeled by "
                f"{len(message_labels_object['labelings'])} people. Labelings: "
                f"{user_labelings_lists_of_labels_ids}"
            )
            if len(user_labelings_lists_of_labels_ids) == 2:
                if (
                    EXCLUDE_CLEARLY_IRRELEVANT_MESSAGES
                    and user_labelings_lists_of_labels_ids[0] == [""]
                    and user_labelings_lists_of_labels_ids[1] == [""]
                ):
                    continue
                if (
                    user_labelings_lists_of_labels_ids[0]
                    == user_labelings_lists_of_labels_ids[1]
                ):
                    overlap_two_agree += 1
                else:
                    overlap_two_disagree += 1
            if len(user_labelings_lists_of_labels_ids) == 3:
                if (
                    EXCLUDE_CLEARLY_IRRELEVANT_MESSAGES
                    and user_labelings_lists_of_labels_ids[0] == [""]
                    and user_labelings_lists_of_labels_ids[1] == [""]
                    and user_labelings_lists_of_labels_ids[2] == [""]
                ):
                    continue
                if (
                    user_labelings_lists_of_labels_ids[0]
                    == user_labelings_lists_of_labels_ids[1]
                    and user_labelings_lists_of_labels_ids[1]
                    == user_labelings_lists_of_labels_ids[2]
                ):
                    overlap_three_agree += 1
                else:
                    overlap_three_disagree += 1
    print("\nInter-rater Agreement as the percentage of consistent labelings:")
    print(
        "Agreement for messages labeled by two",
        "(excluding messages that were were not assigned a label by anyone):"
        if EXCLUDE_CLEARLY_IRRELEVANT_MESSAGES
        else ":",
        overlap_two_agree / (overlap_two_agree + overlap_two_disagree),
        f"({overlap_two_agree + overlap_two_disagree} messages in total)",
    )
    print(
        "Agreement for messages labeled by three",
        "(excluding messages that were were not assigned a label by anyone):"
        if EXCLUDE_CLEARLY_IRRELEVANT_MESSAGES
        else ":",
        overlap_three_agree / (overlap_three_agree + overlap_three_disagree),
        f"({overlap_three_agree + overlap_three_disagree} messages in total)",
    )
