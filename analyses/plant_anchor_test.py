#!/usr/bin/env python3
"""Are pharmacy plant-part labels plant names? (analyses/plant_anchor_prereg.md)

    python analyses/plant_anchor_test.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, VoynichParser, parse_zl3b  # noqa: E402

SEED = 20261002
N_DRAWS = 10_000
ALPHA = 0.01
MIN_LEN = 4


def label_words():
    out = []  # (pharmacy folio, word)
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.Lf>\s+(.*)", line)
        if not m:
            continue
        text = re.sub(r"<[^>]*>", "", m.group(2))
        for tok in re.split(r"[.,\s]+", text):
            w = VoynichParser.clean_token(tok)
            if len(w) >= MIN_LEN:
                out.append((m.group(1), w))
    return out


def main():
    labels = label_words()
    label_set = {w for _, w in labels}
    df = parse_zl3b(CORPUS_PATH)
    herb = df[(df.locus_type == "P") & (df.section == "Herbal") & (df.clean.str.len() > 0)]
    pages = defaultdict(Counter)
    for f, w in zip(herb.folio, herb.clean):
        pages[w][f] += 1
    count = {w: sum(c.values()) for w, c in pages.items()}
    conc = {w: max(c.values()) / count[w] for w, c in pages.items()}
    top_page = {w: c.most_common(1)[0][0] for w, c in pages.items()}

    qual = sorted(w for w in label_set if count.get(w, 0) >= 2)
    by_n = defaultdict(list)
    for w, n in count.items():
        if w not in label_set and n >= 2:
            by_n[n].append(w)
    avail = np.array(sorted(by_n))
    report = ["# Are the pharmacy plant-part labels plant names?", "",
              f"Pre-registration: `analyses/plant_anchor_prereg.md`. {len(labels)} label words "
              f"({len(label_set)} distinct, {MIN_LEN}+ letters) from the pharmacy plant-part labels; herbal text "
              f"{len(herb):,} words on {herb.folio.nunique()} pages.", "",
              f"- Label words that occur anywhere in herbal text: {sum(w in count for w in label_set)} of {len(label_set)}",
              f"- Label words seen 2+ times in herbal text (tested in A1): {len(qual)}", ""]
    if len(qual) < 10:
        report.append("**A1: too few to test.**")
    else:
        obs = float(np.mean([conc[w] for w in qual]))
        rng = np.random.default_rng(SEED)
        pools = []
        for w in qual:
            n = count[w]
            near = avail[np.argmin(np.abs(avail - n))]
            pools.append(np.array([conc[x] for x in by_n[near]]))
        null = np.mean([rng.choice(p, N_DRAWS) for p in pools], axis=0)
        p = float((np.sum(null >= obs) + 1) / (N_DRAWS + 1))
        report += ["## A1. Are label words concentrated like names?", "",
                   f"- Mean concentration of label words: **{obs:.3f}**",
                   f"- Same-frequency ordinary herbal words: {null.mean():.3f} (10,000 draws)",
                   f"- p = {p:.3g} → **{'PASS' if p < ALPHA else 'FAIL'}**", ""]
    cands = sorted((w for w in label_set if w in count and conc[w] >= 0.5),
                   key=lambda w: (-conc[w], -count[w]))
    src = defaultdict(set)
    for f, w in labels:
        src[w].add(f)
    report += ["## A2. Candidate anchors (descriptive, not a test)", "",
               "| Label word | On pharmacy page(s) | Herbal count | Concentration | Herbal page |",
               "|---|---|---:|---:|---|"]
    report += [f"| {w} | {', '.join(sorted(src[w]))} | {count[w]} | {conc[w]:.2f} | {top_page[w]} |" for w in cands[:20]]
    text = "\n".join(report) + "\n"
    (ROOT / "output" / "plant_anchor_report.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
