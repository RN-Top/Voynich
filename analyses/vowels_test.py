#!/usr/bin/env python3
"""Do the Voynich symbols alternate like vowels and consonants? (analyses/vowels_prereg.md)

    python analyses/vowels_test.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from comparison_fingerprint import LATIN_SOURCES, latin_words  # noqa: E402
from freqmatch_test import units  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261003
N_SHUF = 20
LATIN_DIR = ROOT.parent / "cltk" / "lat_text_latin_library"


def sukhotin(words):
    syms = sorted({s for w in words for s in w})
    ix = {s: i for i, s in enumerate(syms)}
    M = np.zeros((len(syms), len(syms)))
    for w in words:
        for a, b in zip(w, w[1:]):
            if a != b:
                M[ix[a], ix[b]] += 1
                M[ix[b], ix[a]] += 1
    sums = M.sum(1).astype(float)
    vowels = set()
    while True:
        cand = [i for i in range(len(syms)) if i not in vowels]
        if not cand:
            break
        v = max(cand, key=lambda i: sums[i])
        if sums[v] <= 0:
            break
        vowels.add(v)
        for i in cand:
            if i != v:
                sums[i] -= 2 * M[i, v]
    return {syms[i] for i in vowels}


def alternation(words, vowels):
    alt = tot = 0
    for w in words:
        for a, b in zip(w, w[1:]):
            tot += 1
            alt += (a in vowels) != (b in vowels)
    return alt / tot if tot else float("nan")


def excess(words, rng):
    v = sukhotin(words)
    real = alternation(words, v)
    sh = []
    for _ in range(N_SHUF):
        s = [list(rng.permutation(w)) for w in words]
        sh.append(alternation(s, sukhotin(s)))
    return real, float(np.mean(sh)), real - float(np.mean(sh)), v


def main():
    rng = np.random.default_rng(SEED)
    lat = []
    for name, globs in LATIN_SOURCES.items():
        files = sorted(f for g in globs for f in LATIN_DIR.glob(g))
        lat += latin_words(" ".join(f.read_text(errors="ignore") for f in files))
    lat = [list(w) for w in lat[:100_000]]
    lr, ls, le, lv = excess(lat, rng)
    ok = len(lv & set("aeiou")) >= 4
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.clean.str.len() > 0)]
    L = ["# Do the Voynich symbols alternate like vowels and consonants? (Sukhotin)", "",
         f"Pre-registration: `analyses/vowels_prereg.md`. Shuffled baseline: letters shuffled within words, "
         f"{N_SHUF} times; seed {SEED}.", "",
         "| Text | Vowels found | Alternation | Shuffled | Excess | Ratio to Latin |", "|---|---|---:|---:|---:|---:|",
         f"| Latin (control) | {' '.join(sorted(lv))} | {lr:.3f} | {ls:.3f} | {le:.3f} | 1.00 |"]
    ratios = []
    for cur in ("A", "B"):
        words = p[p.currier == cur].clean.tolist()
        for scheme in ("S1", "S2"):
            ws = [units(w, scheme) for w in words]
            r, s, e, v = excess(ws, rng)
            ratios.append(e / le)
            L.append(f"| Voynich {cur} {scheme} | {' '.join(sorted(v))} | {r:.3f} | {s:.3f} | {e:.3f} | {e / le:.2f} |")
    if not ok:
        verdict = "UNINFORMATIVE (control failed)"
    elif all(x >= 0.5 for x in ratios):
        verdict = "ALPHABET-LIKE"
    elif all(x < 0.5 for x in ratios):
        verdict = "NOT ALPHABET-LIKE"
    else:
        verdict = "MIXED"
    L += ["", f"Control: Latin vowels found {'include' if ok else 'do NOT include'} at least 4 of a e i o u.", "",
          f"**Verdict: {verdict}.**"]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "vowels_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
