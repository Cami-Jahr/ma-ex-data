import os
import json

SOURCE_EN = "manifests/resen"
SOURCE_JP = "manifests/resjp"


def get_files(source, file, primary_id):
    with open(os.path.join(source, f"{file}.json"), encoding="utf-8") as f:
        return {char[primary_id]: char for char in json.load(f)["payload"]["mstList"]}


def get_both(file, primary_id):
    return {
        "jp": get_files(SOURCE_JP, file, primary_id),
        "en": get_files(SOURCE_EN, file, primary_id),
    }
