#!/usr/bin/env python3
"""Recipe roots as process words (analyses/process_words_prereg.md)"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from recipe_format_test import paragraphs  # noqa: E402
from root_dictionary_test import root_of  # noqa: E402

SEED = 20261012
N = 10_000
RECIPE = ["alk", "cheeo", "cheed", "ched", "kech", "lke", "lk", "lkee", "pair", "ted", "tched", "teed", "keed",
          "lkch", "lr", "rar", "chd", "tair", "lkeeo"]


def main():
    paras = [[root_of(w) for w in ws] for s, ws in paragraphs() if s == "Stars/Recipes"]
    L = np.array([len(p) for p in paras]); Ntok = L.sum()
    count = Counter(r for p in paras for r in p)
    sets = [set(p) for p in paras]

    def disp(r):
        k = count[r]
        cov = np.mean([r in s for s in sets])
        exp = np.mean(1 - (1 - L / Ntok) ** k)
        return cov / exp

    rec = [r for r in RECIPE if count[r] >= 5]
    D = {r: disp(r) for r in rec}
    obs = float(np.mean(list(D.values())))
    pool = [r for r in count if r not in RECIPE and count[r] >= 5]
    pdisp = {r: disp(r) for r in pool}
    rng = np.random.default_rng(SEED)
    cands = {r: [c for c in pool if abs(count[c] - count[r]) <= 0.25 * count[r]] for r in rec}
    null = np.array([np.mean([pdisp[rng.choice(cands[r])] for r in rec]) for _ in range(N)])
    p = float((np.sum(null >= obs) + 1) / (N + 1))

    def nb(r, off):
        c = Counter()
        for q in paras:
            for i, x in enumerate(q):
                if x == r and 0 <= i + off < len(q):
                    c[q[i + off]] += 1
        return ", ".join(f"{w}" for w, _ in c.most_common(3))

    out = ["# Recipe-section roots: process words or ingredients?", "",
           f"Pre-registration: `analyses/process_words_prereg.md`. {len(paras)} recipe paragraphs, {Ntok} tokens; "
           f"{len(rec)} recipe roots; {N:,} frequency-matched draws, seed {SEED}.", "",
           f"- Mean dispersion of recipe roots: **{obs:.3f}** (matched roots {null.mean():.3f}; 1.0 = random spread, "
           f"lower = clumped); p = {p:.3g} → **{'SUPPORTED' if p < 0.05 else 'NOT SUPPORTED'}**", "",
           "| Root | Tokens | Paragraphs containing it | Dispersion | Often before | Often after |",
           "|---|---:|---:|---:|---|---|"]
    for r in sorted(rec, key=lambda r: -count[r]):
        out.append(f"| {r} | {count[r]} | {np.mean([r in s for s in sets]):.0%} | {D[r]:.2f} | {nb(r, -1)} | {nb(r, 1)} |")
    report = "\n".join(out) + "\n"
    (ROOT / "output" / "process_words_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
