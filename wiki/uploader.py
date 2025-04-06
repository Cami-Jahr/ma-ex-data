import os
import re
from wiki_bot import wikibot


def upload():
    for root, _, files in os.walk(r"full\gallery\library\Sprite"):
        for file in files:
            if re.search(r"\d{8}_original.png", file):
                print(file)
                # wikibot.upload_image(os.path.join(root, file))

    for root, _, files in os.walk("wiki"):
        for file in files:
            name, ext = file.rsplit(".", 1)
            if ext == "wt" and name != "test":
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    wikibot.upload(name, f.read())


if __name__ == "__main__":
    upload()
