from subprocess import PIPE, Popen, DEVNULL
import shutil
import os
import acb
from collections import defaultdict
import json


def convert_acb(src_dir):
    with open("complementing_awbs.json", "r") as f:
        data = json.load(f)
    mapping_overview = defaultdict(set, {k: set(v) for k, v in data.items()})

    for root, _, files in os.walk(src_dir):
        awb_files = [f for f in files if ".awb" in f]
        for file in files:
            abs_path = os.path.join(root, file)
            if "." not in file and open(abs_path, "rb").read()[:4] == b"@UTF":
                folder = f"{abs_path}_HCAs"
                shutil.copy2(abs_path, f"{abs_path}.acb")
                if not os.path.isdir(folder):
                    os.makedirs(folder, 0o755, exist_ok=True)
                    try:
                        acb.extract_acb(f"{abs_path}.acb", folder)  # type: ignore This isn't actually supposed to be able to be used from code, only cli, but might makes right
                    except ValueError as e:
                        for (
                            i
                        ) in (
                            awb_files
                        ):  # Check what awb files could possibly work as input for the acb, testing aid to complemeting_awb_matcher.py
                            try:
                                acb.extract_acb(f"{abs_path}.acb", folder, os.path.join(root, i))  # type: ignore
                                mapping_overview[abs_path].add(
                                    i
                                )  # If it actually worked, write it down
                            except ValueError:
                                pass
                        if "but there's no external AWB attached." not in str(
                            e
                        ):  # This is just for those which expect an external awb, just noise for now
                            print(f"Error when converting {abs_path} to {folder}: {e}")
                        shutil.rmtree(folder)

    with open("complementing_awbs.json", "w") as f:
        json.dump({k: list(v) for k, v in mapping_overview.items()}, f)


def convert_hca(src_dir, dst_dir):
    for root, _, files in os.walk(src_dir):
        for file in files:
            abs_path = os.path.join(root, file)
            dest_root = root.replace(src_dir, dst_dir).replace("_HCAs", "_WAVs")
            dest_path = os.path.join(dest_root, file.replace(".hca", ".wav"))
            if ".hca" == file[-4:]:
                os.makedirs(dest_root, 0o755, exist_ok=True)
                if not os.path.isfile(dest_path):
                    if (
                        e := Popen(
                            [
                                "vgmstream/vgmstream-cli.exe",
                                "-o",
                                dest_path,
                                abs_path,
                            ],
                            stdout=DEVNULL,
                            stderr=PIPE,
                        ).stderr.read()  # type: ignore
                    ) != b"":
                        print(
                            f"Creating [ {" ".join([
                                "vgmstream/vgmstream-cli.exe",
                                "-o",
                                f'"{dest_path}"',
                                f'"{abs_path}"',
                            ])} ] failed because of {e}"
                        )
    for root, _, files in os.walk(
        dst_dir
    ):  # Put non-obfuscated name found in acb as folder names
        if "_WAVs" in root:
            new_root = root.replace(
                os.path.basename(root), os.path.commonprefix(files).rstrip("_ ")
            )
            try:
                shutil.rmtree(new_root)
            except FileNotFoundError:
                pass
            os.rename(root, new_root)


def convert_awb(src_dir, dst_dir):
    for root, _, files in os.walk(src_dir):
        for file in files:
            abs_path = os.path.join(root, file)
            dst_root = root.replace(src_dir, dst_dir)
            dest_file = f"{os.path.join(dst_root, file)}.wav"
            if "." not in file and open(abs_path, "rb").read()[:4] == b"AFS2":
                shutil.copy2(abs_path, f"{abs_path}.awb")
                os.makedirs(dst_root, 0o755, exist_ok=True)
                if not os.path.isfile(dest_file):
                    print("Running:", dest_file)
                    if (
                        e := Popen(
                            [
                                "vgmstream/vgmstream-cli.exe",
                                "-o",
                                dest_file,
                                f"{abs_path}.awb",
                            ],
                            stdout=DEVNULL,
                            stderr=PIPE,
                        ).stderr.read()  # type: ignore
                    ) != b"":
                        print(f"Creating {dest_file} failed because of {e}")


def minimize(src_dir, dst_dir):
    for root, _, files in os.walk(src_dir):
        dst_root = root.replace(src_dir, dst_dir)
        for file in files:
            if file[-4:] == ".wav" and not os.path.isfile(
                os.path.join(dst_root, f"{file[:-4]}.ogg")
            ):
                print(root, file)
                os.makedirs(dst_root, 0o755, exist_ok=True)
                print(
                    Popen(
                        [
                            "VGM/opusenc.exe",
                            os.path.join(root, file),
                            os.path.join(dst_root, f"{file[:-4]}.ogg"),
                        ],
                        stderr=PIPE,
                        stdout=DEVNULL,
                    ).stderr.read()  # type: ignore
                )


def convert(src_dir, dst_dir):
    convert_awb(src_dir, dst_dir)
    convert_acb(src_dir)
    convert_hca(src_dir, dst_dir)


if __name__ == "__main__":
    convert(
        r"D:\madoka-exedra\processed\media\assets\audio",
        r"D:\madoka-exedra\full\media\assets\audio",
    )
    minimize(
        r"D:\madoka-exedra\full\media\assets\audio",
        r"D:\madoka-exedra\mini\media\assets\audio",
    )
