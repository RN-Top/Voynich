#!/usr/bin/env python3
"""Metal key (planetary scale) and sevens (analyses/metal_key_prereg.md).

    python analyses/metal_key_test.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402
from root_dictionary_test import root_of  # noqa: E402

SEED = 20261004
N_PERMS = 10_000
ALPHA = 0.025
# colour -> (planet, metal, place on the Ptolemaic scale)
KEY = {"white": ("Moon", "silver", 1), "green": ("Venus", "copper", 3), "yellow": ("Sun", "gold", 4),
       "red": ("Mars", "iron", 5), "blue": ("Jupiter", "tin", 6)}


def sim_matrix(p, pages):
    vecs = {f: Counter(p[p.folio == f].clean.map(root_of)) for f in pages}
    vocab = sorted(set().union(*vecs.values()))
    ix = {v: i for i, v in enumerate(vocab)}
    M = np.zeros((len(pages), len(vocab)))
    for i, f in enumerate(pages):
        for k, v in vecs[f].items():
            M[i, ix[k]] = v
    M /= np.linalg.norm(M, axis=1, keepdims=True)
    return M @ M.T


def shuffle_within(x, groups, rng):
    y = x.copy()
    for g in groups:
        y[g] = x[g][rng.permutation(len(g))]
    return y


def pearson(a, b):
    a, b = a - a.mean(), b - b.mean()
    return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum()))


def main():
    colour = {r["folio"]: r["colour"] for r in csv.DictReader(open(ROOT / "analyses" / "flower_colours.csv"))}
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.section == "Herbal") & (df.clean.str.len() > 0)]
    cur = p.groupby("folio").currier.agg(lambda s: s.mode()[0])
    rng = np.random.default_rng(SEED)

    # ---- Test 1: planetary scale
    pages = [f for f in p.folio.unique() if colour.get(f) in KEY]
    S = sim_matrix(p, pages)
    iu = np.triu_indices(len(pages), 1)
    sims = S[iu]
    rank = np.array([KEY[colour[f]][2] for f in pages])
    groups = [np.flatnonzero(np.array([cur[f] for f in pages]) == c) for c in ("A", "B")]

    def stat1(r):
        d = np.abs(r[iu[0]] - r[iu[1]])
        keep = d > 0
        return pearson(rankdata(d[keep]), rankdata(sims[keep]))

    obs1 = stat1(rank)
    null1 = np.array([stat1(shuffle_within(rank, groups, rng)) for _ in range(N_PERMS)])
    p1 = float((np.sum(null1 <= obs1) + 1) / (N_PERMS + 1))
    d_all = np.abs(rank[iu[0]] - rank[iu[1]])
    by_dist = {int(k): (int((d_all == k).sum()), float(sims[d_all == k].mean())) for k in np.unique(d_all)}

    # ---- Test 2: sevens in book order
    pages2 = list(p.folio.unique())
    S2 = sim_matrix(p, pages2)
    groups2 = [np.flatnonzero(np.array([cur[f] for f in pages2]) == c) for c in ("A", "B")]
    n = len(pages2)

    def lag_means(order):
        T = S2[np.ix_(order, order)]
        return {k: float(np.diagonal(T, k).mean()) for k in range(2, 14)}

    def contrast(m, k):
        return m[k] - 0.5 * (m[k - 1] + m[k + 1])

    base = np.arange(n)
    m_obs = lag_means(base)
    obs2 = contrast(m_obs, 7)
    nulls = {k: np.empty(N_PERMS) for k in range(3, 13)}
    for t in range(N_PERMS):
        m = lag_means(shuffle_within(base, groups2, rng))
        for k in nulls:
            nulls[k][t] = contrast(m, k)
    p2 = float((np.sum(nulls[7] >= obs2) + 1) / (N_PERMS + 1))

    v = lambda pv: "SUPPORTED" if pv < ALPHA else "NOT SUPPORTED"
    L = ["# The metal key and sevens", "",
         "Pre-registration: `analyses/metal_key_prereg.md`. Key: flower colour → heraldic planet → metal. "
         f"{N_PERMS:,} shuffles within Currier language, seed {SEED}; threshold p < {ALPHA} (Bonferroni over 2).", "",
         "## Test 1: does the planetary scale order the text?", "",
         f"{len(pages)} herbal pages. Pages per metal: " + ", ".join(
             f"{KEY[c][1]} ({KEY[c][0]}) {int((np.array([colour[f] for f in pages]) == c).sum())}" for c in KEY), "",
         f"- Spearman ρ (scale distance vs text similarity, different-metal pairs only): **{obs1:+.4f}** "
         f"(shuffled mean {null1.mean():+.4f}); one-sided p = {p1:.3g} → **{v(p1)}**", "",
         "| Scale distance | Pairs | Mean similarity |", "|---|---|---|"]
    L += [f"| {k} | {c} | {s:.4f} |" for k, (c, s) in by_dist.items()]
    L += ["", "## Test 2: a 7-page cycle in book order?", "",
          f"{n} herbal pages in current folio order.", "",
          f"- D7 (lag-7 similarity minus mean of lags 6 and 8): **{obs2:+.5f}** (shuffled mean {nulls[7].mean():+.5f}); "
          f"one-sided p = {p2:.3g} → **{v(p2)}**", "",
          "Same contrast at other lags (descriptive; not corrected):", "",
          "| Lag | Contrast | p (one-sided) |", "|---|---|---|"]
    for k in range(3, 13):
        c = contrast(m_obs, k)
        L.append(f"| {k} | {c:+.5f} | {(np.sum(nulls[k] >= c) + 1) / (N_PERMS + 1):.3g} |")
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "metal_key_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
