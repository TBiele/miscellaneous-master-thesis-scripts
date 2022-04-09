"""
How to Use
----------
Place misconception table json exported from Web labeling interface into input directory
Run script

Result: Json file that uses the misinfo.json format from the CoVaxLies paper is created
    in the output directory.
"""

import json
import os


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
        return json.loads(data)


if __name__ == "__main__":
    web_interface_json_files = [
        file_name
        for file_name in os.listdir("conversion/input")
        if file_name.startswith("Misconception")
    ]
    for web_interface_json_file_name in web_interface_json_files:
        misinfo_json_object = {}
        web_interface_json_file_object_list = load_json(
            "conversion/input/" + web_interface_json_file_name
        )
        for web_interface_json_file_object in web_interface_json_file_object_list:
            misinfo_json_object[web_interface_json_file_object["id"]] = {
                "title": web_interface_json_file_object["name"],
                "text": web_interface_json_file_object["description"],
            }
        with open(
            "conversion/output/"
            + web_interface_json_file_name.split(".json")[0]
            + "-misinfo.json",
            "w",
        ) as output_file:
            output_file.write(json.dumps(misinfo_json_object, ensure_ascii=False))
