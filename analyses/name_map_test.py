#!/usr/bin/env python3
"""A map of name links between sections (analyses/name_map_prereg.md)

    python analyses/name_map_test.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402
from plant_star_test import RARE_TYPES, chunks, words_of  # noqa: E402

SEED = 20261002
N_DRAWS = 2000
GROUPS = {"Ls": "stars", "Lz": "zodiac figures", "Ln": "bathing figures", "Lt": "pools/tubes",
          "Lc": "jars", "Lf": "plant parts", "L0": "other", "La": "other", "Lp": "other", "Lx": "other"}


def main():
    section = parse_zl3b(CORPUS_PATH).groupby("folio")["section"].first().to_dict()
    all_types, labels, openings = set(), defaultdict(list), defaultdict(list)
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.(\d+),(.)(\w+)>\s+(.*)", line)
        if not m:
            continue
        folio, start, code, ws = m.group(1), m.group(3) == "@", m.group(4), words_of(m.group(5))
        all_types.update(ws)
        if code in GROUPS:
            labels[GROUPS[code]] += ws
        elif code.startswith("P") and start and ws:
            openings[section.get(folio, "?")].append(ws[0])
    freq = defaultdict(int)
    for w in all_types:
        for c in chunks(w):
            freq[c] += 1
    rare = lambda w: frozenset(c for c in chunks(w) if freq[c] < RARE_TYPES)
    lab_rare = {g: [rare(w) for w in ws] for g, ws in labels.items()}
    sections = [s for s, ws in openings.items() if len(ws) >= 10]
    cells = [(s, g) for s in sections for g in labels]
    alpha = 0.01 / len(cells)
    rng = np.random.default_rng(SEED)
    rows = []
    for s, g in cells:
        op = [rare(w) for w in openings[s]]
        score = lambda pool: sum(bool(r & pool) for r in op)
        obs = score(frozenset().union(*lab_rare[g]))
        others = [r for h, rs in lab_rare.items() if h != g for r in rs]
        k = len(lab_rare[g])
        null = np.array([score(frozenset().union(*(others[i] for i in rng.choice(len(others), k, replace=False))))
                         for _ in range(N_DRAWS)])
        p = float((np.sum(null >= obs) + 1) / (N_DRAWS + 1))
        rows.append((s, g, len(op), k, obs, float(null.mean()), p))
    passed = [r for r in rows if r[6] < alpha]
    new = [r for r in passed if not (r[0] == "Herbal" and r[1] == "stars")]
    L = ["# A map of name links between sections", "",
         f"Pre-registration: `analyses/name_map_prereg.md`. {len(cells)} cells, Bonferroni threshold p < {alpha:.5f}; "
         f"{N_DRAWS:,} draws per cell, seed {SEED}.", "",
         "| Opening words from | Label group | Openings | Label words | Shared | Expected | Ratio | p | Link? |",
         "|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for s, g, n, k, o, e, p in sorted(rows, key=lambda r: r[6]):
        L.append(f"| {s} | {g} | {n} | {k} | {o} | {e:.1f} | {o / e if e else float('nan'):.2f} | {p:.3g} | "
                 f"{'**yes**' if p < alpha else ''} |")
    L += ["", f"**Cells passing:** {len(passed)} ({len(new)} besides Herbal × stars). "
          f"**Map wider than one link: {'YES' if new else 'NO'}.**"]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "name_map_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
