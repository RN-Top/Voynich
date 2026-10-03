#!/usr/bin/env python3
"""Does the vocabulary split into glue words and content words? (analyses/glue_words_prereg.md)

    python analyses/glue_words_test.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261003
N_PERMS = 10_000
ALPHA = 0.01
MIN_COUNT = 30
BANDS = [30, 50, 100, 200, 500, 10**9]


def main():
    df = parse_zl3b(CORPUS_PATH)
    b = df[(df.locus_type == "P") & (df.currier == "B") & (df.clean.str.len() > 0)]
    tab = pd.crosstab(b.clean, b.section)
    tab = tab[tab.sum(1) >= MIN_COUNT]
    overall = b.section.value_counts(normalize=True).reindex(tab.columns).to_numpy()
    sm = tab.to_numpy(float) + 0.5
    dist = sm / sm.sum(1, keepdims=True)
    kl = (dist * np.log2(dist / overall)).sum(1)
    words = tab.index.to_numpy()
    length = np.array([len(w) for w in words])
    count = tab.sum(1).to_numpy()
    band = np.digitize(count, BANDS)
    obs = spearmanr(length, kl).correlation
    rng = np.random.default_rng(SEED)
    groups = [np.flatnonzero(band == k) for k in np.unique(band)]
    null = np.empty(N_PERMS)
    for i in range(N_PERMS):
        s = kl.copy()
        for g in groups:
            s[g] = kl[g][rng.permutation(len(g))]
        null[i] = spearmanr(length, s).correlation
    p = float((np.sum(null >= obs) + 1) / (N_PERMS + 1))
    main_sec = tab.idxmax(axis=1).to_numpy()
    order = np.argsort(kl)
    row = lambda i: f"| {words[i]} | {count[i]} | {length[i]} | {kl[i]:.3f} | {main_sec[i]} |"
    L = ["# Glue words and content words", "",
         f"Pre-registration: `analyses/glue_words_prereg.md`. Currier B paragraph text; {len(words)} words with "
         f"{MIN_COUNT}+ uses; {N_PERMS:,} shuffles within frequency bands, seed {SEED}.", "",
         f"- Spearman correlation, length vs unevenness: **{obs:+.3f}** (shuffled within frequency bands: {null.mean():+.3f})",
         f"- p = {p:.3g} → **{'SUPPORTED' if p < ALPHA else 'NOT SUPPORTED'}**", "",
         "## Most even words (glue candidates)", "", "| Word | Uses | Length | Unevenness | Main section |",
         "|---|---:|---:|---:|---|"]
    L += [row(i) for i in order[:20]]
    L += ["", "## Most topic-bound words (content candidates)", "", "| Word | Uses | Length | Unevenness | Main section |",
          "|---|---:|---:|---:|---|"]
    L += [row(i) for i in order[::-1][:20]]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "glue_words_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
