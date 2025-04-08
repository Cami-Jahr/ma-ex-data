from subprocess import PIPE, Popen, DEVNULL
import shutil
import os
import acb


def convert_acb(src_dir):
    for root, _, files in os.walk(src_dir):
        for file in files:
            abs_path = os.path.join(root, file)
            if open(abs_path, "rb").read()[:4] == b"@UTF":
                if ".acb" not in abs_path:
                    # If file is obfuscated rename it to same as unobfuscated ones
                    shutil.copy2(abs_path, f"{abs_path}.acb")
                    abs_path = f"{abs_path}.acb"
                hca_folder = f"{abs_path[:-4]}_HCAs"  # Remove .acb from folder name

                if not os.path.isdir(hca_folder):
                    os.makedirs(hca_folder, 0o755, exist_ok=True)
                    try:
                        # extract_acb automatically detects awb files in the same folder if it is needed.
                        # Exedra always uses the same name for the awb and matching acb
                        # All awb have a describing awb. Some acb have the awb embedded, but some acb are orphaned and produces the error below
                        acb.extract_acb(abs_path, hca_folder)  # type: ignore This isn't actually supposed to be able to be used from code, only cli, but might makes right
                    except ValueError as e:
                        if "but there's no external AWB attached." not in str(e):
                            # Can't really do anything about this. Means the audio hasn't been released, but the metadata/ management file has been.
                            print(
                                f"ERROR: When converting {abs_path} to {hca_folder}: {e}"
                            )
                        shutil.rmtree(hca_folder)
                        # Delete the folder, it doesn't contain any useful data, couldn't parse so this is just a trash folder


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
                            f"ERROR: [ {" ".join([
                                "vgmstream/vgmstream-cli.exe",
                                "-o",
                                f'"{dest_path}"',
                                f'"{abs_path}"',
                            ])} ] failed because of {e}"
                        )


def minimize(src_dir, dst_dir):
    for root, _, files in os.walk(src_dir):
        dst_root = root.replace(src_dir, dst_dir).replace("_WAVs", "")
        for file in files:
            dst_file = os.path.join(dst_root, f"{file[:-4]}.ogg")
            if file[-4:] == ".wav" and not os.path.isfile(dst_file):
                os.makedirs(dst_root, 0o755, exist_ok=True)
                if b"Encoding complete" not in (
                    e := Popen(
                        [
                            "VGM/opusenc.exe",
                            os.path.join(root, file),
                            dst_file,
                        ],
                        stderr=PIPE,
                        stdout=DEVNULL,
                    ).stderr.read()  # type: ignore
                ):
                    print(
                        f"ERROR: [ {" ".join([
                                "VGM/opusenc.exe",
                                f'"{os.path.join(root, file)}"',
                                f'"{dst_file}"'
                            ])} ] failed because of {e}"
                    )


def convert(src_dir, dst_dir):
    convert_acb(src_dir)
    convert_hca(src_dir, dst_dir)


if __name__ == "__main__":
    convert(
        r"processed\gallery\kfOi\Sound",
        r"full\gallery\kfOi\Sound",
    )
    minimize(
        r"full\gallery\kfOi\Sound",
        r"mini\gallery\kfOi\Sound",
    )
