#!/usr/bin/env python3
"""
Build voynich_integrated.json: the whole manuscript as one file, page by page.

For every page in the ZL3b transcription (Data/Zl3b-n.txt) the output holds,
together in one entry:
  - the page's place in the book (order, quire, page in quire)
  - what is drawn on it (illustration type from ZL3b, plus the transcriber's
    own notes on the drawings)
  - the Yale Beinecke page image(s) it appears on (IIIF links to the
    full-resolution scans of MS 408)
  - its writing, split by where it sits relative to the drawings:
    paragraphs, labels next to drawings, text in circles, text along radii,
    with each label's position and the places where a drawing cuts a line

Image list: Data/yale_ms408_images.csv (made from Yale's IIIF manifest,
https://collections.library.yale.edu/manifests/2002046).
Run with --refresh-images to download the manifest again and rewrite it.

    python3 build_integrated.py
    python3 build_integrated.py --refresh-images
"""

import argparse
import csv
import json
import re
import sys
import urllib.request
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVA_FILE = ROOT / "Data" / "Zl3b-n.txt"
IMAGE_CSV = ROOT / "Data" / "yale_ms408_images.csv"
OUT_FILE = ROOT / "voynich_integrated.json"
MANIFEST = "https://collections.library.yale.edu/manifests/2002046"
CATALOG = "https://collections.library.yale.edu/catalog/2002046"

# ZL3b page variable $I (illustration type)
ILLUSTRATION = {
    "T": "text only",
    "H": "herbal",
    "A": "astronomical",
    "C": "cosmological",
    "Z": "zodiac",
    "B": "biological",
    "P": "pharmaceutical",
    "S": "stars (recipes)",
}

# ZL3b locus type (first letter after the +,@,*,= etc.)
UNIT = {
    "P": "paragraph",
    "L": "label",
    "C": "circle",
    "R": "radius",
}

# Foldouts: Yale photographs several panels in one image, so these are mapped by
# hand. "checked" = looked at the Yale image and matched it to ZL3b's description.
# "page order" = Yale and ZL3b list the panels in the same order (true for every
# foldout that was checked); not looked at panel by panel.
FOLDOUTS = {
    "f67r1": (["67r"], "checked"), "f67r2": (["67r"], "checked"),
    "f67v2": (["67v"], "page order"), "f67v1": (["67v"], "page order"),
    "f68r1": (["68r"], "page order"), "f68r2": (["68r"], "page order"),
    "f68r3": (["68r"], "page order"),
    "f68v3": (["68v"], "page order"), "f68v2": (["68v"], "page order"),
    "f68v1": (["68v"], "page order"),
    "f69v": (["69v and 70r"], "page order"), "f70r1": (["69v and 70r"], "page order"),
    "f70r2": (["69v and 70r"], "page order"),
    "f70v2": (["70v (part)#1"], "checked"),  # Pisces, two fish
    "f70v1": (["70v (part)#2"], "checked"),  # Aries, "abril"
    "f71v": (["71v and 72r"], "page order"), "f72r1": (["71v and 72r"], "page order"),
    "f72r2": (["71v and 72r"], "page order"), "f72r3": (["71v and 72r"], "page order"),
    "f72v3": (["72v (part)#1"], "checked"),  # Leo, left circle of the wide image
    "f72v2": (["72v (part)#1"], "checked"),  # Virgo, right circle
    "f72v1": (["72v (part)#2"], "checked"),  # Libra
    "f85r1": (["85r (part) (part of 85-86 foldout)"], "checked"),  # text only
    "f85r2": (["85r (part) 86v (part) (part of 85-86 foldout)"], "checked"),  # four figures
    "fRos": (["85v and 86r (foldout)"], "checked"),  # the nine rosettes
    "f86v4": (["85r (part) 86v (part) (part of 85-86 foldout)"], "checked"),  # moon, rings
    "f86v6": (["85r (part) 86v (part) (part of 85-86 foldout)"], "checked"),  # text
    "f86v5": (["86v (part) (part of 85-86 foldout)"], "checked"),  # text
    "f86v3": (["86v (part) (part of 85-86 foldout)"], "checked"),  # circle in 3, figures
    "f88v": (["88v and 89r"], "page order"), "f89r1": (["88v and 89r"], "page order"),
    "f89r2": (["88v and 89r"], "page order"),
    "f89v2": (["89v (part)"], "checked"),  # 3 rows of plants
    "f89v1": (["89v (part) and 90r"], "checked"),  # 2 rows of plants
    "f90r1": (["89v (part) and 90r"], "checked"),
    "f90r2": (["89v (part) and 90r"], "checked"),
    # Yale labels this image "90r", but f90r1/f90r2 are both in the image above and
    # the fern-like leaves match ZL3b's note for f90v2 ("leaves of Osmunda regalis").
    "f90v2": (["90r"], "checked, Yale label differs"),
    "f90v1": (["90v (part)"], "checked"),
    "f94v": (["94v and 95r"], "page order"), "f95r1": (["94v and 95r"], "page order"),
    "f95r2": (["94v and 95r"], "page order"),
    "f95v2": (["95v (part)"], "page order"), "f95v1": (["95v"], "page order"),
    "f100v": (["100v and 101r"], "page order"), "f101r": (["100v and 101r"], "page order"),
    "f101v": (["101v (part)", "101v (part) and 102r"], "page order"),
    "f102r1": (["101v (part) and 102r"], "page order"),
    "f102r2": (["101v (part) and 102r"], "page order"),
    "f102v2": (["102v (part)#1"], "page order"), "f102v1": (["102v (part)#2"], "page order"),
}


def refresh_images():
    with urllib.request.urlopen(MANIFEST, timeout=120) as r:
        m = json.loads(r.read())
    with open(IMAGE_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["image_number", "label", "iiif_id", "width", "height"])
        for i, c in enumerate(m["items"], 1):
            label = list(c["label"].values())[0][0]
            svc = c["items"][0]["items"][0]["body"]["service"][0]
            w.writerow([i, label, svc.get("id") or svc.get("@id"), c["width"], c["height"]])
    print(f"Wrote {IMAGE_CSV.name} ({len(m['items'])} images)")


def load_images():
    """Return {key: image dict}. Repeated labels get #1, #2 in manifest order."""
    rows = list(csv.DictReader(open(IMAGE_CSV, newline="", encoding="utf-8")))
    seen = Counter(r["label"] for r in rows)
    count = Counter()
    images = {}
    for r in rows:
        key = r["label"]
        if seen[key] > 1:
            count[key] += 1
            key = f"{key}#{count[key]}"
        sid = r["iiif_id"]
        images[key] = {
            "yale_image_number": int(r["image_number"]),
            "yale_label": r["label"],
            "iiif_id": sid,
            "full_res_url": f"{sid}/full/full/0/default.jpg",
            "preview_url": f"{sid}/full/800,/0/default.jpg",
            "width_px": int(r["width"]),
            "height_px": int(r["height"]),
        }
    return images, rows


def images_for(folio_id, images):
    if folio_id in FOLDOUTS:
        keys, basis = FOLDOUTS[folio_id]
        scope = "foldout panel (the photo may also show neighbouring panels)"
    else:
        keys, basis, scope = [folio_id[1:]], "Yale label", "whole page"
    found = [images[k] for k in keys if k in images]
    if len(found) != len(keys):
        missing = [k for k in keys if k not in images]
        raise SystemExit(f"ERROR: no Yale image labelled {missing} for {folio_id}")
    return found, basis, scope


# ---------- text ----------

def clean_words(text):
    """EVA line -> list of words. Keeps the Voynich characters, drops markup.

    - <!...> comments, <%> paragraph start, <$> paragraph end: removed
    - <-> and <~> (drawing or gap cutting the line): word break
    - [a:b] (transcriber unsure between readings): first reading kept
    - {..} (ligature or odd shape): brackets removed, letters kept
    - @NNN; (rare character code): kept as is
    - . and , : word breaks ( , = uncertain space, kept as a break as before)
    """
    t = re.sub(r"<![^>]*>", "", text)
    t = re.sub(r"<[%$]>", "", t)
    t = re.sub(r"<[-~]>", ".", t)
    t = re.sub(r"<[^>]*>", "", t)  # any other inline tag
    t = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", t)
    t = re.sub(r"\{([^}]*)\}", lambda m: m.group(1).replace("'", ""), t)
    return [w for w in re.split(r"[.,\s]+", t) if w]


def parse_locus(locus):
    # e.g. "@P0", "+Lf", "=Pt", "*Cc", "@Ri"
    m = re.match(r"([@+*=&~])([A-Z])(\w*)", locus)
    if not m:
        return {"unit": "other", "unit_code": locus, "starts_new_unit": False}
    mark, kind, sub = m.groups()
    return {
        "unit": UNIT.get(kind, kind),
        "unit_code": kind + sub,
        "starts_new_unit": mark in "@*",
        "ends_unit": mark == "=",
    }


def parse_eva():
    pages = OrderedDict()
    current = None
    pending = []
    for raw in open(EVA_FILE, encoding="utf-8"):
        line = raw.rstrip("\n")
        head = re.match(r"<(f[A-Za-z0-9]+)>\s*<!(.*)>", line)
        if head:
            fid = head.group(1)
            vars_ = dict(re.findall(r"\$(\w)=(\w*)", head.group(2)))
            pages[fid] = {"vars": vars_, "notes": [], "lines": []}
            current = fid
            pending = []
            continue
        body = re.match(r"<(f[A-Za-z0-9]+)\.(\d+),([^>]+)>\s*(.*)", line)
        if body:
            fid, num, locus, text = body.groups()
            if fid not in pages:
                raise SystemExit(f"ERROR: line for {fid} before its page header")
            pos = re.match(r"\s*<!([^>@]*)>", text)  # leading position note, e.g. <!2:11> <!09:00> <!N>
            pages[fid]["lines"].append((int(num), locus, text, pos.group(1).strip() if pos else None,
                                        pending))
            pending = []
            continue
        if line.startswith("#") and current:
            note = line.lstrip("#").strip()
            if note:
                pages[current]["notes"].append(note)
                if pages[current]["lines"]:  # a note inside the page describes the lines after it
                    pending.append(note)
    return pages


def build():
    if not EVA_FILE.exists():
        raise SystemExit(f"ERROR: {EVA_FILE} not found")
    images, image_rows = load_images()
    pages = parse_eva()

    folios = []
    used_images = set()
    total_words = 0
    vocab = Counter()
    stats = Counter()

    for order, (fid, p) in enumerate(pages.items(), 1):
        v = p["vars"]
        imgs, basis, scope = images_for(fid, images)
        used_images.update(i["yale_image_number"] for i in imgs)

        text_lines, units = [], []
        for num, locus, text, position, line_notes in p["lines"]:
            info = parse_locus(locus)
            words = clean_words(text)
            total_words += len(words)
            vocab.update(words)
            entry = {
                "line": num,
                "locus": locus,
                "unit": info["unit"],
                "unit_code": info["unit_code"],
                "position": position,
                "text": text,
                "words": words,
                "word_count": len(words),
                "drawing_breaks": text.count("<->"),
            }
            if line_notes:
                entry["notes_before"] = line_notes
            text_lines.append(entry)
            if info["starts_new_unit"] or not units or units[-1]["unit"] != info["unit"]:
                units.append({"unit": info["unit"], "unit_code": info["unit_code"],
                              "position": position, "notes": line_notes, "lines": [], "words": []})
            units[-1]["lines"].append(num)
            units[-1]["words"].extend(words)

        by_unit = Counter()
        for ln in text_lines:
            by_unit[ln["unit"]] += ln["word_count"]
        labels = [{"line": ln["line"], "label_type": ln["unit_code"], "position": ln["position"],
                   "words": ln["words"]} for ln in text_lines if ln["unit"] == "label"]

        ill_code = v.get("I", "")
        is_foldout = fid in FOLDOUTS
        stats["foldout" if is_foldout else "integrated"] += 1
        stats[f"ill_{ill_code}"] += 1

        folios.append({
            # --- kept from the old format so existing scripts still work ---
            "folio_id": fid,
            "type": "foldout" if is_foldout else "integrated",
            "image_paths": [i["full_res_url"] for i in imgs],
            "text_lines": text_lines,
            "has_text": bool(text_lines),
            "has_image": bool(imgs),
            "word_count": sum(ln["word_count"] for ln in text_lines),
            # --- where the page sits in the book ---
            "order": order,
            "quire": v.get("Q"),
            "page_in_quire": v.get("P"),
            "currier_language": v.get("L"),
            "currier_hand": v.get("H"),
            "page_variables": v,
            # --- the drawing ---
            "illustration": {
                "type_code": ill_code,
                "type": ILLUSTRATION.get(ill_code, ill_code),
                "transcriber_notes": p["notes"],
            },
            # --- the photograph ---
            "images": imgs,
            "image_scope": scope,
            "image_match": basis,
            # --- the writing, grouped the way it sits on the page ---
            "text_units": units,
            "labels": labels,
            "words_by_unit": dict(by_unit),
            "drawing_breaks": sum(ln["drawing_breaks"] for ln in text_lines),
        })

    unused = [r["label"] for r in image_rows if int(r["image_number"]) not in used_images]
    data = {
        "metadata": {
            "description": ("Voynich Manuscript (Yale Beinecke MS 408) as one file: every page "
                            "of the ZL3b transcription in book order, with its text, labels, "
                            "drawing type and notes, and its Yale page image(s)."),
            "text_source": "ZL3b transcription (Data/Zl3b-n.txt), version 3b of 13/05/2025",
            "image_source": f"Yale Beinecke IIIF manifest {MANIFEST} (catalog {CATALOG})",
            "folios_total": len(folios),
            "integrated_count": stats["integrated"],
            "foldout_count": stats["foldout"],
            "text_only_count": 0,
            "image_only_count": 0,
            "unmatched_count": 0,
            "pages_by_illustration": {ILLUSTRATION.get(k[4:], k[4:]): n
                                      for k, n in sorted(stats.items()) if k.startswith("ill_")},
            "total_words": total_words,
            "unique_words": len(vocab),
            "total_lines": sum(len(f["text_lines"]) for f in folios),
            "labels_total": sum(len(f["labels"]) for f in folios),
            "drawing_breaks_total": sum(f["drawing_breaks"] for f in folios),
            "yale_images_not_tied_to_text": unused,
            "how_to_read": {
                "unit": "paragraph = body text; label = word(s) next to a drawing; "
                        "circle = text written round a ring; radius = text along a spoke",
                "position": "ZL3b position note for the line, e.g. clock position '09:00', "
                            "compass 'N', or rosette 'circle:locus' like '2:11'",
                "drawing_breaks": "places where a drawing cuts through a line of text (<-> in ZL3b)",
                "image_match": "how the page was tied to its photo: 'Yale label', 'checked' "
                               "(looked at), or 'page order' (foldout panels in the same order)",
            },
        },
        "folios": folios,
    }
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh-images", action="store_true",
                    help="download Yale's manifest again before building")
    args = ap.parse_args()
    if args.refresh_images or not IMAGE_CSV.exists():
        refresh_images()

    data = build()
    m = data["metadata"]

    # Checks: every page has text and a photo; nothing in the transcription is skipped.
    eva_lines = sum(1 for l in open(EVA_FILE, encoding="utf-8") if re.match(r"<f[A-Za-z0-9]+\.\d+,", l))
    problems = []
    if m["total_lines"] != eva_lines:
        problems.append(f"lines in file {m['total_lines']} != lines in transcription {eva_lines}")
    for f in data["folios"]:
        if not f["has_text"]:
            problems.append(f"{f['folio_id']} has no text")
        if not f["has_image"]:
            problems.append(f"{f['folio_id']} has no image")
    if problems:
        print("\n".join(problems))
        sys.exit(1)

    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)

    print(f"Saved {OUT_FILE.name}")
    print(f"  pages:              {m['folios_total']} ({m['foldout_count']} foldout panels)")
    print(f"  pages with photo:   {m['folios_total']} / {m['folios_total']}")
    print(f"  lines:              {m['total_lines']} (all {eva_lines} in the transcription)")
    print(f"  words:              {m['total_words']} ({m['unique_words']} different)")
    print(f"  labels:             {m['labels_total']}")
    print(f"  drawing breaks:     {m['drawing_breaks_total']}")
    print(f"  by drawing type:    {m['pages_by_illustration']}")
    print(f"  Yale images with no transcribed text: {m['yale_images_not_tied_to_text']}")


if __name__ == "__main__":
    main()
