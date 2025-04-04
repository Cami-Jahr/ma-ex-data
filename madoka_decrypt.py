import base64
import hashlib
import json
import os


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


file_locations = {}
known_mappings = {}

for manifest in (
    r"D:\madoka-exedra\manifests\resen\get_resource_asset_bundle_mst_list.json",
    r"D:\madoka-exedra\manifests\resjp\get_resource_file_mst_list.json",
):
    dump = json.load(open(manifest, "r"))

    path_dict = {
        item["pathId"]: item["path"] for item in dump["payload"]["pathMappingMstList"]
    }
    mstlist = dump["payload"]["mstList"]

    for key in range(len(mstlist)):
        mon = mstlist[key]

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
        file_locations[base64_str] = (byte_key, name)


def copy_files(target_folder: str, cwd: str):
    for root, _, files in os.walk(cwd):
        lroot = root.replace("/", "\\").split("\\")
        for filename in files:
            target_path = file_locations.get(filename, (None, None))[1]
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
                key, name = file_locations[filename]
                # XOR each byte with the key
                if ".usm" not in name and ".awb" not in name and ".acb" not in name:
                    # audio and video files are not encrypted, just the name is obfuscated,
                    #  it's very possible more things should be excluded but I don't know what yet
                    for i in range(len(data)):
                        data[i] ^= key[i % len(key)]
            except:
                print("INFO: Using obfuscated name for", os.path.join(root, filename))

            target_list = os.path.join(root, filename).lstrip(cwd).split(os.path.sep)

            for i in range(len(target_list)):
                target_list[i] = known_mappings.get(target_list[i], target_list[i])

            os.makedirs(os.path.join(target_folder, *target_list[:-1]), exist_ok=True)
            with open(os.path.join(target_folder, *target_list), "wb") as f:
                f.write(data)


if __name__ == "__main__":
    copy_files("processed", "com.aniplex.magia.exedra.en/files/CYU6")
