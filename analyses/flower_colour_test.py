#!/usr/bin/env python3
"""Do flower colours line up with the text? (analyses/flower_colour_prereg.md)

    python analyses/flower_colour_test.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402
from root_dictionary_test import root_of  # noqa: E402

SEED = 20261003
N_PERMS = 10_000
USE = {"blue", "red", "yellow", "white", "green"}


def main():
    colour = {r["folio"]: r["colour"] for r in csv.DictReader(open(ROOT / "analyses" / "flower_colours.csv"))}
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.section == "Herbal") & (df.clean.str.len() > 0)]
    pages = [f for f in p.folio.unique() if colour.get(f) in USE]
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
    cols = np.array([colour[f] for f in pages])
    groups = [np.flatnonzero(np.array([cur[f] for f in pages]) == c) for c in ("A", "B")]

    def stat(c):
        same = c[iu[0]] == c[iu[1]]
        return S[iu][same].mean() - S[iu][~same].mean()

    obs = stat(cols)
    rng = np.random.default_rng(SEED)
    null = np.empty(N_PERMS)
    for t in range(N_PERMS):
        c = cols.copy()
        for g in groups:
            c[g] = cols[g][rng.permutation(len(g))]
        null[t] = stat(c)
    pv = float((np.sum(null >= obs) + 1) / (N_PERMS + 1))
    opening = p.groupby("folio", sort=False).clean.first()
    L = ["# Do flower colours line up with the text?", "",
         f"Pre-registration: `analyses/flower_colour_prereg.md`. Colours: `analyses/flower_colours.csv`. {len(pages)} herbal "
         f"pages with a single flower colour; colour labels shuffled within Currier language, {N_PERMS:,} times, seed {SEED}.", "",
         f"- Pages per colour: {dict(Counter(cols))}",
         f"- Same-colour minus different-colour text similarity: **{obs:+.4f}** (shuffled {null.mean():+.4f}); "
         f"p = {pv:.3g} → **{'SUPPORTED' if pv < 0.01 else 'NOT SUPPORTED'}**", "",
         "## Opening words by colour (descriptive)", ""]
    for c in sorted(USE):
        fs = [f for f in pages if colour[f] == c]
        L.append(f"- **{c}** ({len(fs)}): " + ", ".join(f"{opening[f]} ({f})" for f in fs))
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "flower_colour_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
