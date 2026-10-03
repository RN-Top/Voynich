#!/usr/bin/env python3
"""Scribe vs topic, and whether the rules hold for every scribe. (analyses/scribes_prereg.md)

    python analyses/scribes_test.py
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
sys.path.insert(0, str(ROOT / "analyses"))

import phrases_test as pt  # noqa: E402
import writing_types_test as wt  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402
from root_dictionary_test import mi, root_of  # noqa: E402

SEED = 20261003
N_PAGE = 2000
ALPHA = 0.01


def hands():
    h = {}
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.>]+)>\s+<!(.*)>", line)
        if m:
            x = re.search(r"\$H=(\d)", m.group(2))
            h[m.group(1)] = x.group(1) if x else None
    return h


def page_test(sub: pd.DataFrame, label: str, rng):
    """MI between root and a page-level label, with labels shuffled among pages."""
    cnt = sub.root.value_counts()
    r5 = sub.root.where(sub.root.map(cnt) >= 5, "<rare>")
    pages = sub.groupby("folio")[label].first()
    codes, names = pd.factorize(pages)
    F = pd.crosstab(sub.folio, r5).reindex(pages.index).to_numpy(float)

    def stat(a):
        J = np.zeros((len(names), F.shape[1]))
        np.add.at(J, a, F)
        return mi(J)

    obs = stat(codes)
    null = np.array([stat(codes[rng.permutation(len(codes))]) for _ in range(N_PAGE)])
    return {"pages": len(pages), "groups": ", ".join(f"{n} ({(pages == n).sum()})" for n in names), "mi": obs,
            "null": float(null.mean()), "excess": obs - float(null.mean()),
            "p": float((np.sum(null >= obs) + 1) / (N_PAGE + 1))}


def main():
    hd = hands()
    df = parse_zl3b(CORPUS_PATH)
    df["hand"] = df.folio.map(hd)
    p = df[(df.locus_type == "P") & (df.clean.str.len() > 0) & df.hand.notna()].copy()
    p["root"] = p.clean.map(root_of)
    rng = np.random.default_rng(SEED)
    L = ["# Scribe vs topic", "", f"Pre-registration: `analyses/scribes_prereg.md`. Seed {SEED}.", "",
         "## Who wrote what (paragraph words)", "",
         "```", p.groupby(["hand", "section"]).size().unstack(fill_value=0).to_string(), "```", "",
         "## S1. Writer effect, topic fixed (herbal pages only)", ""]
    s1 = page_test(p[p.section == "Herbal"], "hand", rng)
    L.append(f"- Scribes: {s1['groups']}. Root–scribe information {s1['mi']:.4f} vs shuffled {s1['null']:.4f} "
             f"(excess {s1['excess']:.4f}); p = {s1['p']:.3g} → **{'PASS' if s1['p'] < ALPHA else 'FAIL'}**")
    L += ["", "## S2. Topic effect, writer fixed", ""]
    s2_pass = []
    for h in ("1", "2", "3"):
        sub = p[p.hand == h]
        sizes = sub.section.value_counts()
        keep = sizes[sizes >= 500].index
        sub = sub[sub.section.isin(keep)]
        if len(keep) < 2:
            continue
        r = page_test(sub, "section", rng)
        ok = r["p"] < ALPHA / 3
        s2_pass.append(ok)
        L.append(f"- Scribe {h}: {r['groups']}. Root–section information {r['mi']:.4f} vs {r['null']:.4f} "
                 f"(excess {r['excess']:.4f}); p = {r['p']:.3g} → **{'PASS' if ok else 'FAIL'}**")
    L.append(f"- **Topic effect confirmed with writer fixed: {'YES' if any(s2_pass) else 'NO'}**")
    L += ["", "## S3. Do the rules hold for every scribe?", "",
          "| Scribe | Interior pairs | Word order excess (bits) | p | Strongest link | Its p |", "|---|---:|---:|---:|---|---:|"]
    wt.N_W1, pt.N_PERMS = 1000, 500
    universal = True
    for h in sorted(p.hand.unique()):
        g = p[p.hand == h]
        r1 = wt.w1(g, rng)
        if r1 is None:
            L.append(f"| {h} | <1500 | | | too little text | |")
            continue
        r2 = pt.analyse(g, rng, h)["r2"]
        best = max(r2, key=lambda k: r2[k]["excess"])
        ok = r1["p"] < ALPHA and best == "ending->beginning" and r2[best]["p"] < ALPHA
        universal &= ok
        L.append(f"| {h} | {r1['pairs']:,} | {r1['excess']:.4f} | {r1['p']:.3g} | {best.replace('->', ' → ')} | "
                 f"{r2[best]['p']:.3g} |")
    L.append(f"\n**Rules universal across qualifying scribes: {'YES' if universal else 'NO'}**")
    L += ["", "## Scribe profiles (descriptive)", "",
          "| Scribe | Words | Mean length | Common beginnings | Common endings |", "|---|---:|---:|---|---|"]
    for h in sorted(p.hand.unique()):
        w = p[p.hand == h].clean
        b, e = Counter(x[:2] for x in w), Counter(x[-2:] for x in w)
        L.append(f"| {h} | {len(w):,} | {w.str.len().mean():.2f} | "
                 f"{', '.join(f'{k}- {v / len(w):.0%}' for k, v in b.most_common(4))} | "
                 f"{', '.join(f'-{k} {v / len(w):.0%}' for k, v in e.most_common(4))} |")
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "scribes_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
