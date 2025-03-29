import os
import shutil

readable_format = {
    "3c9Q": "media",
    "BGcT-ZTR3VbIOjTSED3D2Q": "opening song",
    "jdKuKFukRTY3WBKcvjCE_w": "player v player",
    "qS5N9gQUdF2MHq8cmuMMfQ": "union v union",
    "sZqhHAi3sirpi40RLFiclg": "witch backgrounds",
    "zN-qox17-wsy2Y3CD7wOAA": "gacha animations",
    "eS9W3BezrGrbpyvnoBonHQ": "video",
    "kfOi": "assets",
    "EWXF-evfuTQyaX7xDuKwDg": "felicia",
    "ont8m_mi4TcJeTZM2ktw3Q": "homura",
    "97V9Egw9L5PeaDXk-9EDoQ": "iroha",
    "Kl0t1Q6JyEhP6uvgWkBMkA": "kirika",
    "TziFO2jytzF0NEZxpG9pzg": "madoka",
    "hBcsybkbeOGXoKDkoAEUDw": "oriko",
    "3Ak-OuWdhyUribmel4QWRg": "ren",
    "hIhShGcvGrwJLHxOGn-DyQ": "sana",
    "XCeurzQBBsL3-_SEQH0zLw": "tsuruno",
    "-h80TA6qRYVJsyWjUQQAsA": "yachiyo",
    "OWi3MxQSPhXrmaJkgh4RNw": "sayaka",
    "uVm6ulDBrDhYA46u1X5Kow": "Mami",
    "ZppVaXXwyPTkrKimXRGbOA": "kyouko",
    "dUyFQnbD5gxiMxJ8tSkXNg": "background",
    "sVvJ4TvIc4R08iko7UvfGQ": "background",
    "WY0jzn69vWDdnweDyT-uig": "lighthouse",
    "obyhYXuzILmkGd5tjqGI4g": "audio",
    "kxUQlUAG63yur8Gd7SzLzg": "OST",
    "Fslzkho8beogRM5BTBtsng": "voice lines",
    "qH0WMaIQl6ncRtEc1m89Jw": "sound effects",
    # So I stop rereading the same folders:
    "p4Q2": "unknown encrpytedp4Q2",
    "UzJBZu0-e2shG0ervsum8Q": "unknown encrpytedUzJBZu0-e2shG0ervsum8Q",
    "HuEa77wqQGiPLdcRiUCbYA": "unknown encrpytedHuEa77wqQGiPLdcRiUCbYA",
    "YU-L": "unknown encrpytedYU-L",
    "SXdX": "unknown encrpytedSXdX",
}


def rename_file(file_path):
    for key, value in readable_format.items():
        file_path = file_path.replace(key, value)
    return file_path


def copy_files(src_dir, dst_dir):
    for root, _, files in os.walk(src_dir):
        for file_name in files:
            src_file_path = os.path.join(root, file_name)
            new_dst_file_path = rename_file(
                os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))
            )
            if not os.path.isfile(new_dst_file_path):
                print("CREATING NEW FILE: ", new_dst_file_path)
                os.makedirs(os.path.dirname(new_dst_file_path), exist_ok=True)
                shutil.copy2(src_file_path, new_dst_file_path)


if __name__ == "__main_:":
    copy_files(r"com.aniplex.magia.exedra.en/files/CYU6", "processed")
