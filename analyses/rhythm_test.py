#!/usr/bin/env python3
"""Does anything pulse at a regular beat inside lines or down pages? (analyses/rhythm_prereg.md)

    python analyses/rhythm_test.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import structural_validation as sv  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261003
N_PERMS = 2000
R1_LAGS, R2_LAGS = range(1, 8), range(1, 10)


def r1(g, rng):
    g = g.reset_index(drop=True)
    end = pd.factorize(g.clean.map(sv.ending_of))[0]
    line = pd.factorize(g.folio + "|" + g.header)[0]
    pos = g.groupby(line).cumcount().to_numpy()
    length = np.bincount(line)[line]
    interior = (pos >= 1) & (pos <= length - 2)
    idx = np.flatnonzero(interior)
    e, ln = end[idx], line[idx]

    def m(vals):
        return {k: int(np.sum((vals[:-k] == vals[k:]) & (ln[:-k] == ln[k:]))) for k in R1_LAGS}

    def peaks(mm):
        return {k: mm[k] - (mm[k - 1] + mm[k + 1]) / 2 for k in range(2, 7)}

    obs = peaks(m(e))
    null = {k: np.empty(N_PERMS) for k in obs}
    for i in range(N_PERMS):
        s = e[np.lexsort((rng.random(len(e)), ln))]
        pk = peaks(m(s))
        for k in obs:
            null[k][i] = pk[k]
    return {k: (obs[k], float(null[k].mean()), float((np.sum(null[k] >= obs[k]) + 1) / (N_PERMS + 1))) for k in obs}


def r2(g, rng):
    g = g.assign(qo=g.clean.str.startswith("qo"))
    lines = g.groupby(["folio", "header"], sort=False).qo.mean().reset_index()
    series = [grp.qo.to_numpy() - grp.qo.mean() for _, grp in lines.groupby("folio", sort=False) if len(grp) >= 4]

    def a(ss):
        out = {}
        for k in R2_LAGS:
            prods = [s[:-k] * s[k:] for s in ss if len(s) > k]
            out[k] = float(np.concatenate(prods).mean()) if prods else 0.0
        return out

    def peaks(aa):
        return {k: aa[k] - (aa[k - 1] + aa[k + 1]) / 2 for k in range(2, 9)}

    obs = peaks(a(series))
    null = {k: np.empty(N_PERMS) for k in obs}
    for i in range(N_PERMS):
        pk = peaks(a([rng.permutation(s) for s in series]))
        for k in obs:
            null[k][i] = pk[k]
    return {k: (obs[k], float(null[k].mean()), float((np.sum(null[k] >= obs[k]) + 1) / (N_PERMS + 1))) for k in obs}


def main():
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.clean.str.len() > 0)]
    rng = np.random.default_rng(SEED)
    L = ["# Does anything pulse at a regular beat?", "",
         f"Pre-registration: `analyses/rhythm_prereg.md`. {N_PERMS:,} shuffles, seed {SEED}.", ""]
    found = []
    for cur in ("A", "B"):
        g = p[p.currier == cur]
        res1, res2 = r1(g, rng), r2(g, rng)
        L += [f"## Currier {cur}", "", "**R1, inside lines (same ending k words apart):**", "",
              "| k | Local peak | Shuffled | p |", "|---:|---:|---:|---:|"]
        for k, (o, n, pv) in res1.items():
            L.append(f"| {k} | {o:+.1f} | {n:+.1f} | {pv:.3g} |")
            if pv < 0.001:
                found.append(f"Currier {cur}: beat every {k} words")
        L += ["", "**R2, down the page (qo- share, k lines apart):**", "",
              "| k | Local peak | Shuffled | p |", "|---:|---:|---:|---:|"]
        for k, (o, n, pv) in res2.items():
            L.append(f"| {k} | {o:+.5f} | {n:+.5f} | {pv:.3g} |")
            if pv < 0.0007:
                found.append(f"Currier {cur}: wave every {k} lines")
        L.append("")
    L.append(f"**Verdict: {'; '.join(found) if found else 'no rhythm found'}.**")
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "rhythm_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
