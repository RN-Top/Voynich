#!/usr/bin/env python3
"""Are the diagram labels measurements (coordinates)? (analyses/coordinates_prereg.md)

    python analyses/coordinates_test.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, VoynichParser  # noqa: E402

SEED = 20261003
N_PERMS = 10_000
MIN_LABELS = 8


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def main():
    diag = defaultdict(list)  # folio -> [(angle, word, code)]
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.(L\w)>\s+<!(\d\d):(\d\d)>(.*)", line)
        if not m:
            continue
        text = re.sub(r"<[^>]*>", "", m.group(5)).strip()
        w = VoynichParser.clean_token(re.split(r"[.,\s]+", text)[0]) if text else ""
        if w:
            ang = ((int(m.group(3)) % 12) * 60 + int(m.group(4))) / 720 * 360
            diag[m.group(1)].append((ang, w, m.group(2)))
    diag = {f: v for f, v in diag.items() if len(v) >= MIN_LABELS}
    pairs_i, pairs_j, dist, groups, words = [], [], [], [], []
    off = 0
    nn_mask = []
    for f, items in diag.items():
        n = len(items)
        angs = np.array([a for a, _, _ in items])
        words += [w for _, w, _ in items]
        groups.append(np.arange(off, off + n))
        D = np.abs(angs[:, None] - angs[None, :])
        D = np.minimum(D, 360 - D)
        np.fill_diagonal(D, np.inf)
        nearest = D.argmin(1)
        for i in range(n):
            for j in range(i + 1, n):
                pairs_i.append(off + i)
                pairs_j.append(off + j)
                dist.append(D[i, j])
                nn_mask.append(nearest[i] == j or nearest[j] == i)
        off += n
    pi, pj, dist, nn_mask = map(np.array, (pairs_i, pairs_j, dist, nn_mask))
    W = len(words)
    cache = {}

    def dis(a, b):
        k = (a, b) if a < b else (b, a)
        if k not in cache:
            cache[k] = lev(a, b) / max(len(a), len(b))
        return cache[k]

    def stats(order):
        w = [words[k] for k in order]
        d = np.array([dis(w[a], w[b]) for a, b in zip(pi, pj)])
        return spearmanr(dist, d).correlation, d[nn_mask].mean() - d[~nn_mask].mean()

    ident = np.arange(W)
    obs_r, obs_nn = stats(ident)
    rng = np.random.default_rng(SEED)
    null_r, null_nn = np.empty(N_PERMS), np.empty(N_PERMS)
    for t in range(N_PERMS):
        order = ident.copy()
        for g in groups:
            order[g] = g[rng.permutation(len(g))]
        null_r[t], null_nn[t] = stats(order)
    p_r = float((np.sum(null_r >= obs_r) + 1) / (N_PERMS + 1))
    p_nn = float((np.sum(null_nn <= obs_nn) + 1) / (N_PERMS + 1))
    codes = sorted({c for v in diag.values() for _, _, c in v})
    L = ["# Are the diagram labels measurements (coordinates)?", "",
         f"Pre-registration: `analyses/coordinates_prereg.md`. {len(diag)} diagrams with ≥{MIN_LABELS} positioned labels "
         f"({W} labels; label codes {', '.join(codes)}); {len(pi):,} within-diagram pairs; {N_PERMS:,} shuffles, seed {SEED}.", "",
         f"- Correlation between angular distance and label dissimilarity: **{obs_r:+.3f}** (shuffled {null_r.mean():+.3f}); "
         f"p = {p_r:.3g} → **{'SUPPORTED' if p_r < 0.01 else 'NOT SUPPORTED'}**",
         f"- Neighbours minus other pairs, mean dissimilarity: {obs_nn:+.3f} (shuffled {null_nn.mean():+.3f}); p = {p_nn:.3g}", "",
         "Diagrams: " + ", ".join(f"{f} ({len(v)})" for f, v in diag.items())]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "coordinates_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
