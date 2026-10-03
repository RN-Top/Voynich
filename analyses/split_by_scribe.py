#!/usr/bin/env python3
"""Write each scribe's text to its own file, in book order (ZL3b order).

Output: output/scribes/scribe_<n>.txt. Each page starts with a header line giving folio, section and Currier
language. Each locus is on its own line with its ZL3b locus id, and words are separated by spaces. Inline comments
are removed; uncertain readings keep the first option.

    python analyses/split_by_scribe.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, VoynichParser, parse_zl3b  # noqa: E402


def main():
    df = parse_zl3b(CORPUS_PATH)
    section = df.groupby("folio")["section"].first().to_dict()
    hand, lang, order = {}, {}, []
    out = defaultdict(list)
    cur = None
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.>]+)>\s+<!(.*)>", line)
        if m:
            cur = m.group(1)
            h = re.search(r"\$H=(\d)", m.group(2))
            lg = re.search(r"\$L=(\w)", m.group(2))
            hand[cur] = h.group(1) if h else "unknown"
            lang[cur] = lg.group(1) if lg else "?"
            out[hand[cur]].append(f"\n## {cur}  ({section.get(cur, '?')}, Currier {lang[cur]})")
            continue
        m = re.match(r"<(f[^.]+\.\d+),.(\w+)>\s+(.*)", line)
        if not m or cur is None:
            continue
        text = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", m.group(3))
        text = re.sub(r"<->", ".", text)
        text = re.sub(r"<[^>]*>", "", text)
        words = [w for w in (VoynichParser.clean_token(t) for t in re.split(r"[.,\s]+", text)) if w]
        if words:
            out[hand[cur]].append(f"{m.group(1):<12} {m.group(2):<3} {' '.join(words)}")
    d = ROOT / "output" / "scribes"
    d.mkdir(parents=True, exist_ok=True)
    for h, lines in sorted(out.items()):
        pages = sum(1 for l in lines if l.startswith("\n## "))
        head = (f"# Scribe {h}: {pages} pages, in book order\n"
                "# Source: ZL3b transliteration (data/ZL3b-n.txt); scribe tags $H after L. Fagin Davis (2020).\n"
                "# Columns: locus id, locus type (P paragraph, L label, C ring, R radial), words.\n")
        (d / f"scribe_{h}.txt").write_text(head + "\n".join(lines).lstrip("\n") + "\n", encoding="utf-8")
        print(f"scribe {h}: {pages} pages")


if __name__ == "__main__":
    main()
