#!/usr/bin/env python3
"""Correspondence chains: herb -> star -> body (analyses/chains_prereg.md)

    python analyses/chains_test.py
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
from plant_star_test import RARE_TYPES, chunks, show, words_of  # noqa: E402

SEED = 20261005
N_DRAWS = 20_000
ALPHA = 0.05
BODY, REMEDY, STAR = {"Ln", "Lt", "Lz"}, {"Lc", "Lf"}, {"Ls"}
OTHER = {"L0", "La", "Lp", "Lx"}


def main():
    section = parse_zl3b(CORPUS_PATH).groupby("folio")["section"].first().to_dict()
    all_types, H, lab = set(), [], defaultdict(list)
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.(\d+),(.)(\w+)>\s+(.*)", line)
        if not m:
            continue
        folio, start, code, ws = m.group(1), m.group(3) == "@", m.group(4), words_of(m.group(5))
        all_types.update(ws)
        if code.startswith("L"):
            lab[code] += [(w, folio) for w in ws]
        elif code.startswith("P") and start and ws and section.get(folio) == "Herbal":
            H.append((ws[0], folio))
    freq = defaultdict(int)
    for w in all_types:
        for c in chunks(w):
            freq[c] += 1
    rare = lambda w: {c for c in chunks(w) if freq[c] < RARE_TYPES}
    pool = lambda codes: [x for c in codes for x in lab.get(c, [])]
    S, B, R, O = pool(STAR), pool(BODY), pool(REMEDY), pool(OTHER)
    cset = lambda ws: set().union(*(rare(w) for w, _ in ws)) if ws else set()
    cH, cS = cset(H), cset(S)
    hs = cH & cS
    rng = np.random.default_rng(SEED)

    def test(target, null_pool):
        obs = len(hs & cset(target))
        null = np.empty(N_DRAWS)
        pr = [rare(w) for w, _ in null_pool]
        for t in range(N_DRAWS):
            idx = rng.choice(len(pr), len(target), replace=False)
            null[t] = len(hs & set().union(*(pr[i] for i in idx)))
        return obs, float(null.mean()), float((np.sum(null >= obs) + 1) / (N_DRAWS + 1))

    o1, e1, p1 = test(B, R + O)
    o2, e2, p2 = test(R, B + O)
    # four-way: B and R jointly replaced from the other labels
    obs4 = len(hs & cset(B) & cset(R))
    pr = [rare(w) for w, _ in O]
    null4 = np.empty(N_DRAWS)
    for t in range(N_DRAWS):
        if len(pr) >= len(B) + len(R):
            idx = rng.permutation(len(pr))
        else:
            idx = rng.choice(len(pr), len(B) + len(R), replace=True)
        b = set().union(*(pr[i] for i in idx[:len(B)]))
        r = set().union(*(pr[i] for i in idx[len(B):len(B) + len(R)]))
        null4[t] = len(hs & b & r)
    p4 = float((np.sum(null4 >= obs4) + 1) / (N_DRAWS + 1))

    def ex(ws, c):
        hits = [f"{show(w)} ({f})" for w, f in ws if c in rare(w)]
        return ", ".join(hits[:3]) + (" …" if len(hits) > 3 else "")

    v = lambda p: "SUPPORTED" if p < ALPHA else "NOT SUPPORTED"
    L = ["# Correspondence chains: herb → star → body", "",
         f"Pre-registration: `analyses/chains_prereg.md`. Rare chunk = in < {RARE_TYPES} word types. "
         f"{N_DRAWS:,} draws, seed {SEED}.", "",
         f"Sizes: herbal openings {len(H)}, star labels {len(S)}, body labels (Ln/Lt/Lz) {len(B)}, "
         f"remedy labels (Lc/Lf) {len(R)}, other labels {len(O)}. Rare chunks shared by herb and star: {len(hs)}.", "",
         "| Test | Chains | Expected | p | Verdict |", "|---|---:|---:|---:|---|",
         f"| **Primary: herb → star → body** | {o1} | {e1:.2f} | {p1:.3g} | **{v(p1)}** |",
         f"| Secondary: herb → star → remedy | {o2} | {e2:.2f} | {p2:.3g} | {v(p2)} |",
         f"| Secondary: herb → star → body → remedy | {obs4} | {null4.mean():.2f} | {p4:.3g} | {v(p4)} |", "",
         "## Every herb–star shared chunk and where else it goes", "",
         "| Chunk | Herb openings | Star labels | Body labels | Remedy labels |", "|---|---|---|---|---|"]
    for c in sorted(hs, key=lambda c: (-(c in cset(B)) - (c in cset(R)), c)):
        L.append(f"| `{show(c)}` | {ex(H, c)} | {ex(S, c)} | {ex(B, c) or '—'} | {ex(R, c) or '—'} |")
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "chains_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
