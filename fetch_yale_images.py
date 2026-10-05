#!/usr/bin/env python3
"""Download every page of Yale Beinecke MS 408 (the Voynich manuscript) at full resolution.

    python fetch_yale_images.py            # full size (~500 MB)
    python fetch_yale_images.py --width 1500

Images go to images/yale/ (git-ignored), named by page order and folio label, e.g. 003_1r.jpg.
An index (images/yale/index.csv) maps each file to its folio label and IIIF id.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.request
from pathlib import Path

MANIFEST = "https://collections.library.yale.edu/manifests/2002046"
OUT = Path(__file__).resolve().parent / "images" / "yale"


def get(url, timeout=120):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=0, help="max width in px (0 = full size)")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    m = json.loads(get(MANIFEST))
    size = "full" if not args.width else f"{args.width},"
    rows = []
    for i, c in enumerate(m["items"]):
        label = list(c["label"].values())[0][0]
        svc = c["items"][0]["items"][0]["body"]["service"][0]
        sid = svc.get("id") or svc.get("@id")
        name = f"{i:03d}_{re.sub(r'[^A-Za-z0-9]+', '_', label).strip('_')}.jpg"
        path = OUT / name
        if not path.exists():
            path.write_bytes(get(f"{sid}/full/{size}/0/default.jpg"))
        rows.append({"file": name, "label": label, "iiif": sid})
        print(f"{i + 1}/{len(m['items'])} {name}", flush=True)
    with open(OUT / "index.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["file", "label", "iiif"])
        w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
