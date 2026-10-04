#!/usr/bin/env python3
"""Recipe format in the starred paragraphs (analyses/recipe_format_prereg.md)"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261011
N = 10_000
ALPHA = 0.05 / 3


def paragraphs():
    df = parse_zl3b(CORPUS_PATH)
    df = df[(df.locus_type == "P") & (df.clean.str.len() > 0) & (df.currier == "B")]
    paras, cur, key = [], [], None
    for r in df.itertuples():
        if ",@P" in r.header and r.token_idx == 0 and cur:
            paras.append((key, cur)); cur = []
        if not cur:
            key = r.section
        cur.append(r.clean)
    if cur:
        paras.append((key, cur))
    return [(s, w) for s, w in paras if len(w) >= 5]


def simpson(items):
    c = Counter(items); n = len(items)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1))


def edge_stat(paras, is_rec, pos):
    def diff(mask):
        ps = [w for (_, w), m in zip(paras, mask) if m]
        edge = [w[pos] for w in ps]
        inner = [x for w in ps for x in w[1:-1]]
        return simpson(edge) - simpson(inner)
    return diff(is_rec) - diff(~is_rec)


def cv_stat(ws_list):
    cvs = []
    for w in ws_list:
        c = Counter(x for x in w if len(x) <= 3)
        for tok, k in c.items():
            if k >= 3:
                idx = np.array([i for i, x in enumerate(w) if x == tok])
                g = np.diff(idx)
                cvs.append(g.std() / g.mean())
    return float(np.mean(cvs)) if cvs else float("nan"), len(cvs)


def main():
    paras = paragraphs()
    is_rec = np.array([s == "Stars/Recipes" for s, _ in paras])
    rng = np.random.default_rng(SEED)
    out = {}
    for name, pos in (("T1 opening", 0), ("T2 closing", -1)):
        obs = edge_stat(paras, is_rec, pos)
        null = np.array([edge_stat(paras, rng.permutation(is_rec), pos) for _ in range(N)])
        out[name] = (obs, null.mean(), float((np.sum(null >= obs) + 1) / (N + 1)))
    rec = [w for (_, w), m in zip(paras, is_rec) if m]
    ctl = [w for (_, w), m in zip(paras, is_rec) if not m]
    cv_obs, ncase = cv_stat(rec)
    null3 = np.array([cv_stat([list(rng.permutation(w)) for w in rec])[0] for _ in range(N)])
    p3 = float((np.sum(null3 <= cv_obs) + 1) / (N + 1))
    cv_ctl, nctl = cv_stat(ctl)
    v = lambda p: "SUPPORTED" if p < ALPHA else "NOT SUPPORTED"
    top = lambda pos, grp: ", ".join(f"{w} ({k})" for w, k in Counter(w[pos] for w in grp).most_common(6))
    L = ["# Are the starred paragraphs written in recipe format?", "",
         f"Pre-registration: `analyses/recipe_format_prereg.md`. Currier B only: {len(rec)} recipe paragraphs, "
         f"{len(ctl)} control paragraphs. {N:,} permutations, seed {SEED}; each test needs p < {ALPHA:.4f}.", "",
         "| Test | Observed | Null mean | p | Verdict |", "|---|---:|---:|---:|---|"]
    for name, (o, m, p) in out.items():
        L.append(f"| {name} formula (recipe minus control, edge minus interior repeat rate) | {o:+.4f} | {m:+.4f} | {p:.3g} | **{v(p)}** |")
    L.append(f"| T3 quantity-word spacing (mean gap CV, {ncase} cases; lower = more regular) | {cv_obs:.3f} | {null3.mean():.3f} | {p3:.3g} | **{v(p3)}** |")
    L += ["", f"Control paragraphs, same T3 statistic (not tested): {cv_ctl:.3f} over {nctl} cases.", "",
          "## Most common words (descriptive)", "",
          f"- **Recipe openings:** {top(0, rec)}", f"- **Control openings:** {top(0, ctl)}",
          f"- **Recipe closings:** {top(-1, rec)}", f"- **Control closings:** {top(-1, ctl)}", ""]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "recipe_format_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
