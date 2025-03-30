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
        print("Running:", " ".join(run_config))
        if (e := Popen(run_config, stdout=DEVNULL, stderr=PIPE).stderr.read()) != b"":  # type: ignore
            print(f"Creating {dst_file} failed because of {e}")


def convert(src_dir, mini_dst_dir, full_dst_dir):
    """
    Drag the video folder into VGMTOOLBOX before running this,
    haven't done the usm -> adx + m2v conversion in CLI yet
    TODO: Remove manual step
    """
    for root, _, files in os.walk(src_dir):
        di = defaultdict(list)
        for f in files:
            di[f.split("_")[0]].append(f)
        for file_hash in di.values():
            run_config = ["ffmpeg", "-y"]
            for file in [x for x in file_hash if "." in x]:
                abs_path = os.path.join(root, file)
                run_config += ["-i", abs_path]
            file_name_root = next(x for x in file_hash if "." not in x)

            create(
                root.replace(src_dir, mini_dst_dir),
                file_name_root,
                run_config.copy(),
                True,
            )
            create(
                root.replace(src_dir, full_dst_dir),
                file_name_root,
                run_config.copy(),
                False,
            )


if __name__ == "__main_:":
    convert(
        r"D:\madoka-exedra\processed\media\assets\video",
        r"D:\madoka-exedra\full\media\assets\video",
        r"D:\madoka-exedra\mini\media\assets\video",
    )
