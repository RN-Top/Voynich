#!/usr/bin/env python3
"""Where do the rare symbols land? (analyses/rare_symbols_prereg.md)

    python analyses/rare_symbols_test.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261002
N_PERMS = 10_000
ALPHA = 0.01
RARE = re.compile(r"@(\d+);")


def read_loci():
    rows = []
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.(\d+),(.)(\w)\w*>\s+(.*)", line)
        if not m:
            continue
        text = re.sub(r"<![^>]*>", "", m.group(5))
        rows.append({"folio": m.group(1), "n": int(m.group(2)), "start": m.group(3) == "@",
                     "type": m.group(4), "text": text})
    return rows


def main():
    loci = read_loci()
    section = parse_zl3b(CORPUS_PATH).groupby("folio")["section"].first().to_dict()
    pages = defaultdict(list)
    for r in loci:
        if r["type"] == "P":
            pages[r["folio"]].append((len(RARE.findall(r["text"])), r["start"]))
    pages = {p: v for p, v in pages.items() if len(v) >= 2}

    rng = np.random.default_rng(SEED)
    counts = [np.array([c for c, _ in v]) for v in pages.values()]
    starts = [np.array([s for _, s in v]) for v in pages.values()]
    s1_obs = int(sum(c[0] for c in counts))
    s2_obs = int(sum(c[s].sum() for c, s in zip(counts, starts)))
    s1_null, s2_null = np.zeros(N_PERMS), np.zeros(N_PERMS)
    for c, s in zip(counts, starts):
        s1_null += c[rng.integers(0, len(c), N_PERMS)]
        k = int(s.sum())
        if k:
            s2_null += np.array([c[rng.choice(len(c), k, replace=False)].sum() for _ in range(N_PERMS)])
    p1 = float((np.sum(s1_null >= s1_obs) + 1) / (N_PERMS + 1))
    p2 = float((np.sum(s2_null >= s2_obs) + 1) / (N_PERMS + 1))
    total = int(sum(c.sum() for c in counts))

    # Descriptive map
    info = defaultdict(lambda: {"n": 0, "pages": set(), "sections": Counter(), "types": Counter(),
                                "in_word": Counter(), "in_line": Counter()})
    names = {"P": "paragraph", "L": "label", "C": "ring", "R": "radial"}
    for r in loci:
        words = [w for w in re.split(r"[.,\s]+|<->", re.sub(r"<[^!][^>]*>|[{}\[\]]", "", r["text"])) if w]
        for wi, w in enumerate(words):
            for m in RARE.finditer(w):
                d = info[m.group(1)]
                d["n"] += 1
                d["pages"].add(r["folio"])
                d["sections"][section.get(r["folio"], "?")] += 1
                d["types"][names.get(r["type"], r["type"])] += 1
                rest = RARE.sub("", w)
                d["in_word"]["alone" if not rest else "start" if m.start() == 0 else
                             "end" if m.end() == len(w) else "middle"] += 1
                d["in_line"]["first word" if wi == 0 else "last word" if wi == len(words) - 1 else "other"] += 1

    L = ["# Where do the rare symbols land?", "",
         f"Pre-registration: `analyses/rare_symbols_prereg.md`. {N_PERMS:,} shuffles within page, seed {SEED}.", "",
         f"Paragraph text: {total} rare symbols on {len(pages)} pages.", "",
         "| Test | Rare symbols there | Chance | p | Result |", "|---|---:|---:|---:|---|",
         f"| S1 page-first lines | {s1_obs} | {s1_null.mean():.1f} | {p1:.3g} | {'PASS' if p1 < ALPHA else 'FAIL'} |",
         f"| S2 paragraph-first lines | {s2_obs} | {s2_null.mean():.1f} | {p2:.3g} | {'PASS' if p2 < ALPHA else 'FAIL'} |",
         "", "## What each symbol lands on (whole book, all writing types)", "",
         "| Symbol | Count | Pages | Sections | Writing type | In word | In line |", "|---|---:|---:|---|---|---|---|"]
    fmt = lambda c: ", ".join(f"{k} {v}" for k, v in c.most_common(3))
    for code, d in sorted(info.items(), key=lambda kv: -kv[1]["n"]):
        pg = sorted(d["pages"])
        L.append(f"| @{code} | {d['n']} | {len(pg)} ({', '.join(pg[:4])}{'…' if len(pg) > 4 else ''}) | {fmt(d['sections'])} | "
                 f"{fmt(d['types'])} | {fmt(d['in_word'])} | {fmt(d['in_line'])} |")
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "rare_symbols_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
