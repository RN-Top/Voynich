#!/usr/bin/env python3
"""Do the star-marked paragraphs repeat in cycles? (analyses/cycles_prereg.md)

    python analyses/cycles_test.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from parser import CORPUS_PATH, VoynichParser, parse_zl3b  # noqa: E402
from root_dictionary_test import root_of  # noqa: E402

SEED = 20261003
N_PERMS = 10_000
ALPHA = 0.01
LAGS = list(range(1, 42))


def paragraphs():
    sec = parse_zl3b(CORPUS_PATH).groupby("folio")["section"].first().to_dict()
    runs, cur, words, last_leaf = [[], []], None, [], None
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f(\d+)[^.]*)\.\d+,.P\w*>\s+(.*)", line)
        if not m or sec.get(m.group(1)) != "Stars/Recipes":
            continue
        run = 0 if int(m.group(2)) <= 108 else 1
        text = m.group(3)
        if "<%>" in text:
            words = []
        body = re.sub(r"<[^>]*>", " ", text)
        words += [w for w in (VoynichParser.clean_token(t) for t in re.split(r"[.,\s]+", body)) if w]
        if "<$>" in text:
            runs[run].append(Counter(root_of(w) for w in words))
            words = []
    return runs


def main():
    runs = paragraphs()
    vocab = sorted(set().union(*[c for r in runs for c in r]))
    idx = {v: i for i, v in enumerate(vocab)}
    mats = []
    for r in runs:
        M = np.zeros((len(r), len(vocab)))
        for i, c in enumerate(r):
            for k, v in c.items():
                M[i, idx[k]] = v
        M /= np.linalg.norm(M, axis=1, keepdims=True)
        mats.append(M @ M.T)

    def sims(orders):
        out = np.zeros(len(LAGS))
        for j, L in enumerate(LAGS):
            vals = []
            for S, o in zip(mats, orders):
                n = len(o)
                if n > L:
                    vals.append(S[o[:-L], o[L:]])
            out[j] = np.concatenate(vals).mean()
        return out

    def peaks(s):
        return {L: s[LAGS.index(L)] - (s[LAGS.index(L - 1)] + s[LAGS.index(L + 1)]) / 2 for L in range(2, 41)}

    ident = [np.arange(len(m)) for m in mats]
    obs_s = sims(ident)
    obs = peaks(obs_s)
    rng = np.random.default_rng(SEED)
    null = {L: np.empty(N_PERMS) for L in obs}
    null_month = np.empty(N_PERMS)
    for i in range(N_PERMS):
        pk = peaks(sims([rng.permutation(len(m)) for m in mats]))
        for L in obs:
            null[L][i] = pk[L]
        null_month[i] = max(pk[L] for L in range(27, 32))
    pval = lambda nul, o: float((np.sum(nul >= o) + 1) / (N_PERMS + 1))
    p7 = pval(null[7], obs[7])
    month_obs = max(obs[L] for L in range(27, 32))
    pm = pval(null_month, month_obs)
    scan = {L: pval(null[L], obs[L]) for L in obs}
    bonf = ALPHA / len(scan)
    hits = [L for L, p in scan.items() if p < bonf]
    L_ = ["# Do the star-marked paragraphs repeat in cycles?", "",
          f"Pre-registration: `analyses/cycles_prereg.md`. Paragraphs: {len(runs[0])} (f103–f108) + {len(runs[1])} "
          f"(f111–f116); {N_PERMS:,} order shuffles, seed {SEED}.", "",
          f"- **C1 week (lag 7):** peak {obs[7]:+.4f}, p = {p7:.3g} → **{'PASS' if p7 < ALPHA else 'FAIL'}**",
          f"- **C2 month (lags 27–31):** best peak {month_obs:+.4f}, p = {pm:.3g} → **{'PASS' if pm < ALPHA else 'FAIL'}**",
          f"- **C3 any cycle (2–40, Bonferroni p < {bonf:.5f}):** {', '.join(map(str, hits)) if hits else 'none'}", "",
          "## Similarity by spacing (descriptive)", "", "| Spacing | Mean similarity | Local peak | p |", "|---:|---:|---:|---:|"]
    for L in range(2, 41):
        L_.append(f"| {L} | {obs_s[LAGS.index(L)]:.4f} | {obs[L]:+.4f} | {scan[L]:.3g} |")
    L_.insert(9, f"- Similarity of neighbouring paragraphs (spacing 1): {obs_s[0]:.4f}; spacing 40: {obs_s[LAGS.index(40)]:.4f}")
    report = "\n".join(L_) + "\n"
    (ROOT / "output" / "cycles_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
