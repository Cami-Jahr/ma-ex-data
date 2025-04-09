import base64
import hashlib
import json
import os
from collections import defaultdict


def generate_bytes_key(key, salt=""):
    if salt:
        key += salt

    sha512 = hashlib.sha512()
    key_bytes = key.encode("utf-8")
    sha512.update(key_bytes)
    hash1 = sha512.digest()

    sha512 = hashlib.sha512()
    sha512.update(hash1)
    hash2 = sha512.digest()

    result = hash1 + hash2
    return result


file_keys = {}
file_names = {}
known_mappings = {}

for manifest in (
    r"manifests\resen\get_resource_asset_bundle_mst_list.json",
    r"manifests\resjp\get_resource_file_mst_list.json",
):
    with open(manifest, "r", encoding="utf-8") as f:
        dump = json.load(f)

    path_dict = {
        item["pathId"]: item["path"] for item in dump["payload"]["pathMappingMstList"]
    }
    mstlist = dump["payload"]["mstList"]

    for key, mon in enumerate(mstlist):
        salt = "1c7f"
        name = path_dict.get(mon["pathId"], "Path not found") + mon["name"]
        input_str = name.split("/")[-1] + salt
        input_bytes = input_str.encode("utf-8")
        md5_hash = hashlib.md5(input_bytes).digest()
        base64_str = (
            base64.b64encode(md5_hash)
            .decode("utf-8")
            .replace("+", "-")
            .replace("/", "_")
            .rstrip("=")
        )
        byte_key = generate_bytes_key(name + mon["cryptoKey"], "")
        file_keys[base64_str] = byte_key
        file_names[base64_str] = name


def copy_files(target_folder: str, cwd: str):
    occurrences: dict[str, int] = defaultdict(int)
    known_types = (b"CRID", b"AFS2", b"@UTF")
    for root, _, files in os.walk(cwd):
        lroot = root.replace("/", "\\").split("\\")
        for filename in files:
            target_path = file_names.get(filename)
            if target_path:
                folders = target_path.split("/")
                known_mappings[filename] = folders[-1]
                for i in range(1, len(folders)):
                    known_mappings[lroot[-i]] = folders[-i - 1]

    for root, _, files in os.walk(cwd):
        for filename in files:
            with open(os.path.join(root, filename), "rb") as f:
                data = bytearray(f.read())

            try:
                file_key = file_keys.get(filename)
                data_type = bytes(data[:4])
                occurrences[str(data_type)] += 1
                if file_key and data_type not in known_types:
                    # usm, acb and awb files are only common patterns I've found which are not encrypted, just the name is obfuscated
                    # XOR each byte with the key for the encrypted ones
                    for i in range(len(data)):
                        data[i] ^= file_key[i % len(file_key)]
            except KeyError:
                print("INFO: Using obfuscated name for", os.path.join(root, filename))

            target_list = os.path.join(root, filename).lstrip(cwd).split(os.path.sep)

            for i, val in enumerate(target_list):
                target_list[i] = known_mappings.get(val, val)

            os.makedirs(os.path.join(target_folder, *target_list[:-1]), exist_ok=True)
            with open(os.path.join(target_folder, *target_list), "wb") as f:
                f.write(data)

    for k, v in occurrences.items():
        if v > 1 and k not in (str(s) for s in known_types):
            print(f"MISSING KNOWN TYPE? {v} occurrences of {k} were spotted")


if __name__ == "__main__":
    copy_files("processed", "com.aniplex.magia.exedra.en/files/CYU6")
