#!/usr/bin/env python3
"""Is the label gradient position (measurement) or writing order (drift)? (analyses/coord_vs_drift_prereg.md)

    python analyses/coord_vs_drift_test.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from coordinates_test import MIN_LABELS, lev  # noqa: E402
from parser import CORPUS_PATH, VoynichParser  # noqa: E402

SEED = 20261003
N_PERMS = 10_000


def partial(x, y, z):
    """Partial correlation of x and y controlling for z (inputs already ranked)."""
    rxy, rxz, ryz = np.corrcoef(x, y)[0, 1], np.corrcoef(x, z)[0, 1], np.corrcoef(y, z)[0, 1]
    return (rxy - rxz * ryz) / np.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))


def main():
    diag = defaultdict(list)
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.(L\w)>\s+<!(\d\d):(\d\d)>(.*)", line)
        if not m:
            continue
        text = re.sub(r"<[^>]*>", "", m.group(5)).strip()
        w = VoynichParser.clean_token(re.split(r"[.,\s]+", text)[0]) if text else ""
        if w:
            ang = ((int(m.group(3)) % 12) * 60 + int(m.group(4))) / 720 * 360
            diag[m.group(1)].append((ang, w))
    diag = {f: v for f, v in diag.items() if len(v) >= MIN_LABELS}
    words, groups, pi, pj, angd, seqd = [], [], [], [], [], []
    off = 0
    for f, items in diag.items():
        n = len(items)
        words += [w for _, w in items]
        groups.append(np.arange(off, off + n))
        for i in range(n):
            for j in range(i + 1, n):
                d = abs(items[i][0] - items[j][0])
                pi.append(off + i)
                pj.append(off + j)
                angd.append(min(d, 360 - d))
                seqd.append(j - i)
        off += n
    pi, pj = np.array(pi), np.array(pj)
    ra, rs = rankdata(angd), rankdata(seqd)
    cache = {}

    def dis(a, b):
        k = (a, b) if a < b else (b, a)
        if k not in cache:
            cache[k] = lev(a, b) / max(len(a), len(b))
        return cache[k]

    def stats(order):
        w = [words[k] for k in order]
        rd = rankdata([dis(w[a], w[b]) for a, b in zip(pi, pj)])
        return partial(rd, ra, rs), partial(rd, rs, ra)

    ident = np.arange(len(words))
    oa, os_ = stats(ident)
    rng = np.random.default_rng(SEED)
    na, ns = np.empty(N_PERMS), np.empty(N_PERMS)
    for t in range(N_PERMS):
        order = ident.copy()
        for g in groups:
            order[g] = g[rng.permutation(len(g))]
        na[t], ns[t] = stats(order)
    pa = float((np.sum(na >= oa) + 1) / (N_PERMS + 1))
    ps = float((np.sum(ns >= os_) + 1) / (N_PERMS + 1))
    if pa < 0.01 and ps >= 0.01:
        verdict = "MEASUREMENT (position)"
    elif ps < 0.01 and pa >= 0.01:
        verdict = "DRIFT (writing order)"
    elif pa < 0.01 and ps < 0.01:
        verdict = "BOTH"
    else:
        verdict = "UNDECIDED"
    r_as = np.corrcoef(ra, rs)[0, 1]
    L = ["# Position (measurement) or writing order (drift)?", "",
         f"Pre-registration: `analyses/coord_vs_drift_prereg.md`. {len(diag)} wheels, {len(words)} labels, "
         f"{len(pi):,} pairs; {N_PERMS:,} shuffles, seed {SEED}.", "",
         f"- Rank correlation between angular distance and sequence distance: {r_as:.2f} (how far the two can be told apart)",
         f"- Dissimilarity with **angle**, controlling for sequence: **{oa:+.3f}** (shuffled {na.mean():+.3f}), p = {pa:.3g}",
         f"- Dissimilarity with **sequence**, controlling for angle: **{os_:+.3f}** (shuffled {ns.mean():+.3f}), p = {ps:.3g}", "",
         f"**Verdict: {verdict}.**"]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "coord_vs_drift_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
