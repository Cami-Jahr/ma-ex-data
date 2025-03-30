import json
from collections import defaultdict
import acb
import os


handled = set()


def find_and_remove_unique_values(data):
    found = True
    while found:
        seen = defaultdict(int)
        found = False
        for k, v in data.items():
            if len(v) == 1 and list(v)[0] not in handled:
                val = list(v)[0]
                handled.add(val)
                found = True
                for key in data:
                    if key != k:
                        data[key].discard(val)

        for vals in data.values():
            for x in vals:
                seen[x] += 1
        for x, i in seen.items():
            if i == 1:
                for k, v in data.items():
                    if x in v:
                        k = {x}
    return {k: sorted(v) for k, v in data.items()}


def find_single_possibilities():
    """THIS IS NOT FOUL PROOF, BUT AN EDUCATED GUESS"""
    with open("complementing_awbs.json", "r") as f:
        data = find_and_remove_unique_values(
            {k: set(v) for k, v in json.load(f).items()}
        )

    for k, v in data.items():
        if len(v) == 1:
            folder = f'{"\\".join(k.split("\\")[:-1])}\\{v[0][:-4]}_HCAs'
            if not os.path.isdir(folder):
                print(f"Extracting {k}")
                os.makedirs(folder, 0o755, exist_ok=True)
                acb.extract_acb(  # type: ignore
                    k,
                    folder,
                    f'{"\\".join(k.split("\\")[:-1])}\\{v[0]}',
                )

    with open("filtered_awbs.json", "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)
