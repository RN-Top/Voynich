#!/usr/bin/env python3
"""Jar-label endings, split replication (analyses/jar_endings_prereg.md)"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from dictionary_test import labels  # noqa: E402

SEED = 20261008
N_PERMS = 10_000


def main():
    d = labels()
    d = d[d.code.isin(["Lc", "Lf"])].reset_index(drop=True)
    b1 = d[d.folio.str.match(r"f8[89]")]
    b2 = d[d.folio.str.match(r"f(99|10[012])")].reset_index(drop=True)
    base = (b1.code == "Lc").mean()
    tab = b1.groupby("ending").code.agg(jar=lambda s: (s == "Lc").sum(), n="size")
    jar_end = sorted(tab[(tab.jar >= 2) & (tab.jar / tab.n > base)].index)
    has = b2.ending.isin(jar_end).to_numpy()
    kind = (b2.code == "Lc").to_numpy()
    stat = lambda k: has[k].mean() - has[~k].mean()
    obs = stat(kind)
    groups = [np.flatnonzero(b2.folio.to_numpy() == f) for f in b2.folio.unique()]
    rng = np.random.default_rng(SEED)
    null = np.empty(N_PERMS)
    for t in range(N_PERMS):
        k = kind.copy()
        for g in groups:
            k[g] = kind[g][rng.permutation(len(g))]
        null[t] = stat(k)
    p = float((np.sum(null >= obs) + 1) / (N_PERMS + 1))
    jars2 = b2[kind]
    L = ["# Jar-label endings: split replication", "",
         "Pre-registration: `analyses/jar_endings_prereg.md`. Block 1 = f88–f89, block 2 = f99–f102.", "",
         f"- Block 1: {int((b1.code == 'Lc').sum())} jar, {int((b1.code == 'Lf').sum())} plant-part labels. "
         f"Jar endings learned: **{', '.join('-' + e for e in jar_end) or 'none'}**",
         f"- Block 2: {int(kind.sum())} jar, {int((~kind).sum())} plant-part labels.",
         f"- Jar labels with a jar ending: {has[kind].mean():.0%}; plant-part labels: {has[~kind].mean():.0%}",
         f"- Difference **{obs:+.3f}** (shuffled {null.mean():+.3f}); p = {p:.3g} → "
         f"**{'SUPPORTED' if p < 0.05 else 'NOT SUPPORTED'}**", "",
         "Block 2 jar labels: " + ", ".join(f"{w} ({f})" for w, f in zip(jars2.word, jars2.folio)), ""]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "jar_endings_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
