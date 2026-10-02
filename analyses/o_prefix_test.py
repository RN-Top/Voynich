#!/usr/bin/env python3
"""Is "o" a label/name-forming prefix? (analyses/o_prefix_prereg.md)

    python analyses/o_prefix_test.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from plant_star_test import show, words_of  # noqa: E402
from parser import CORPUS_PATH  # noqa: E402

SEED = 20261002
N_PERMS = 10_000
ALPHA = 0.01
GROUP = {"Ls": "stars", "Lz": "zodiac figures", "Ln": "bathing figures", "Lt": "pools/tubes", "Lc": "jars",
         "Lf": "plant parts"}


def main():
    label_types, label_group = set(), defaultdict(set)
    para_tokens = []  # (word, is_line_first, is_para_first)
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.(\d+),(.)(\w+)>\s+(.*)", line)
        if not m:
            continue
        start, code, ws = m.group(3) == "@", m.group(4), words_of(m.group(5))
        if code.startswith("L"):
            for w in ws:
                label_types.add(w)
                label_group[w].add(GROUP.get(code, "other"))
        elif code.startswith("P"):
            for i, w in enumerate(ws):
                para_tokens.append((w, i == 0, i == 0 and start))
    para_vocab = {w for w, _, _ in para_tokens}
    is_o = lambda w: w.startswith("o") and len(w) >= 4
    labs = sorted(w for w in label_types if is_o(w))
    paras = sorted(w for w in para_vocab if is_o(w) and w not in label_types)
    words = labs + paras
    hit = np.array([w[1:] in para_vocab for w in words])
    is_lab = np.array([True] * len(labs) + [False] * len(paras))
    lengths = np.array([len(w) for w in words])
    obs = int(hit[is_lab].sum())
    rng = np.random.default_rng(SEED)
    groups = [np.flatnonzero(lengths == L) for L in np.unique(lengths)]
    null = np.empty(N_PERMS)
    for i in range(N_PERMS):
        lab = is_lab.copy()
        for g in groups:
            lab[g] = is_lab[g][rng.permutation(len(g))]
        null[i] = hit[lab].sum()
    p = float((np.sum(null >= obs) + 1) / (N_PERMS + 1))

    # Descriptive
    by_group = defaultdict(lambda: [0, 0])
    for w in labs:
        for g in label_group[w]:
            by_group[g][0] += w[1:] in para_vocab
            by_group[g][1] += 1
    rem = Counter(w[1:] for w in labs if w[1:] in para_vocab)
    pos = defaultdict(lambda: [0, 0, 0])
    for w, lf, pf in para_tokens:
        d = pos[w]
        d[0] += 1
        d[1] += lf
        d[2] += pf
    tot = [sum(v[i] for v in pos.values()) for i in range(3)]
    rems = set(rem)
    rt = [sum(pos[w][i] for w in rems) for i in range(3)]
    L = ['# Is "o" a label/name-forming prefix?', "",
         f"Pre-registration: `analyses/o_prefix_prereg.md`. {N_PERMS:,} shuffles within word length, seed {SEED}.", "",
         f"- Label words starting with o (4+ letters): {len(labs)}; of these, **{obs} ({obs / len(labs):.0%})** are "
         f"o + an existing paragraph word.",
         f"- Paragraph-only words starting with o: {len(paras)}; of these, {int(hit[~is_lab].sum())} "
         f"({hit[~is_lab].mean():.0%}) are o + an existing word.",
         f"- Expected for labels at the same lengths: {null.mean():.1f}",
         f"- p = {p:.3g} → **{'SUPPORTED' if p < ALPHA else 'NOT SUPPORTED'}**", "",
         "## By label group (descriptive)", "", "| Group | o-words | o + existing word | Rate |", "|---|---:|---:|---:|"]
    for g, (h, n) in sorted(by_group.items(), key=lambda kv: -kv[1][1]):
        L.append(f"| {g} | {n} | {h} | {h / n:.0%} |")
    L += ["", f"Paragraph-only o-words for comparison: {hit[~is_lab].mean():.0%}.", "",
          "## Where the remainders occur in paragraph text (descriptive)", "",
          f"- Remainders: share of their paragraph uses that are line-first {rt[1] / rt[0]:.1%}, paragraph-first "
          f"{rt[2] / rt[0]:.1%}",
          f"- All paragraph words: line-first {tot[1] / tot[0]:.1%}, paragraph-first {tot[2] / tot[0]:.1%}", "",
          "Most common remainders (label = o + remainder): " +
          ", ".join(f"{show(r)} ({c})" for r, c in rem.most_common(15))]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "o_prefix_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
