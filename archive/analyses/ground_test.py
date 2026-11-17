#!/usr/bin/env python3
"""Does a page's paragraph text mention that page's labels? (analyses/ground_prereg.md)

    python analyses/ground_test.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, VoynichParser, parse_zl3b  # noqa: E402

SEED = 20261002
N_PERMS = 10_000
ALPHA = 0.01
MIN_LEN = 3


def main():
    df = parse_zl3b(CORPUS_PATH)
    para = df[(df.locus_type == "P") & (df.clean.str.len() > 0)]
    page_vocab = para.groupby("folio")["clean"].agg(set).to_dict()
    section = df.groupby("folio")["section"].first().to_dict()

    labels = []  # (page, [words])
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.(L\w)>\s+(.*)", line)
        if not m or m.group(1) not in page_vocab:
            continue
        text = re.sub(r"<[^>]*>", "", m.group(3))
        words = sorted({w for w in (VoynichParser.clean_token(t) for t in re.split(r"[.,\s]+", text)) if len(w) >= MIN_LEN})
        if words:
            labels.append((m.group(1), words))

    def run(subset_sections, rng):
        lab = [(p, ws) for p, ws in labels if section.get(p) in subset_sections]
        pages = np.array([p for p, _ in lab])
        secs = np.array([section[p] for p in pages])

        def score(assign):
            return sum(sum(w in page_vocab[pg] for w in ws) for pg, (_, ws) in zip(assign, lab))

        obs = score(pages)
        null = np.empty(N_PERMS)
        groups = [np.flatnonzero(secs == s) for s in np.unique(secs)]
        for i in range(N_PERMS):
            a = pages.copy()
            for g in groups:
                a[g] = pages[g][rng.permutation(len(g))]
            null[i] = score(a)
        hits = sorted({(p, w) for p, ws in lab for w in ws if w in page_vocab[p]})
        return {"labels": len(lab), "words": sum(len(ws) for _, ws in lab), "pages": len(set(pages)),
                "obs": obs, "null_mean": float(null.mean()),
                "p": float((np.sum(null >= obs) + 1) / (N_PERMS + 1)), "hits": hits}

    rng = np.random.default_rng(SEED)
    all_secs = {section[p] for p, _ in labels}
    res = {"G1 bath pages (Biological)": run({"Biological"}, rng),
           "G2 all sections": run(all_secs, rng)}
    L = ["# Does a page's text mention that page's labels? (ground test)", "",
         f"Pre-registration: `analyses/ground_prereg.md`. {N_PERMS:,} shuffles within section, seed {SEED}.", "",
         "| Test | Labels | Label words | Pages | Found in own page's text | Shuffled mean | p | Result |",
         "|---|---:|---:|---:|---:|---:|---:|---|"]
    for name, r in res.items():
        L.append(f"| {name} | {r['labels']} | {r['words']} | {r['pages']} | {r['obs']} | {r['null_mean']:.1f} | "
                 f"{r['p']:.3g} | {'PASS' if r['p'] < ALPHA else 'FAIL'} |")
    found = any(r["p"] < ALPHA for r in res.values())
    L += ["", f"**Verdict: {'SUPPORTED (ground found)' if found else 'NOT SUPPORTED'}.**", ""]
    for name, r in res.items():
        by_page = defaultdict(list)
        for p, w in r["hits"]:
            by_page[p].append(w)
        L.append(f"**{name}, label words found in their own page's text:** " +
                 ("; ".join(f"{p}: {', '.join(ws)}" for p, ws in sorted(by_page.items())) or "none"))
        L.append("")
    report = "\n".join(L)
    (ROOT / "output" / "ground_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
