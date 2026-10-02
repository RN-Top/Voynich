#!/usr/bin/env python3
"""Root dictionary: which word cores belong to which section? (analyses/root_dictionary_prereg.md)

    python analyses/root_dictionary_test.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import structural_validation as sv  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261002
N_PERMS = 2000
ALPHA, FDR = 0.01, 0.05
ENDS = sorted(sv.ENDINGS, key=len, reverse=True)


def root_of(w: str) -> str:
    for p in ("q", "o", "y"):
        if w.startswith(p) and len(w) > 1:
            w = w[1:]
    for e in ENDS:
        if w.endswith(e):
            w = w[: -len(e)]
            break
    return w or "∅"


def mi(t):
    t = t / t.sum()
    px, py = t.sum(1, keepdims=True), t.sum(0, keepdims=True)
    m = t > 0
    return float(np.sum(t[m] * np.log2(t[m] / (px @ py)[m])))


def main():
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.clean.str.len() > 0)].copy()
    p["root"] = p.clean.map(root_of)
    cnt = p.root.value_counts()
    p["root5"] = p.root.where(p.root.map(cnt) >= 5, "<rare>")
    folio = p.groupby("folio").agg(section=("section", "first"), currier=("currier", lambda s: s.mode()[0]))
    sec_codes, sec_names = pd.factorize(folio.section)
    F = pd.crosstab(p.folio, p.root5).reindex(folio.index)
    roots = list(F.columns)
    Fm = F.to_numpy(float)
    groups = [np.flatnonzero(folio.currier.to_numpy() == c) for c in folio.currier.unique()]

    def joint(assign):
        J = np.zeros((len(sec_names), Fm.shape[1]))
        np.add.at(J, assign, Fm)
        return J

    big = [i for i, r in enumerate(roots) if r != "<rare>" and cnt[r] >= 10]
    J0 = joint(sec_codes)
    obs_mi = mi(J0)
    obs_share = J0[:, big].max(0) / J0[:, big].sum(0)
    rng = np.random.default_rng(SEED)
    null_mi = np.empty(N_PERMS)
    ge = np.zeros(len(big))
    for i in range(N_PERMS):
        a = sec_codes.copy()
        for g in groups:
            a[g] = sec_codes[g][rng.permutation(len(g))]
        J = joint(a)
        null_mi[i] = mi(J)
        ge += (J[:, big].max(0) / J[:, big].sum(0)) >= obs_share - 1e-12
    p_mi = float((np.sum(null_mi >= obs_mi) + 1) / (N_PERMS + 1))
    p_root = (ge + 1) / (N_PERMS + 1)
    order = np.argsort(p_root)
    m = len(p_root)
    passed = np.zeros(m, bool)
    k = max([r + 1 for r in range(m) if p_root[order[r]] <= FDR * (r + 1) / m], default=0)
    passed[order[:k]] = True

    L = ["# Root dictionary", "", f"Pre-registration: `analyses/root_dictionary_prereg.md`. {N_PERMS:,} page shuffles "
         f"within Currier language, seed {SEED}. Paragraph text, {len(p):,} words, {p.root.nunique():,} distinct roots.", "",
         "## T1. Do roots follow the topic?", "",
         f"- Root–section information: {obs_mi:.4f} bits; shuffled {null_mi.mean():.4f}; p = {p_mi:.3g} → "
         f"**{'PASS' if p_mi < ALPHA else 'FAIL'}**", "",
         f"## T2. Section roots (FDR 5%; {int(passed.sum())} of {m} roots with 10+ uses)", "",
         "| Root | Uses | Main section | Share there | Section's share of text | p | Example words |",
         "|---|---:|---|---:|---:|---:|---|"]
    sec_share = p.section.value_counts(normalize=True)
    for j in order:
        if not passed[j]:
            continue
        r = roots[big[j]]
        s = sec_names[int(J0[:, big[j]].argmax())]
        ex = ", ".join(w for w, _ in Counter(p.clean[p.root == r]).most_common(4))
        L.append(f"| {r} | {cnt[r]} | {s} | {obs_share[j]:.0%} | {sec_share[s]:.0%} | {p_root[j]:.3g} | {ex} |")

    # Descriptive: roots shared by herbal openings and star labels (canonical clean words).
    import re
    from parser import VoynichParser
    star, opening = set(), {}
    section = df.groupby("folio")["section"].first().to_dict()
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        mm = re.match(r"<(f[^.]+)\.\d+,.(\w+)>\s+(.*)", line)
        if not mm:
            continue
        ws = [VoynichParser.clean_token(t) for t in re.split(r"[.,\s]+", re.sub(r"<[^>]*>", "", mm.group(3)))]
        ws = [w for w in ws if w]
        if mm.group(2) == "Ls":
            star.update(root_of(w) for w in ws)
        elif mm.group(2).startswith("P") and section.get(mm.group(1)) == "Herbal" and mm.group(1) not in opening and ws:
            opening[mm.group(1)] = ws[0]
    shared = sorted({root_of(w) for w in opening.values()} & star - {"∅"})
    L += ["", "## Roots in both herbal openings and star labels (descriptive)", "",
          ", ".join(f"{r} ({cnt.get(r, 0)} uses in paragraphs)" for r in shared) or "none"]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "root_dictionary_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
