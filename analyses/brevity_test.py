#!/usr/bin/env python3
"""Do frequent words get shorter (Zipf's law of abbreviation)? (analyses/brevity_prereg.md)

    python analyses/brevity_test.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from comparison_fingerprint import LATIN_SOURCES, latin_words, verbose_cipher  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261003
N_HALF = 200
LATIN_DIR = ROOT.parent / "cltk" / "lat_text_latin_library"


def strength(tokens, min_count):
    c = Counter(tokens)
    types = [w for w, n in c.items() if n >= min_count]
    return -spearmanr([c[w] for w in types], [len(w) for w in types]).correlation, len(types)


def main():
    rng = np.random.default_rng(SEED)
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.clean.str.len() > 0)]
    texts = {"Voynich A": p[p.currier == "A"].clean.tolist(), "Voynich B": p[p.currier == "B"].clean.tolist()}
    first = None
    for name, globs in LATIN_SOURCES.items():
        files = sorted(f for g in globs for f in LATIN_DIR.glob(g))
        words = latin_words(" ".join(f.read_text(errors="ignore") for f in files))
        texts[name] = words
        first = first or words
    texts["cipher of Apicius"] = verbose_cipher(first, rng)
    N = min(len(v) for v in texts.values())
    res = {}
    for name, ws in texts.items():
        sample = list(rng.choice(ws, N, replace=False))
        s, n_types = strength(sample, 5)
        half = [strength(list(rng.choice(sample, N // 2, replace=False)), 3)[0] for _ in range(N_HALF)]
        res[name] = (s, *np.percentile(half, [2.5, 97.5]), n_types)
    v, lat = ["Voynich A", "Voynich B"], [k for k in res if k.startswith("latin")]
    if max(res[k][2] for k in v) < min(res[k][1] for k in lat):
        verdict = "NOTATION-LIKE (weaker law)"
    elif all(res[k][0] >= min(res[x][0] for x in lat) for k in v):
        verdict = "LANGUAGE-LIKE"
    else:
        verdict = "MIXED"
    L = ["# Do frequent words get shorter? (Zipf's law of abbreviation)", "",
         f"Pre-registration: `analyses/brevity_prereg.md`. Equal samples of N = {N:,} tokens; seed {SEED}.", "",
         "| Text | Types (5+ uses) | Strength −ρ (full sample) | Half-sample interval |", "|---|---:|---:|---|"]
    for k, (s, lo, hi, n) in res.items():
        L.append(f"| {k} | {n} | {s:.3f} | {lo:.3f}–{hi:.3f} |")
    L += ["", f"**Verdict: {verdict}.**"]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "brevity_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
