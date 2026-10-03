#!/usr/bin/env python3
"""Is the ending -> next-beginning grammar the same for every scribe? (analyses/grammar_table_prereg.md)

    python analyses/grammar_table_test.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

import structural_validation as sv  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402
from scribes_test import hands  # noqa: E402

SEED = 20261003
N_PERMS = 1000
ALPHA = 0.01 / 3
MIN_CELL = 10
SCRIBES = ["1", "2", "3"]


class Scribe:
    def __init__(self, g: pd.DataFrame):
        g = g.reset_index(drop=True)
        self.end = g.clean.map(sv.ending_of).to_numpy()
        self.beg = g.clean.str[:2].to_numpy()
        line = pd.factorize(g.folio + "|" + g.header)[0]
        pos = g.groupby(line).cumcount().to_numpy()
        length = np.bincount(line)[line]
        interior = (pos >= 1) & (pos <= length - 2)
        self.pair = interior[:-1] & interior[1:] & (line[:-1] == line[1:])
        self.idx = np.flatnonzero(interior)
        self.grp = line[self.idx]
        self.folio = g.folio.to_numpy()

    def table(self, order=None, mask=None):
        e = self.end if order is None else self.end[order]
        b = self.beg if order is None else self.beg[order]
        pm = self.pair if mask is None else self.pair & mask[:-1]
        t = pd.crosstab(e[:-1][pm], b[1:][pm])
        exp = np.outer(t.sum(1), t.sum(0)) / t.to_numpy().sum()
        return t, pd.DataFrame(np.log(t.to_numpy() / exp), index=t.index, columns=t.columns)

    def shuffled(self, rng):
        order = np.arange(len(self.end))
        order[self.idx] = self.idx[np.lexsort((rng.random(len(self.idx)), self.grp))]
        return order


def corr(ta, la, tb, lb):
    cells = [(e, b) for e in ta.index for b in ta.columns
             if e in tb.index and b in tb.columns and ta.at[e, b] >= MIN_CELL and tb.at[e, b] >= MIN_CELL]
    if len(cells) < 5:
        return float("nan"), len(cells)
    x = np.array([la.at[c] for c in cells])
    y = np.array([lb.at[c] for c in cells])
    return float(np.corrcoef(x, y)[0, 1]), len(cells)


def main():
    hd = hands()
    df = parse_zl3b(CORPUS_PATH)
    df["hand"] = df.folio.map(hd)
    p = df[(df.locus_type == "P") & (df.clean.str.len() > 0)]
    S = {h: Scribe(p[p.hand == h]) for h in SCRIBES}
    tabs = {h: S[h].table() for h in SCRIBES}
    rng = np.random.default_rng(SEED)
    L = ["# Is the ending → next-beginning grammar the same for every scribe?", "",
         f"Pre-registration: `analyses/grammar_table_prereg.md`. {N_PERMS:,} within-line shuffles, seed {SEED}.", "",
         "| Scribes | Shared cells | Correlation of log lift | Shuffled mean | p | Result |",
         "|---|---:|---:|---:|---:|---|"]
    passes = []
    for a, b in itertools.combinations(SCRIBES, 2):
        r, n = corr(*tabs[a], *tabs[b])
        null = np.array([corr(*S[a].table(S[a].shuffled(rng)), *S[b].table(S[b].shuffled(rng)))[0]
                         for _ in range(N_PERMS)])
        null = np.nan_to_num(null, nan=-1)
        pv = float((np.sum(null >= r) + 1) / (N_PERMS + 1))
        passes.append(pv < ALPHA)
        L.append(f"| {a} vs {b} | {n} | {r:.3f} | {null.mean():.3f} | {pv:.3g} | {'PASS' if pv < ALPHA else 'FAIL'} |")
    L += ["", f"**Shared grammar across scribes: {'YES' if all(passes) else 'NO'}**", "",
          "## Split-half check within each scribe (descriptive)", ""]
    for h in SCRIBES:
        s = S[h]
        pages = pd.unique(s.folio)
        odd = np.isin(s.folio, pages[::2])
        r, n = corr(*s.table(mask=odd), *s.table(mask=~odd))
        L.append(f"- Scribe {h}: odd vs even pages, correlation {r:.3f} over {n} cells")
    L += ["", "## The grammar table (descriptive)", "",
          "For each ending: the next-word beginnings it favours most (lift = times more often than chance; count ≥ 10).", "",
          "| Ending of word | " + " | ".join(f"Scribe {h}" for h in SCRIBES) + " |", "|---|" + "---|" * len(SCRIBES)]
    common = [e for e in tabs["1"][0].index if all(e in tabs[h][0].index for h in SCRIBES) and e != "?"]
    for e in sorted(common, key=lambda e: -sum(tabs[h][0].loc[e].sum() for h in SCRIBES)):
        cells = []
        for h in SCRIBES:
            t, lg = tabs[h]
            row = [(b, np.exp(lg.at[e, b])) for b in t.columns if t.at[e, b] >= MIN_CELL]
            row.sort(key=lambda x: -x[1])
            cells.append(", ".join(f"{b}- ×{v:.1f}" for b, v in row[:3]) or "—")
        L.append(f"| -{e} | " + " | ".join(cells) + " |")
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "grammar_table_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
