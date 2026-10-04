#!/usr/bin/env python3
"""Two-colour leaves (analyses/leaf_colour_prereg.md)

    python analyses/leaf_colour_test.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import fisher_exact

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402
from root_dictionary_test import root_of  # noqa: E402

SEED = 20261006
N_PERMS = 10_000
ALPHA = 0.05
STAR_MATCH = {"f1r", "f3v", "f6v", "f9r", "f13v", "f16r", "f19v", "f23r", "f27v", "f30v", "f37r", "f52r", "f56r"}


def main():
    leaf = {r["folio"]: r["leaf2"] for r in csv.DictReader(open(ROOT / "analyses" / "leaf_colours.csv"))}
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.section == "Herbal") & (df.clean.str.len() > 0)]
    pages = [f for f in p.folio.unique() if f in leaf]
    cur = p.groupby("folio").currier.agg(lambda s: s.mode()[0])
    vecs = {f: Counter(p[p.folio == f].clean.map(root_of)) for f in pages}
    vocab = sorted(set().union(*vecs.values()))
    ix = {v: i for i, v in enumerate(vocab)}
    M = np.zeros((len(pages), len(vocab)))
    for i, f in enumerate(pages):
        for k, v in vecs[f].items():
            M[i, ix[k]] = v
    M /= np.linalg.norm(M, axis=1, keepdims=True)
    S = M @ M.T
    iu = np.triu_indices(len(pages), 1)
    y = np.array([leaf[f] == "yes" for f in pages])
    groups = [np.flatnonzero(np.array([cur[f] for f in pages]) == c) for c in ("A", "B")]

    def stat(lab):
        a, b = lab[iu[0]], lab[iu[1]]
        return S[iu][a & b].mean() - S[iu][a ^ b].mean()

    obs = stat(y)
    rng = np.random.default_rng(SEED)
    null = np.empty(N_PERMS)
    for t in range(N_PERMS):
        z = y.copy()
        for g in groups:
            z[g] = y[g][rng.permutation(len(g))]
        null[t] = stat(z)
    pv = float((np.sum(null >= obs) + 1) / (N_PERMS + 1))
    yes = [f for f in pages if leaf[f] == "yes"]
    a = len(set(yes) & STAR_MATCH)
    tab = [[a, len(yes) - a], [len(STAR_MATCH & set(pages)) - a, len(pages) - len(yes) - len(STAR_MATCH & set(pages)) + a]]
    _, pf = fisher_exact(tab, alternative="greater")
    opening = p.groupby("folio", sort=False).clean.first()
    by_cur = Counter(cur[f] for f in yes)
    L = ["# Two-colour leaves", "",
         f"Pre-registration: `analyses/leaf_colour_prereg.md`. Classification: `analyses/leaf_colours.csv`. {len(pages)} herbal "
         f"pages, {len(yes)} with two-colour leaves (Currier {dict(by_cur)}). {N_PERMS:,} shuffles within Currier, seed {SEED}.", "",
         f"- Two-colour pages with each other minus with other pages (text similarity): **{obs:+.4f}** "
         f"(shuffled {null.mean():+.4f}); p = {pv:.3g} → **{'SUPPORTED' if pv < ALPHA else 'NOT SUPPORTED'}**", "",
         "## Secondary", "",
         f"- Two-colour pages among the 13 star-matching openings: {a} of {len(yes)} (Fisher one-sided p = {pf:.3g}).", "",
         "Opening words of the two-colour pages: " + ", ".join(f"{opening[f]} ({f})" for f in yes), ""]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "leaf_colour_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
