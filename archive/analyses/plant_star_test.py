#!/usr/bin/env python3
"""Do plant-page opening words share unusual spellings with star labels? (analyses/plant_star_prereg.md)

    python analyses/plant_star_test.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261002
N_DRAWS = 10_000
ALPHA = 0.01
RARE_TYPES = 20
OTHER = {"L0", "La", "Lc", "Lf", "Ln", "Lp", "Lt", "Lx", "Lz"}


def words_of(text: str):
    text = re.sub(r"<![^>]*>", "", text)
    text = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", text)
    text = re.sub(r"<->", ".", text)
    text = re.sub(r"<[^>]*>|[{}'*?]", "", text)
    text = re.sub(r"@(\d+);", lambda m: chr(0xE000 + int(m.group(1))), text)
    return [w for w in re.split(r"[.,\s]+", text) if w]


def chunks(w: str):
    s = "^" + w + "$"
    return {s[i:i + 3] for i in range(len(s) - 2)}


def show(w: str):
    return re.sub(r"[-]", lambda m: f"@{ord(m.group(0)) - 0xE000}", w)


def main():
    section = parse_zl3b(CORPUS_PATH).groupby("folio")["section"].first().to_dict()
    all_types, star, other, opening = set(), [], [], {}
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.(\d+),.(\w+)>\s+(.*)", line)
        if not m:
            continue
        folio, code, ws = m.group(1), m.group(3), words_of(m.group(4))
        all_types.update(ws)
        if code == "Ls":
            star += [(folio, w) for w in ws]
        elif code in OTHER:
            other += [(folio, w) for w in ws]
        elif code.startswith("P") and section.get(folio) == "Herbal" and folio not in opening and ws:
            opening[folio] = ws[0]
    freq = defaultdict(int)
    for w in all_types:
        for c in chunks(w):
            freq[c] += 1
    rare = lambda w: {c for c in chunks(w) if freq[c] < RARE_TYPES}
    open_rare = {f: rare(w) for f, w in opening.items()}

    def score(label_words):
        pool = set().union(*(rare(w) for _, w in label_words)) if label_words else set()
        return sum(bool(r & pool) for r in open_rare.values())

    obs = score(star)
    rng = np.random.default_rng(SEED)
    null = np.array([score([other[i] for i in rng.choice(len(other), len(star), replace=False)])
                     for _ in range(N_DRAWS)])
    p = float((np.sum(null >= obs) + 1) / (N_DRAWS + 1))
    matches = []
    for f, w in opening.items():
        for sf, sw in star:
            shared = open_rare[f] & rare(sw)
            if shared:
                matches.append((f, show(w), sf, show(sw), ", ".join(sorted(show(c) for c in shared))))
    L = ["# Do plant-page opening words share unusual spellings with star labels?", "",
         f"Pre-registration: `analyses/plant_star_prereg.md`. {len(opening)} herbal opening words; {len(star)} star-label "
         f"words; {len(other)} other label words; {N_DRAWS:,} draws, seed {SEED}.", "",
         f"- Opening words sharing an unusual chunk with star labels: **{obs}**",
         f"- Same number of words drawn from other labels: {null.mean():.1f} on average",
         f"- p = {p:.3g} → **{'SUPPORTED' if p < ALPHA else 'NOT SUPPORTED'}**", "",
         "## Matches (descriptive)", "", "| Plant page | Opening word | Star page | Star label | Shared chunk(s) |",
         "|---|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in matches]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "plant_star_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
