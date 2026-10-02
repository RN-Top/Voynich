#!/usr/bin/env python3
"""
Writing types, word order (W1) and topic location (W2).
Pre-registration: analyses/writing_types_prereg.md

    python analyses/writing_types_test.py
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
N_W1, N_W2 = 1000, 2000
MIN_COUNT, MIN_PAIRS, ALPHA = 5, 1500, 0.01


def mi_from_codes(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) == 0:
        return 0.0
    ny = y.max() + 1
    joint = np.bincount(x * ny + y)
    nz = np.flatnonzero(joint)
    pxy = joint[nz] / len(x)
    px = np.bincount(x) / len(x)
    py = np.bincount(y) / len(x)
    return float(np.sum(pxy * np.log2(pxy / (px[nz // ny] * py[nz % ny]))))


def mi_table(t: np.ndarray) -> float:
    t = t / t.sum()
    px, py = t.sum(1, keepdims=True), t.sum(0, keepdims=True)
    m = t > 0
    return float(np.sum(t[m] * np.log2(t[m] / (px @ py)[m])))


def types(df):
    return {
        "Paragraph, Currier A": df[(df.locus_type == "P") & (df.currier == "A")],
        "Paragraph, Currier B": df[(df.locus_type == "P") & (df.currier == "B")],
        "Ring text (C)": df[df.locus_type == "C"],
        "Labels (L)": df[df.locus_type == "L"],
        "Radial text (R)": df[df.locus_type == "R"],
    }


def profile(name, g, para_vocab):
    w = g["clean"]
    begins, ends = Counter(x[:2] for x in w), Counter(x[-2:] for x in w)
    return {
        "type": name, "words": len(w), "distinct": w.nunique(),
        "mean_len": round(w.str.len().mean(), 2),
        "top_beginnings": ", ".join(f"{k}- {v / len(w):.0%}" for k, v in begins.most_common(4)),
        "top_endings": ", ".join(f"-{k} {v / len(w):.0%}" for k, v in ends.most_common(4)),
        "in_other_paragraph_text": round(w.isin(para_vocab).mean(), 3),
    }


def w1(g, rng):
    g = g.reset_index(drop=True)
    counts = g["clean"].value_counts()
    words = g["clean"].where(g["clean"].map(counts) >= MIN_COUNT, "<rare>")
    codes = pd.factorize(words)[0]
    line = pd.factorize(g["folio"] + "|" + g["header"])[0]
    pos = g.groupby(line).cumcount().to_numpy()
    length = np.bincount(line)[line]
    interior = (pos >= 1) & (pos <= length - 2)
    pair = interior[:-1] & interior[1:] & (line[:-1] == line[1:])
    if pair.sum() < MIN_PAIRS:
        return None
    obs = mi_from_codes(codes[:-1][pair], codes[1:][pair])
    idx = np.flatnonzero(interior)
    grp = line[idx]
    null = np.empty(N_W1)
    for i in range(N_W1):
        s = codes.copy()
        s[idx] = codes[idx][np.lexsort((rng.random(len(idx)), grp))]
        null[i] = mi_from_codes(s[:-1][pair], s[1:][pair])
    return {"pairs": int(pair.sum()), "mi": obs, "null_mean": float(null.mean()),
            "excess": obs - float(null.mean()), "p": float((np.sum(null >= obs) + 1) / (N_W1 + 1))}


def w2(p, rng):
    folio = p.groupby("folio").agg(section=("section", "first"), currier=("currier", lambda s: s.mode()[0]))
    out = {}
    for part, fn in (("beginning", lambda x: x[:2]), ("ending", lambda x: x[-2:])):
        F = pd.crosstab(p["folio"], p["clean"].map(fn)).reindex(folio.index).to_numpy(float)
        sec_codes, sec_names = pd.factorize(folio["section"])

        def mi_for(assign):
            joint = np.zeros((len(sec_names), F.shape[1]))
            np.add.at(joint, assign, F)
            return mi_table(joint)

        obs = mi_for(sec_codes)
        null = np.empty(N_W2)
        groups = [np.flatnonzero(folio["currier"].to_numpy() == c) for c in folio["currier"].unique()]
        for i in range(N_W2):
            a = sec_codes.copy()
            for gidx in groups:
                a[gidx] = sec_codes[gidx][rng.permutation(len(gidx))]
            null[i] = mi_for(a)
        out[part] = {"mi": obs, "null_mean": float(null.mean()), "excess": obs - float(null.mean()),
                     "p": float((np.sum(null >= obs) + 1) / (N_W2 + 1)), "distinct": F.shape[1]}
    return out


def main():
    df = parse_zl3b(CORPUS_PATH)
    df = df[df["clean"].str.len() > 0]
    rng = np.random.default_rng(SEED)
    t = types(df)
    para = df[df.locus_type == "P"]
    profiles = []
    for name, g in t.items():
        other = para[para.currier != g["currier"].iloc[0]] if name.startswith("Paragraph") else para
        profiles.append(profile(name, g, set(other["clean"])))
    w1_res = {name: w1(g, rng) for name, g in t.items()}
    w2_res = w2(para, rng)

    lines = ["# Writing types, word order and topic location", "",
             "Pre-registration: `analyses/writing_types_prereg.md`. Seed " + str(SEED) + ".", "",
             "## Profiles", "",
             "| Type | Words | Distinct | Mean length | Common beginnings | Common endings | Words also in other paragraph text |",
             "|---|---:|---:|---:|---|---|---:|"]
    for r in profiles:
        lines.append(f"| {r['type']} | {r['words']:,} | {r['distinct']:,} | {r['mean_len']} | {r['top_beginnings']} | "
                     f"{r['top_endings']} | {r['in_other_paragraph_text']:.0%} |")
    lines += ["", "For the paragraph types, the last column compares A with B; for the others, with all paragraph text.", "",
              "## W1. Does word order carry information? (interior words only)", "",
              "| Type | Pairs | MI (bits) | Shuffled mean | Excess | p | Result |", "|---|---:|---:|---:|---:|---:|---|"]
    for name, r in w1_res.items():
        if r is None:
            lines.append(f"| {name} | <{MIN_PAIRS} | | | | | too small |")
        else:
            lines.append(f"| {name} | {r['pairs']:,} | {r['mi']:.4f} | {r['null_mean']:.4f} | {r['excess']:.4f} | "
                         f"{r['p']:.3g} | {'order matters' if r['p'] < ALPHA else 'no detectable order effect'} |")
    lines += ["", "## W2. Does the start or the end of a word carry the topic? (paragraph text)", "",
              "| Word part | Distinct values | MI with section | Shuffled mean | Excess | p |", "|---|---:|---:|---:|---:|---:|"]
    for part, r in w2_res.items():
        lines.append(f"| {part} | {r['distinct']} | {r['mi']:.4f} | {r['null_mean']:.4f} | {r['excess']:.4f} | {r['p']:.3g} |")
    passing = sorted([k for k, v in w2_res.items() if v["p"] < ALPHA], key=lambda k: -w2_res[k]["excess"])
    lines += ["", "**W2 result:** " + (" > ".join(passing) + " (larger excess first)" if passing else "no detectable topic signal")]
    report = "\n".join(lines) + "\n"
    (ROOT / "output" / "writing_types_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
