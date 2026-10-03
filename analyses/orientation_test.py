#!/usr/bin/env python3
"""Does writing orientation explain the zodiac label gradient? (analyses/orientation_prereg.md)

    python analyses/orientation_test.py
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


def main():
    diag = defaultdict(list)
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.(L\w)>\s+<!(\d\d):(\d\d)>(.*)", line)
        if not m:
            continue
        text = re.sub(r"<[^>]*>", "", m.group(5)).strip()
        w = VoynichParser.clean_token(re.split(r"[.,\s]+", text)[0]) if text else ""
        if w:
            diag[m.group(1)].append((((int(m.group(3)) % 12) * 60 + int(m.group(4))) / 2, w))
    diag = {f: v for f, v in diag.items() if len(v) >= MIN_LABELS}
    angles, words, groups, wheel = [], [], [], []
    off = 0
    for k, (f, items) in enumerate(diag.items()):
        angles += [a for a, _ in items]
        words += [w for _, w in items]
        groups.append(np.arange(off, off + len(items)))
        wheel += [k] * len(items)
        off += len(items)
    angles, wheel = np.array(angles), np.array(wheel)
    iu = np.triu_indices(len(words), 1)
    cross = wheel[iu[0]] != wheel[iu[1]]
    pi, pj = iu[0][cross], iu[1][cross]
    d = np.abs(angles[pi] - angles[pj])
    ra = rankdata(np.minimum(d, 360 - d))
    uniq = sorted(set(words))
    ix = {w: i for i, w in enumerate(uniq)}
    D = np.zeros((len(uniq), len(uniq)))
    for i, a in enumerate(uniq):
        for j in range(i + 1, len(uniq)):
            D[i, j] = D[j, i] = lev(a, uniq[j]) / max(len(a), len(uniq[j]))
    wid = np.array([ix[w] for w in words])

    def stat(order):
        w = wid[order]
        return float(np.corrcoef(ra, rankdata(D[w[pi], w[pj]]))[0, 1])

    ident = np.arange(len(words))
    obs = stat(ident)
    rng = np.random.default_rng(SEED)
    null = np.empty(N_PERMS)
    for t in range(N_PERMS):
        order = ident.copy()
        for g in groups:
            order[g] = g[rng.permutation(len(g))]
        null[t] = stat(order)
    p = float((np.sum(null >= obs) + 1) / (N_PERMS + 1))
    verdict = "ORIENTATION POSSIBLE" if p < 0.01 else "ORIENTATION NOT SUPPORTED (measurement reading stands)"
    L = ["# Does writing orientation explain the zodiac label gradient?", "",
         f"Pre-registration: `analyses/orientation_prereg.md`. {len(diag)} wheels, {len(words)} labels, "
         f"{len(pi):,} cross-wheel pairs; {N_PERMS:,} shuffles, seed {SEED}.", "",
         f"- Cross-wheel correlation, absolute angle vs dissimilarity: **{obs:+.3f}** (shuffled {null.mean():+.3f}), p = {p:.3g}", "",
         f"**Verdict: {verdict}.**"]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "orientation_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
