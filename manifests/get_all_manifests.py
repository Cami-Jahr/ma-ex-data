import requests
import json
import os
import sys
import set_lang
import get_token

csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)
import helpers


def download_manifests(is_en=False, token=None):
    request_body = helpers.BASE_BODY.copy()
    request_body["payload"] = {
        "revision": "2665b791af8875c5a0b5d835a5397a32",
        "platform": None,
    }
    for mst in json.load(
        open(
            f"manifests/res{"en" if is_en else "jp"}/get_resource_master_data_mst_list.json"
        )
    )["payload"]["mstList"]:
        path = mst["name"]
        request_body["payload"]["id"] = f"GetMstList:{path}"
        request_body["payload"]["language"] = mst["language"]

        if is_en:
            # TODO key is needed to request correct lang, should figure out how to generate
            key = "MiaqHhKOHuuWD781hG1IB_lp8vfrfA"
        else:
            key = "IpiRHhKOHW8sJ1YP1ef9eePQv4TnvQ"

        target_url = f"https://static-masterdata-mmme.akamaized.net/api/mst/{path}?key={key}&{token}"
        response = requests.post(
            target_url, helpers.encrypt_data(request_body), timeout=10
        )
        try:
            response.raise_for_status()
            decrypted_response = helpers.decrypt_data(response.content)
            filename = f"manifests/res{"en" if is_en else "jp"}/{path}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(decrypted_response, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("ERROR: Failed to fetch", target_url, "\nException:", e)


def run(is_en=True):
    set_lang.set_language(is_en)
    token = get_token.get_token(is_en)
    download_manifests(is_en, token)


if __name__ == "__main__":
    # run(True) #TODO This doesn't work, only downloads Style correctly, suspect it has something to do with the key
    run(False)
