#!/usr/bin/env python3
"""Zodiac labels vs the 28 lunar mansions (analyses/mansions_prereg.md)"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from zodiac_days_test import zodiac_labels  # noqa: E402

SEED = 20261010
N_DRAWS = 10_000
MAXGAP = 4
ORDER = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorp", "Sagitt", "Capric", "Aquar", "Pisces"]


def sign_index(name):
    for k, s in enumerate(ORDER):
        if s.lower() in name.lower():
            return k
    raise ValueError(name)


def bigrams(w):
    s = "^" + w + "$"
    return {s[i:i + 2] for i in range(len(s) - 1)}


def main():
    signs = zodiac_labels()
    data = []
    for s in signs.values():
        k = sign_index(s["name"])
        labs = s["labels"]
        n = len(labs)
        B = [bigrams(w) for w in labs]
        pairs = [(i, j, len(B[i] & B[j]) / len(B[i] | B[j])) for i in range(n) for j in range(i + 1, min(n, i + MAXGAP + 1))]
        data.append((s["name"], k, n, np.array([p[0] for p in pairs]), np.array([p[1] for p in pairs]),
                     np.array([p[2] for p in pairs])))

    def mansions(k, n, shift):
        d = 30 * ((np.arange(n) + shift) % n) / n
        return np.floor((30 * k + d) / (360 / 28)).astype(int)

    def stat(shifts):
        same, diff = [], []
        for (name, k, n, I, J, S), sh in zip(data, shifts):
            m = mansions(k, n, sh)
            eq = m[I] == m[J]
            same.append(S[eq]); diff.append(S[~eq])
        return np.concatenate(same).mean() - np.concatenate(diff).mean()

    obs = stat([0] * len(data))
    rng = np.random.default_rng(SEED)
    null = np.array([stat([rng.integers(n) for (_, _, n, *_ ) in data]) for _ in range(N_DRAWS)])
    p = float((np.sum(null >= obs) + 1) / (N_DRAWS + 1))
    L = ["# Zodiac labels and the 28 lunar mansions", "",
         "Pre-registration: `analyses/mansions_prereg.md`. "
         f"{len(data)} signs, label pairs 1–{MAXGAP} apart, {N_DRAWS:,} random boundary shifts, seed {SEED}.", "",
         f"- Same-mansion minus cross-boundary similarity: **{obs:+.4f}** (shifted boundaries {null.mean():+.4f}); "
         f"p = {p:.3g} → **{'SUPPORTED' if p < 0.05 else 'NOT SUPPORTED'}**", "",
         "| Sign | Labels | Mansions touched (boundary after label #) |", "|---|---:|---|"]
    for name, k, n, *_ in data:
        m = mansions(k, n, 0)
        cuts = [i for i in range(1, n) if m[i] != m[i - 1]]
        L.append(f"| {name} | {n} | {sorted(set(m.tolist()))} (cuts at {cuts}) |")
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "mansions_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
