from subprocess import PIPE, Popen, DEVNULL
from collections import defaultdict
import os


def create(dst_root, file_name_root, run_config, is_mini):
    os.makedirs(dst_root, 0o755, exist_ok=True)
    dst_file = os.path.join(dst_root, file_name_root) + (".webm" if is_mini else ".mp4")
    if not os.path.isfile(dst_file):
        if is_mini:
            run_config += [
                "-c:v",
                "libvpx-vp9",
                "-crf",
                "30",
                "-b:v",
                "0",
                "-c:a",
                "libopus",
                "-b:a",
                "128k",
            ]
        run_config += [
            dst_file,
        ]
        if (e := Popen(run_config, stdout=DEVNULL, stderr=PIPE).stderr.read()) != b"":  # type: ignore
            print(f"ERROR: Creating {dst_file} failed because of {e}")


def convert(src_dir, dst_dir, is_mini: bool = False):
    """
    Drag the video folder into VGMTOOLBOX before running this,
    haven't done the usm -> adx + m2v conversion in CLI yet
    TODO: Remove manual step
    """
    for root, _, files in os.walk(src_dir):
        di = defaultdict(list)
        for f in files:
            if "adx" in f or "m2v" in f:
                di[f.rsplit("_", 1)[0]].append(f)

        for file_name, composite_files in di.items():
            run_config = ["ffmpeg", "-y"]
            for file in composite_files:
                abs_path = os.path.join(root, file)
                run_config += ["-i", abs_path]

            create(
                root.replace(src_dir, dst_dir),
                file_name,
                run_config.copy(),
                is_mini,
            )


def minimize(src_dir, dst_dir):
    convert(src_dir, dst_dir, True)


if __name__ == "__main__":
    convert(r"processed\gallery\kfOi\CriMovie", r"full\gallery\kfOi\CriMovie")
    minimize(r"processed\gallery\kfOi\CriMovie", r"mini\gallery\kfOi\CriMovie")
