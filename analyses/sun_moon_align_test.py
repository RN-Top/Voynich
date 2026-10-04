#!/usr/bin/env python3
"""Sun wheel (f67r1) vs Moon wheel (f67r2) alignment (analyses/sun_moon_align_prereg.md)"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261009
N_PERMS = 10_000


def loci(folio, lo, hi):
    out = []
    for line in open(ROOT / "data" / "ZL3b-n.txt", encoding="utf-8"):
        m = re.match(rf"<{folio}\.(\d+),", line)
        if m and lo <= int(m.group(1)) <= hi:
            t = re.sub(r"<[^>]*>", "", line.split(">", 1)[1])
            t = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", t)
            out.append(re.sub(r"[.,\s{}']", "", t))
    return out


def bigrams(w):
    s = "^" + w + "$"
    return {s[i:i + 2] for i in range(len(s) - 1)}


def main():
    sun, moon = loci("f67r1", 8, 19), loci("f67r2", 52, 63)
    assert len(sun) == len(moon) == 12
    B1, B2 = [bigrams(w) for w in sun], [bigrams(w) for w in moon]
    J = np.array([[len(a & b) / len(a | b) for b in B2] for a in B1])
    idx = np.arange(12)
    scores = lambda order: np.array([J[idx, order[(idx + s) % 12]].mean() for s in range(12)])
    S = scores(idx)
    M = S.max()
    best = int(S.argmax())
    rng = np.random.default_rng(SEED)
    null = np.array([scores(rng.permutation(12)).max() for _ in range(N_PERMS)])
    p = float((np.sum(null >= M) + 1) / (N_PERMS + 1))
    L = ["# Sun wheel (f67r1) and Moon wheel (f67r2): read together?", "",
         "Pre-registration: `analyses/sun_moon_align_prereg.md`.", "",
         f"- Best rotation: shift {best}, mean pair similarity **{M:.3f}** (shuffled best {null.mean():.3f}); "
         f"p = {p:.3g} → **{'SUPPORTED' if p < 0.05 else 'NOT SUPPORTED'}**", "",
         "Score by rotation: " + ", ".join(f"{s}: {v:.3f}" for s, v in enumerate(S)), "",
         "| Sector | Sun label | Moon label | Similarity |", "|---|---|---|---:|"]
    L += [f"| {i + 1} | {sun[i]} | {moon[(i + best) % 12]} | {J[i, (i + best) % 12]:.2f} |" for i in range(12)]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "sun_moon_align_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
