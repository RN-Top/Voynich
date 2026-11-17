#!/usr/bin/env python3
"""Re-run earlier leads with page types taken from the integrated file
(analyses/rerun_integrated_prereg.md).

    python3 analyses/rerun_with_integrated.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = ["plant_star_test", "chains_test", "ground_test"]
DRAWN = {"H": "Herbal", "A": "Astronomical/Zodiac", "Z": "Astronomical/Zodiac", "B": "Biological",
         "C": "Cosmological", "P": "Pharmaceutical", "S": "Stars/Recipes", "T": "Text only"}


def corpus_from_integrated(path):
    """Write the integrated file back out as an IVTFF transcription (same lines, same order)."""
    d = json.load(open(ROOT / "voynich_integrated.json", encoding="utf-8"))
    with open(path, "w", encoding="utf-8") as fh:
        for f in d["folios"]:
            v = " ".join(f"${k}={x}" for k, x in f["page_variables"].items())
            fh.write(f"<{f['folio_id']}>      <! {v}>\n")
            for ln in f["text_lines"]:
                fh.write(f"<{f['folio_id']}.{ln['line']},{ln['locus']}>      {ln['text']}\n")
    return {f["folio_id"]: DRAWN.get(f["illustration"]["type_code"], "General") for f in d["folios"]}


def child(mode, test, corpus, sections_json):
    """Run one test with parser patched for the chosen input."""
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "analyses"))
    import parser as P
    P.CORPUS_PATH = corpus
    P.ensure_full_corpus = lambda path=corpus: path
    if mode == "integrated":
        sections = json.load(open(sections_json))
        P.infer_section = lambda folio: sections.get(str(folio), "General")
    mod = __import__(test)
    mod.main()


def main():
    if len(sys.argv) == 5:
        return child(*sys.argv[1:])
    (ROOT / "output").mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    corpus = tmp / "integrated_as_ivtff.txt"
    sections = corpus_from_integrated(corpus)
    json.dump(sections, open(tmp / "sections.json", "w"))
    # Same lines? (the text must be identical; only page types differ)
    orig = [l.rstrip("\n") for l in open(ROOT / "Data" / "Zl3b-n.txt", encoding="utf-8") if re.match(r"<f[^.>]+\.\d+,", l)]
    new = [l.rstrip("\n") for l in open(corpus, encoding="utf-8") if re.match(r"<f[^.>]+\.\d+,", l)]
    norm = lambda l: re.sub(r"\s+", " ", l)
    same_text = [norm(a) for a in orig] == [norm(b) for b in new]
    print("text lines identical to ZL3b:", same_text, len(orig))
    for test in TESTS:
        name = test.replace("_test", "")
        for mode, src in (("original", str(ROOT / "Data" / "Zl3b-n.txt")), ("integrated", str(corpus))):
            subprocess.run([sys.executable, __file__, mode, test, src, str(tmp / "sections.json")],
                           check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
            shutil.move(ROOT / "output" / f"{name}_report.md", ROOT / "output" / f"{name}_report_{mode}.md")
            print("done", test, mode)
    moved = {}
    import parser as P
    for f in sections:
        old = P.infer_section(f)
        if old != sections[f]:
            moved[f] = (old, sections[f])
    with open(tmp / "moved.json", "w") as fh:
        json.dump(moved, fh, indent=1)
    print("pages whose type changes:", len(moved))
    shutil.copy(tmp / "moved.json", ROOT / "output" / "rerun_integrated_page_types_changed.json")


if __name__ == "__main__":
    main()
