import requests
import re
import json


def run():
    max_stats = {}
    max_iter = 200
    for i in range(max_iter):
        print(f"{i:>3}/{max_iter}", end="\r")
        text = requests.get(
            f"https://api-gl.mmme.pokelabo.jp/web/announce/body?announceMstId=1{i:03}&language=en-Latn&region=CA&timezoneoffset=0&standardtimezoneoffset=0"
        ).content
        chars = re.findall(rb"""<div class="style-name">\n *<div>(.*?)</div>""", text)
        stats = re.findall(rb"""<div class="value">\n *(\d+)\n *</div>""", text)
        for j in range(len(chars)):
            max_stats[chars[j].decode()] = [
                x.decode() for x in stats[4 * j : 4 * (j + 1)]
            ]

    with open("wiki/max_stats.json", "w", encoding="utf-8") as f:
        json.dump(max_stats, f, indent=4, ensure_ascii=False, sort_keys=True)
