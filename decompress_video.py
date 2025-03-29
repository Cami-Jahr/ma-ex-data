from subprocess import PIPE, Popen, DEVNULL
from collections import defaultdict
import os


def convert(src_dir):
    """
    Drag the video folder into VGMTOOLBOX before running this,
    haven't done the usm -> adx + m2v convertion in CLI yet
    TODO: Remove manual step
    """
    for root, _, files in os.walk(src_dir):
        di = defaultdict(list)
        for f in files:
            if ".mp4" not in f:
                di[f.split("_")[0]].append(f)
        for file_hash in di.values():
            run_config = ["ffmpeg", "-y"]
            for file in [x for x in file_hash if "." in x]:
                abs_path = os.path.join(root, file)
                run_config += ["-i", abs_path]
            dest_file = (
                os.path.join(root, next(x for x in file_hash if "." not in x)) + ".mp4"
            )

            if not os.path.isfile(dest_file):
                run_config += [dest_file]
                print("Running:", " ".join(run_config))
                if (e := Popen(run_config, stdout=DEVNULL, stderr=PIPE).stderr.read()) != b"":  # type: ignore
                    print(f"Creating {dest_file} failed befause of {e}")


if __name__ == "__main_:":
    convert("D:/madoka exedra/processed/media/assets/video")
