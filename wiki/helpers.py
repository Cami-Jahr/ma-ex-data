import os
import json

SOURCE_EN = "manifests/resen"
SOURCE_JP = "manifests/resjp"


def get_files(source, file, idfield):
    with open(os.path.join(source, f"{file}.json"), encoding="utf-8") as f:
        return {char[idfield]: char for char in json.load(f)["payload"]["mstList"]}


def get_both(file, idfield):
    return {
        "jp": get_files(SOURCE_JP, file, idfield),
        "en": get_files(SOURCE_EN, file, idfield),
    }
