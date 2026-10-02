#!/usr/bin/env python3
"""Longer repeated phrases (refrains). Pre-registration: analyses/refrains_prereg.md

    python analyses/refrains_test.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261002
N_PERMS = 1000
ALPHA = 0.005
SPECS = {"L1": (3, 3), "L2": (4, 2)}  # name: (length, minimum occurrences)


def ngram_keys(codes, line, n, V):
    T = len(codes)
    ok = np.ones(T - n + 1, bool)
    for j in range(1, n):
        ok &= line[j:T - n + 1 + j] == line[:T - n + 1]
    key = np.zeros(T - n + 1, np.int64)
    distinct = np.zeros(T - n + 1, bool)
    for j in range(n):
        key = key * V + codes[j:T - n + 1 + j]
        if j:
            distinct |= codes[j:T - n + 1 + j] != codes[:T - n + 1]
    keep = ok & distinct
    return key[keep], np.flatnonzero(keep)


def count_repeated(codes, line, n, k, V):
    key, _ = ngram_keys(codes, line, n, V)
    _, cnt = np.unique(key, return_counts=True)
    return int((cnt >= k).sum())


def analyse(g, rng):
    g = g.reset_index(drop=True)
    codes, vocab = pd.factorize(g["clean"])
    codes = codes.astype(np.int64)
    V = len(vocab)
    line = pd.factorize(g["folio"] + "|" + g["header"])[0]
    obs = {name: count_repeated(codes, line, n, k, V) for name, (n, k) in SPECS.items()}
    null = {name: np.empty(N_PERMS) for name in SPECS}
    for i in range(N_PERMS):
        order = np.lexsort((rng.random(len(codes)), line))
        s = codes[order]
        for name, (n, k) in SPECS.items():
            null[name][i] = count_repeated(s, line, n, k, V)
    res = {name: {"obs": obs[name], "null_mean": float(null[name].mean()),
                  "p": float((np.sum(null[name] >= obs[name]) + 1) / (N_PERMS + 1))} for name in SPECS}
    # descriptive: top sequences and where they occur
    sec = g["section"].to_numpy()
    sec_share = g["section"].value_counts(normalize=True)
    tops = {}
    for name, (n, k) in SPECS.items():
        key, start = ngram_keys(codes, line, n, V)
        c = Counter(key.tolist())
        rep = [kk for kk, v in c.items() if v >= k]
        occ_secs = Counter(sec[start[np.isin(key, rep)]])
        tot = sum(occ_secs.values())
        top = []
        for kk, v in c.most_common(8):
            if v < k:
                break
            idx = start[np.flatnonzero(key == kk)[0]]
            top.append((" ".join(vocab[codes[idx:idx + n]]), v))
        tops[name] = {"top": top, "where": {s: (occ_secs[s] / tot if tot else 0, sec_share[s]) for s in sec_share.index}}
    return res, tops


def main():
    df = parse_zl3b(CORPUS_PATH)
    df = df[(df.locus_type == "P") & (df.clean.str.len() > 0)]
    rng = np.random.default_rng(SEED)
    out = {c: analyse(df[df.currier == c], rng) for c in ("A", "B")}
    L = ["# Longer repeated phrases (refrains)", "",
         f"Pre-registration: `analyses/refrains_prereg.md`. Paragraph text, {N_PERMS:,} within-line shuffles, seed {SEED}.",
         "Sequences of a single repeated word are excluded.", "",
         "| Text | Test | Repeated sequences | Shuffled mean | p | Result |", "|---|---|---:|---:|---:|---|"]
    for c, (res, _) in out.items():
        for name, (n, k) in SPECS.items():
            r = res[name]
            L.append(f"| Currier {c} | {name}: {n} words, {k}+ times | {r['obs']} | {r['null_mean']:.1f} | {r['p']:.3g} | "
                     f"{'PASS' if r['p'] < ALPHA else 'FAIL'} |")
    l2 = any(out[c][0]["L2"]["p"] < ALPHA for c in out)
    l1 = any(out[c][0]["L1"]["p"] < ALPHA for c in out)
    verdict = "SUPPORTED (longer refrains present)" if l2 else ("PARTLY SUPPORTED" if l1 else "NOT SUPPORTED")
    L += ["", f"**Verdict: {verdict}.**", ""]
    for c, (_, tops) in out.items():
        for name, (n, k) in SPECS.items():
            t = tops[name]
            L.append(f"**Currier {c}, {n}-word repeats:** " + ("; ".join(f"{s} ({v})" for s, v in t["top"]) or "none"))
            L.append("Where they occur (share of repeats vs share of text): " +
                     ", ".join(f"{s} {a:.0%} vs {b:.0%}" for s, (a, b) in t["where"].items()))
            L.append("")
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "refrains_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
