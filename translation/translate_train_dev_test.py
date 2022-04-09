"""
How to Use
----------
Put jsonl files (train.jsonl, dev.jsonl, test.jsonl) into input directory
Put the translation file containing all message translations into the input directory
SET FULL_TRANSLATION_FILE to the name of the translation file
Run script

Result: Jsonl files (train, dev, test) with translated text in output directory
"""

import json


FULL_TRANSLATION_FILE = ""


def translate_part_of_dataset(file_path):
    output_file_path = file_path.replace("input", "output")
    with open(output_file_path, "w") as output_file:
        with open(file_path, "r") as input_file:
            for input_line in input_file:
                input_line_object = json.loads(input_line)
                with open(
                    f"translation/input/{FULL_TRANSLATION_FILE}", "r"
                ) as translation_file:
                    for translation_file_line in translation_file:
                        translation_file_line_object = json.loads(translation_file_line)
                        if (
                            input_line_object["id"]
                            == translation_file_line_object["id"]
                        ):
                            input_line_object[
                                "full_text"
                            ] = translation_file_line_object["full_text"]
                            output_file.write(
                                json.dumps(input_line_object, ensure_ascii=False) + "\n"
                            )
                            break


def translate_train_dev_test_files():
    translate_part_of_dataset("translation/input/train.jsonl")
    translate_part_of_dataset("translation/input/dev.jsonl")
    translate_part_of_dataset("translation/input/test.jsonl")


if __name__ == "__main__":
    translate_train_dev_test_files()
