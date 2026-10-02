#!/usr/bin/env python3
"""
Do word beginnings follow what a label is attached to? (analyses/dictionary_prereg.md)

    python analyses/dictionary_test.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, VoynichParser, parse_zl3b  # noqa: E402

SEED = 20261002
N_PERMS = 10_000
ALPHA_EACH = 0.005
KINDS = {"Lc": "jar", "Lf": "plant part", "Ln": "bathing figure", "Lt": "pool / tube"}
TESTS = {"D1 pharmaceutical: jar vs plant part": ("Lc", "Lf"),
         "D2 biological: figure vs pool/tube": ("Ln", "Lt")}


def labels() -> pd.DataFrame:
    rows = []
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.(L\w)>\s+(.*)", line)
        if not m or m.group(2) not in KINDS:
            continue
        text = re.sub(r"<[^>]*>", "", m.group(3)).strip()
        word = VoynichParser.clean_token(re.split(r"[.,\s]+", text)[0]) if text else ""
        if len(word) >= 2:
            rows.append({"folio": m.group(1), "code": m.group(2), "word": word,
                         "beginning": word[:2], "ending": word[-2:]})
    return pd.DataFrame(rows)


def mi(a: np.ndarray, b: np.ndarray) -> float:
    ai, bi = pd.factorize(a)[0], pd.factorize(b)[0]
    t = np.bincount(ai * (bi.max() + 1) + bi, minlength=(ai.max() + 1) * (bi.max() + 1)).astype(float)
    t = t.reshape(ai.max() + 1, bi.max() + 1) / len(ai)
    px, py = t.sum(1, keepdims=True), t.sum(0, keepdims=True)
    m = t > 0
    return float(np.sum(t[m] * np.log2(t[m] / (px @ py)[m])))


def perm_test(sub: pd.DataFrame, col: str, rng) -> dict:
    kinds = sub["code"].to_numpy()
    obs = mi(sub[col].to_numpy(), kinds)
    groups = [np.flatnonzero(sub["folio"].to_numpy() == f) for f in sub["folio"].unique()]
    null = np.empty(N_PERMS)
    for i in range(N_PERMS):
        k = kinds.copy()
        for g in groups:
            k[g] = kinds[g][rng.permutation(len(g))]
        null[i] = mi(sub[col].to_numpy(), k)
    return {"mi": obs, "null_mean": float(null.mean()), "p": float((np.sum(null >= obs) + 1) / (N_PERMS + 1))}


def over_represented(sub: pd.DataFrame, code: str, n=5):
    inside = Counter(sub.loc[sub.code == code, "beginning"])
    total = Counter(sub["beginning"])
    share = (sub.code == code).mean()
    rows = [(b, c, c / (total[b] * share)) for b, c in inside.items() if c >= 3]
    rows.sort(key=lambda r: -r[2])
    return ", ".join(f"{b}- ({c}, x{r:.1f})" for b, c, r in rows[:n]) or "none with 3+"


def section_beginnings(n=4):
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.clean.str.len() >= 2)].copy()
    p["beginning"] = p["clean"].str[:2]
    out = {}
    for (cur, sec), g in p.groupby(["currier", "section"]):
        if len(g) < 500:
            continue
        lang = p[p.currier == cur]
        base = lang["beginning"].value_counts(normalize=True)
        c = g["beginning"].value_counts()
        c = c[c >= 20]
        ratio = (c / len(g)) / base[c.index]
        out[f"{sec} ({cur})"] = ", ".join(f"{b}- (x{r:.1f})" for b, r in ratio.sort_values(ascending=False).head(n).items())
    return out


def main():
    lab = labels()
    rng = np.random.default_rng(SEED)
    lines = ["# Do word beginnings follow what a label is attached to?", "",
             f"Pre-registration: `analyses/dictionary_prereg.md`. {N_PERMS:,} within-page shuffles, seed {SEED}.", "",
             "| Test | Labels | Beginning MI | Shuffled | p | Result | Ending MI | Shuffled | p |",
             "|---|---:|---:|---:|---:|---|---:|---:|---:|"]
    passed = 0
    for name, codes in TESTS.items():
        sub = lab[lab.code.isin(codes)].reset_index(drop=True)
        b, e = perm_test(sub, "beginning", rng), perm_test(sub, "ending", rng)
        ok = b["p"] < ALPHA_EACH
        passed += ok
        counts = " / ".join(f"{(sub.code == c).sum()} {KINDS[c]}" for c in codes)
        lines.append(f"| {name} | {counts} | {b['mi']:.3f} | {b['null_mean']:.3f} | {b['p']:.3g} | "
                     f"{'PASS' if ok else 'FAIL'} | {e['mi']:.3f} | {e['null_mean']:.3f} | {e['p']:.3g} |")
    verdict = {2: "SUPPORTED", 1: "PARTLY SUPPORTED", 0: "NOT SUPPORTED"}[passed]
    lines += ["", f"**Verdict: {verdict}** (each test needs p < {ALPHA_EACH}).", "",
              "## Candidate dictionary leads (descriptive, not tested)", "",
              "Beginnings most over-represented on each picture kind (count, times expected):", ""]
    for name, codes in TESTS.items():
        sub = lab[lab.code.isin(codes)]
        for c in codes:
            lines.append(f"- **{KINDS[c]}**: {over_represented(sub, c)}")
    lines += ["", "Beginnings most concentrated in each section of paragraph text, relative to the same Currier "
              "language (at least 20 uses):", ""]
    for sec, s in section_beginnings().items():
        lines.append(f"- **{sec}**: {s}")
    report = "\n".join(lines) + "\n"
    (ROOT / "output" / "dictionary_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
