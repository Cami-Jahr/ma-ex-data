from subprocess import PIPE, Popen, DEVNULL
import shutil
import os
import acb


def convert_acb(src_dir):
    for root, _, files in os.walk(src_dir):
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
                        with open(f"{folder}/error.txt", "w", encoding="utf-8") as f:
                            f.write(str(e))
                        print(f"Error when converting {abs_path} to {folder}: {e}")


def convert_hca(src_dir):
    # print(src_dir)
    for root, _, files in os.walk(src_dir):
        # print(root, files)
        for file in files:
            if "error.txt" in files:
                break
            abs_path = os.path.join(root, file)
            dest_root = root.replace("_HCAs", "_WAVs")
            dest_path = os.path.join(dest_root, file.replace(".hca", ".wav"))
            # print(abs_path)
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


def convert_awb(src_dir):
    for root, _, files in os.walk(src_dir):
        for file in files:
            abs_path = os.path.join(root, file)
            dest_file = f"{abs_path}.wav"
            if open(abs_path, "rb").read()[:4] == b"AFS2":
                shutil.copy2(abs_path, f"{abs_path}.awb")
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


def convert(dir):
    convert_acb(dir)
    convert_awb(dir)
    convert_hca(dir)


if __name__ == "__main__":
    convert(r"D:\madoka-exedra\processed\media\assets\audio")
