from subprocess import PIPE, Popen, DEVNULL
import shutil
import os


def convert(src_dir):
    for root, _, files in os.walk(src_dir):
        for file in files:
            if "." in file:
                continue
            abs_path = os.path.join(root, file)
            dest_file = f"{abs_path}.wav"
            tag = open(abs_path, "rb").read()[:4]
            run_config = [
                "vgmstream/vgmstream-cli.exe",
                "-o",
                dest_file,
            ]
            if (
                tag == b"@UTF"
            ):  # ACB files sometimes have audio embedded, and sometimes refer to other files, this only really handles those with 1 embeded awb file, but not always see #voicelines. Unsure how to fix those that compile into wav but is like 1 sec sound
                shutil.copy2(abs_path, f"{abs_path}.acb")
                run_config += [f"{abs_path}.acb"]
            elif tag == b"AFS2":
                shutil.copy2(abs_path, f"{abs_path}.awb")
                run_config += [f"{abs_path}.awb"]
            elif (
                tag == b"RIFF"
            ):  # This is wav files, means the file has already been converted
                continue
            else:
                print("UNKOWN FORMAT", abs_path, tag)
                continue
            if not os.path.isfile(dest_file):
                print("Running:", " ".join(run_config))
                if (e := Popen(run_config, stdout=DEVNULL, stderr=PIPE).stderr.read()) != b"":  # type: ignore
                    print(f"Creating {dest_file} failed befause of {e}")


if __name__ == "__main_:":
    convert("D:/madoka exedra/processed/media/assets/audio")
