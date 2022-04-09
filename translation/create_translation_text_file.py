"""
How to Use
----------
Set DEEPL_AUTH_KEY (or leave empty to use free Google Translate API)
Put jsonl files into input directory
Run script

Result: Jsonl files with translated text in output directory
"""

import deepl
import json
import os
import translators as ts

DEEPL_AUTH_KEY = ""


def iterate_over_jsonl_file(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield json.loads(line)


def translate_input_files(deepl_auth_key):
    jsonl_input_files = [
        file_name
        for file_name in os.listdir("translation/input")
        if file_name.endswith(".jsonl")
    ]
    if deepl_auth_key:
        translator = deepl.Translator(DEEPL_AUTH_KEY)
    for jsonl_file in jsonl_input_files:
        file_path = os.path.join("translation/input", jsonl_file)
        with open(f"translation/output/{jsonl_file}", "w") as f:
            for message_object in iterate_over_jsonl_file(file_path):
                if translator:
                    translation = translator.translate_text(
                        message_object["full_text"], target_lang="EN-US"
                    )
                    message_object["full_text"] = str(translation)
                else:
                    translation = ts.google(
                        message_object["full_text"],
                        from_language="de",
                        to_language="en",
                    )
                    message_object["full_text"] = translation
                f.write(json.dumps(message_object, ensure_ascii=False))
                f.write("\n")


if __name__ == "__main__":
    if DEEPL_AUTH_KEY != "":
        translate_input_files(DEEPL_AUTH_KEY)
    else:
        translate_input_files()
