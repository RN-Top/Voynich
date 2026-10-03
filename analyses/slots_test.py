#!/usr/bin/env python3
"""Do word parts combine freely (code-like) or under restrictions (language-like)? (analyses/slots_prereg.md)

    python analyses/slots_test.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from comparison_fingerprint import LATIN_SOURCES, latin_words, verbose_cipher  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261003
N_SHUF, N_BOOT = 200, 200
LATIN_DIR = ROOT.parent / "cltk" / "lat_text_latin_library"


def H(c):
    p = np.array(list(c.values()), float)
    p /= p.sum()
    return float(-(p * np.log2(p)).sum())


def mi(a, b):
    ai, bi = pd.factorize(a)[0], pd.factorize(b)[0]
    nb = bi.max() + 1
    j = np.bincount(ai * nb + bi)
    nz = np.flatnonzero(j)
    pxy = j[nz] / len(ai)
    px, py = np.bincount(ai) / len(ai), np.bincount(bi) / len(ai)
    return float(np.sum(pxy * np.log2(pxy / (px[nz // nb] * py[nz % nb]))))


def dependence(words, rng):
    s = np.array([w[:2] for w in words])
    e = np.array([w[-2:] for w in words])
    base = np.mean([mi(s, rng.permutation(e)) for _ in range(N_SHUF)])
    return (mi(s, e) - base) / min(H(Counter(s)), H(Counter(e)))


def main():
    rng = np.random.default_rng(SEED)
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.clean.str.len() >= 5)]
    texts = {"Voynich A": p[p.currier == "A"].clean.tolist(), "Voynich B": p[p.currier == "B"].clean.tolist()}
    first = None
    for name, globs in LATIN_SOURCES.items():
        files = sorted(f for g in globs for f in LATIN_DIR.glob(g))
        words = latin_words(" ".join(f.read_text(errors="ignore") for f in files))
        texts[name] = [w for w in words if len(w) >= 5]
        first = first or words
    texts["cipher of Apicius"] = [w for w in verbose_cipher(first, rng) if len(w) >= 5]
    N = min(len(v) for v in texts.values())
    res = {}
    for name, ws in texts.items():
        sample = list(rng.choice(ws, N, replace=False))
        d = dependence(sample, rng)
        boots = [dependence(list(rng.choice(sample, N, replace=True)), rng) for _ in range(N_BOOT // 10)]
        lo, hi = np.percentile(boots, [2.5, 97.5])
        res[name] = (d, lo, hi, len(ws))
    lat = [k for k in res if k.startswith("latin")]
    vmax = max(res[k][2] for k in ("Voynich A", "Voynich B"))
    lmin_lo = min(res[k][1] for k in lat)
    lat_min = min(res[k][0] for k in lat)
    if vmax < lmin_lo:
        verdict = "CODE-LIKE (freer slots)"
    elif all(res[k][0] >= lat_min for k in ("Voynich A", "Voynich B")):
        verdict = "LANGUAGE-LIKE"
    else:
        verdict = "MIXED"
    L = ["# Do word parts combine freely or under restrictions?", "",
         f"Pre-registration: `analyses/slots_prereg.md`. Words of 5+ letters; equal samples of N = {N:,} tokens; "
         f"start = first 2 letters, end = last 2 letters. Seed {SEED}.", "",
         "| Text | Eligible tokens | Dependence (0 = free) | 95% interval |", "|---|---:|---:|---|"]
    for k, (d, lo, hi, n) in res.items():
        L.append(f"| {k} | {n:,} | {d:.3f} | {lo:.3f}–{hi:.3f} |")
    L += ["", f"**Verdict: {verdict}.**"]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "slots_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
