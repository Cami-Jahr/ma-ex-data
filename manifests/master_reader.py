"""Fetched Master straight from mitmproxy, unsure why get_all_manifests fails for just that one"""

import os
import sys

csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)
import helpers
import json

with open("manifests/enmaster", "rb") as f:
    with open(
        "manifests/res/get_resource_master_data_mst_listEN.json", "w", encoding="utf-8"
    ) as g:
        json.dump(helpers.decrypt_data(f.read()), g, ensure_ascii=False, indent=4)

with open("manifests/jpmaster", "rb") as f:
    with open(
        "manifests/res/get_resource_master_data_mst_listJP.json", "w", encoding="utf-8"
    ) as g:
        json.dump(helpers.decrypt_data(f.read()), g, ensure_ascii=False, indent=4)
