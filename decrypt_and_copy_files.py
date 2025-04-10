import base64
import hashlib
import json
import os
from collections import defaultdict
import manifests.helpers as helpers


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
        item["pathId"]: {"path": item["path"], "taken": False}
        for item in dump["payload"]["pathMappingMstList"]
    }
    mstlist = dump["payload"]["mstList"]

    for mon in mstlist:
        salt = "1c7f"
        name = path_dict[mon["pathId"]]["path"] + mon["name"]
        path_dict[mon["pathId"]]["taken"] = True
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
        if "isEncrypted" not in mon or mon["isEncrypted"]:
            byte_key = generate_bytes_key(name + mon["cryptoKey"], "")
            file_keys[base64_str] = byte_key
        file_names[base64_str] = name


def copy_files(target_folder: str, cwd: str):
    occurrences: dict[str, int] = defaultdict(int)
    for root, _, files in os.walk(cwd):
        lroot = root.replace("/", "\\").split("\\")
        for filename in files:
            target_path = file_names.get(filename)
            if target_path:
                if "thumb" not in filename:
                    del file_names[filename]
                folders = target_path.split("/")
                known_mappings[filename] = folders[-1]
                for i in range(1, len(folders)):
                    known_mappings[lroot[-i]] = folders[-i - 1]

    backward_mappings = {v: k for k, v in known_mappings.items()}
    for k, v in file_names.items():
        print(
            f"{k} - {v:70} - {"/".join([backward_mappings.get(p, p) for p in v.split("/")[:-1]])
            + "/"
            + k:70}"
        )

    return

    for root, _, files in os.walk(cwd):
        for filename in files:
            target_list = os.path.join(root, filename).lstrip(cwd).split(os.path.sep)

            for i, val in enumerate(target_list):
                target_list[i] = known_mappings.get(val, val)

            if os.path.isfile(os.path.join(target_folder, *target_list)):
                continue
            with open(os.path.join(root, filename), "rb") as f:
                data = bytearray(f.read())

            try:
                file_key = file_keys.get(filename)
                data_type = bytes(data[:4])
                occurrences[str(data_type)] += 1
                if file_key:
                    # XOR each byte with the key for the encrypted ones
                    for i in range(len(data)):
                        data[i] ^= file_key[i % len(file_key)]
            except KeyError:
                print("INFO: Using obfuscated name for", os.path.join(root, filename))

            os.makedirs(os.path.join(target_folder, *target_list[:-1]), exist_ok=True)
            with open(os.path.join(target_folder, *target_list), "wb") as f:
                f.write(data)


if __name__ == "__main__":
    copy_files("processed", "com.aniplex.magia.exedra.en/files/CYU6")
