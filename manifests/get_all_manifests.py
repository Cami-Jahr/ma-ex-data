import requests
import json
import os
import sys

csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)
import helpers
import re


def download_manifests():
    token = helpers.get_token()
    for path in open("manifests/madoka_urls_en.txt").readlines():
        target_url = (
            f"https://static-masterdata-mmme.akamaized.net/api/mst/{path}&{token}"
        )
        response = requests.get(target_url)
        decrypted_response = helpers.decrypt_data(response.content)
        if response.status_code == 200:
            file = re.match(r"(.*?)\?.*", path)
            filename = f"manifests/resen/{file.groups()[0]}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(decrypted_response, f, ensure_ascii=False, indent=4)
        else:
            print("ERROR: Failed to fetch", target_url)


if __name__ == "__main__":
    download_manifests()
