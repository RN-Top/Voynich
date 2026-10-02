#!/usr/bin/env python3
"""
Repeated phrases (R1) and grammar links (R2). Pre-registration: analyses/phrases_prereg.md

    python analyses/phrases_test.py
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
ALPHA = 0.01
MIN_COUNT, MIN_RATIO = 5, 3.0
LINKS = [("ending", "beginning"), ("ending", "ending"), ("beginning", "beginning"), ("beginning", "ending")]


def mi(x, y):
    ny = y.max() + 1
    joint = np.bincount(x * ny + y)
    nz = np.flatnonzero(joint)
    pxy = joint[nz] / len(x)
    px, py = np.bincount(x) / len(x), np.bincount(y) / len(x)
    return float(np.sum(pxy * np.log2(pxy / (px[nz // ny] * py[nz % ny]))))


def set_phrases(a, b):
    """a, b: word codes of first/second words in each pair. Returns (count, list of (a, b, n, ratio))."""
    n = len(a)
    key = a.astype(np.int64) * (b.max() + 1) + b
    uniq, cnt = np.unique(key, return_counts=True)
    keep = cnt >= MIN_COUNT
    ua, ub, c = uniq[keep] // (b.max() + 1), uniq[keep] % (b.max() + 1), cnt[keep]
    pa, pb = np.bincount(a) / n, np.bincount(b, minlength=b.max() + 1) / n
    ratio = c / (n * pa[ua] * pb[ub])
    strong = ratio >= MIN_RATIO
    return int(strong.sum()), list(zip(ua[strong], ub[strong], c[strong], ratio[strong]))


def analyse(g, rng, name):
    g = g.reset_index(drop=True)
    words = g["clean"].to_numpy()
    wcode, vocab = pd.factorize(words)
    bcode, _ = pd.factorize(pd.Series(words).str[:2])
    ecode, _ = pd.factorize(pd.Series(words).str[-2:])
    parts = {"beginning": bcode, "ending": ecode}
    line = pd.factorize(g["folio"] + "|" + g["header"])[0]
    pos = g.groupby(line).cumcount().to_numpy()
    length = np.bincount(line)[line]
    interior = (pos >= 1) & (pos <= length - 2)
    pair = interior[:-1] & interior[1:] & (line[:-1] == line[1:])
    idx = np.flatnonzero(interior)
    grp = line[idx]

    def stats(order):
        w = wcode[order]
        n_sp, sp = set_phrases(w[:-1][pair], w[1:][pair])
        links = {f"{l1}->{l2}": mi(parts[l1][order][:-1][pair], parts[l2][order][1:][pair]) for l1, l2 in LINKS}
        return n_sp, sp, links

    ident = np.arange(len(g))
    obs_n, obs_sp, obs_links = stats(ident)
    null_n, null_links = np.empty(N_PERMS), {k: np.empty(N_PERMS) for k in obs_links}
    for i in range(N_PERMS):
        order = ident.copy()
        order[idx] = idx[np.lexsort((rng.random(len(idx)), grp))]
        n_sp, _, links = stats(order)
        null_n[i] = n_sp
        for k, v in links.items():
            null_links[k][i] = v
    p = lambda null, obs: float((np.sum(null >= obs) + 1) / (N_PERMS + 1))
    top = sorted(obs_sp, key=lambda r: -r[2])[:12]
    sec = g["section"].to_numpy()
    top_rows = []
    for a, b, c, r in top:
        hits = np.flatnonzero(pair & (wcode[:-1] == a) & (wcode[1:] == b))
        secs = Counter(sec[hits]).most_common(2)
        top_rows.append((f"{vocab[a]} {vocab[b]}", int(c), float(r), ", ".join(f"{s} {k}" for s, k in secs)))
    same_line = (line[:-2] == line[1:-1]) & (line[1:-1] == line[2:])
    tri = Counter(zip(words[:-2][same_line], words[1:-1][same_line], words[2:][same_line])).most_common(8)
    return {
        "name": name, "pairs": int(pair.sum()),
        "r1": {"obs": obs_n, "null_mean": float(null_n.mean()), "p": p(null_n, obs_n)},
        "r2": {k: {"obs": v, "null_mean": float(null_links[k].mean()), "excess": v - float(null_links[k].mean()),
                   "p": p(null_links[k], v)} for k, v in obs_links.items()},
        "top": top_rows, "triples": tri,
    }


def main():
    df = parse_zl3b(CORPUS_PATH)
    df = df[(df.locus_type == "P") & (df.clean.str.len() > 0)]
    rng = np.random.default_rng(SEED)
    res = [analyse(df[df.currier == c], rng, f"Currier {c}") for c in ("A", "B")]
    L = ["# Repeated phrases and grammar links", "",
         f"Pre-registration: `analyses/phrases_prereg.md`. Paragraph text, interior pairs only, {N_PERMS:,} "
         f"within-line shuffles, seed {SEED}.", "",
         "## R1. Set phrases (pairs seen 5+ times and 3+ times more often than chance)", "",
         "| Text | Pairs | Set phrases | Shuffled mean | p | Result |", "|---|---:|---:|---:|---:|---|"]
    for r in res:
        x = r["r1"]
        L.append(f"| {r['name']} | {r['pairs']:,} | {x['obs']} | {x['null_mean']:.1f} | {x['p']:.3g} | "
                 f"{'PASS' if x['p'] < ALPHA else 'FAIL'} |")
    L += ["", "## R2. Grammar links (which parts of neighbouring words depend on each other)", "",
          "| Text | Link | MI (bits) | Shuffled | Excess | p |", "|---|---|---:|---:|---:|---:|"]
    for r in res:
        for k, x in sorted(r["r2"].items(), key=lambda kv: -kv[1]["excess"]):
            L.append(f"| {r['name']} | {k.replace('->', ' of word 1 → ')} of word 2 | {x['obs']:.4f} | "
                     f"{x['null_mean']:.4f} | {x['excess']:.4f} | {x['p']:.3g} |")
    for r in res:
        L += ["", f"## Top set phrases, {r['name']} (descriptive)", "",
              "| Phrase | Count | Times expected | Main sections |", "|---|---:|---:|---|"]
        L += [f"| {ph} | {c} | {ra:.1f} | {s} |" for ph, c, ra, s in r["top"]]
        L += ["", "Most frequent three-word sequences: " +
              "; ".join(f"{' '.join(t)} ({c})" for t, c in r["triples"])]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "phrases_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
