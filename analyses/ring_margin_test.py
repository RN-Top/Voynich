#!/usr/bin/env python3
"""f66r margin column vs f57v ring; golden-number check (analyses/ring_margin_prereg.md)"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261007
N_PERMS = 10_000
RING = [{"o"}, {"l"}, {"d", "j"}, {"r"}, {"v"}, {"x"}, {"k"}, {"m"}, {"f", "p"}, {"@169"}, {"t"}, {"r"},
        {"@170"}, {"@171"}, {"y"}, {"c", "I"}, {"@172"}]


def margin():
    out = []
    for line in open(ROOT / "data" / "ZL3b-n.txt", encoding="utf-8"):
        m = re.match(r"<f66r\.(\d+),", line)
        if m and 16 <= int(m.group(1)) <= 49:
            out.append(re.sub(r"<[^>]*>|;", "", line.split(">", 1)[1]).strip())
    return out


def follows(a, b):
    return any(a in RING[i] and b in RING[(i + 1) % 17] for i in range(17))


def main():
    col = margin()
    hits = lambda c: sum(follows(a, b) for a, b in zip(c, c[1:]))
    h = hits(col)
    rng = np.random.default_rng(SEED)
    null = np.array([hits(list(rng.permutation(col))) for _ in range(N_PERMS)])
    p = float((np.sum(null >= h) + 1) / (N_PERMS + 1))
    pairs = [f"{a}→{b}" for a, b in zip(col, col[1:]) if follows(a, b)]
    R = sum(col[i] in col[max(0, i - 18):i] for i in range(len(col)))
    distinct = len(set(col))
    L = ["# f66r margin column vs the f57v ring; golden-number check", "",
         "Pre-registration: `analyses/ring_margin_prereg.md`.", "",
         f"Margin column ({len(col)} entries): `{' '.join(col)}`", "",
         "## Test A: does the column follow the ring's order?", "",
         f"- Adjacent pairs in ring order: **{h}** ({', '.join(pairs) or 'none'}); shuffled mean {null.mean():.2f}; "
         f"p = {p:.3g} → **{'SUPPORTED' if p < 0.05 else 'NOT SUPPORTED'}**", "",
         "## Test B: a golden-number (19-year moon cycle) column?", "",
         f"- Distinct symbols: {distinct} (a golden-number column would have about 19)",
         f"- Repeats within 19 entries: **R = {R}** (a golden-number column needs ≤ 2) → "
         f"**{'CONSISTENT' if R <= 2 else 'REJECTED'}**", ""]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "ring_margin_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
