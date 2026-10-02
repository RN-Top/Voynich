#!/usr/bin/env python3
"""
Fifth-element cycle test (pre-registration: analyses/fifth_element_prereg.md).

The unassigned state '?' is added as a fifth step to the C -> L -> P -> R cycle, in each of its
4 distinct positions. Statistic: share of same-line 5-word windows that run one full cycle step.
Observed and nulls both take the best of the 4 placements.

    python analyses/fifth_element_test.py
"""

from __future__ import annotations

import itertools
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import structural_validation as sv  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261002
N_SHUFFLE, N_TWINS = 2000, 1000
ALPHA = 0.01
N = sv.N_STATES  # C, L, P, R, ?
PLACEMENTS = ["C?LPR", "CL?PR", "CLP?R", "CLPR?"]


def tables(order: str):
    idx = [sv.S_IDX[s] for s in order]
    nxt = np.full(N, -1)
    for i, s in enumerate(idx):
        nxt[s] = idx[(i + 1) % 5]
    return nxt


def scores(states: np.ndarray, corpus: sv.Corpus, nxt: np.ndarray):
    """states (B, T). Returns (pair_score, window5_score) arrays."""
    s = states.astype(np.int64)
    step = nxt[s[:, :-1]] == s[:, 1:]          # (B, T-1): next token follows the cycle
    step &= corpus.pair_mask
    pair = step.sum(1) / corpus.pair_mask.sum()
    w5 = step[:, :-3] & step[:, 1:-2] & step[:, 2:-1] & step[:, 3:]
    n5 = (corpus.pair_mask[:-3] & corpus.pair_mask[1:-2] & corpus.pair_mask[2:-1] & corpus.pair_mask[3:]).sum()
    return pair, w5.sum(1) / max(n5, 1)


def best(states, corpus, tabs):
    res = [scores(states, corpus, t) for t in tabs]
    pair = np.max([r[0] for r in res], axis=0)
    w5 = np.max([r[1] for r in res], axis=0)
    return pair, w5, res


def main():
    df = parse_zl3b(CORPUS_PATH)
    df = df[df["locus_type"] == "P"]
    corpus = sv.Corpus(df)
    tabs = [tables(o) for o in PLACEMENTS]
    obs_pair, obs_w5, per = best(corpus.states[None, :], corpus, tabs)
    obs_pair, obs_w5 = float(obs_pair[0]), float(obs_w5[0])
    per_place = {o: (float(r[0][0]), float(r[1][0])) for o, r in zip(PLACEMENTS, per)}

    rng = np.random.default_rng(SEED)
    nulls = {}
    gens = {
        "within_line_shuffle": sv.within_line_shuffles(corpus.states, corpus.line_id, N_SHUFFLE, rng),
        "markov1_twins": sv.markov_twins(corpus, 1, N_TWINS, rng),
        "markov2_twins": sv.markov_twins(corpus, 2, N_TWINS, rng),
    }
    for name, gen in gens.items():
        ps, ws = [], []
        for block in gen:
            p, w, _ = best(block, corpus, tabs)
            ps.append(p)
            ws.append(w)
        ps, ws = np.concatenate(ps), np.concatenate(ws)
        nulls[name] = {"n": len(ws), "pair_mean": ps.mean(), "pair_p": sv.empirical_p(ps, obs_pair),
                       "w5_mean": ws.mean(), "w5_p": sv.empirical_p(ws, obs_w5)}

    # Descriptive: rank among all 24 cyclic orders of the five states.
    all_cycles = {}
    for perm in itertools.permutations("LPR?"):
        o = "C" + "".join(perm)
        all_cycles[o] = float(scores(corpus.states[None, :], corpus, tables(o))[1][0])
    ranked = sorted(all_cycles.items(), key=lambda x: -x[1])
    best_place = max(per_place, key=lambda o: per_place[o][1])
    rank = 1 + sum(v > all_cycles[best_place] for v in all_cycles.values())
    q_endings = Counter(w[-2:] if len(w) > 1 else w for w in df.loc[df["state"] == "?", "clean"])

    supported = nulls["markov1_twins"]["w5_p"] < ALPHA and nulls["markov2_twins"]["w5_p"] < ALPHA
    lines = [
        "# Fifth-element cycle test",
        "",
        "Pre-registration: `analyses/fifth_element_prereg.md`. Paragraph text, "
        f"{corpus.T:,} words; the fifth element is the {int((df['state'] == '?').sum()):,} words with no role (`?`). "
        f"Seed {SEED}.",
        "",
        "| Placement | 2-word score | 5-word window score |",
        "|---|---:|---:|",
        *[f"| {o} | {p:.4f} | {w:.5f} |" for o, (p, w) in per_place.items()],
        "",
        f"Best placement: **{best_place}** (5-word score {obs_w5:.5f}).",
        "",
        "| Control | n | 5-word mean | p | 2-word mean | p (not used for verdict) |",
        "|---|---:|---:|---:|---:|---:|",
        *[f"| {k} | {v['n']} | {v['w5_mean']:.5f} | {v['w5_p']:.3g} | {v['pair_mean']:.4f} | {v['pair_p']:.3g} |"
          for k, v in nulls.items()],
        "",
        f"**Verdict: {'SUPPORTED' if supported else 'NOT SUPPORTED'}** (needs p < {ALPHA} against both Markov twins).",
        "",
        f"Descriptive: the best placement ranks {rank} of 24 possible five-step cycles. Top three: "
        + ", ".join(f"{o} ({v:.5f})" for o, v in ranked[:3]) + ".",
        "",
        "Most common last two letters of the `?` words: "
        + ", ".join(f"-{e} ({c})" for e, c in q_endings.most_common(8)) + ".",
    ]
    report = "\n".join(lines) + "\n"
    (ROOT / "output").mkdir(exist_ok=True)
    (ROOT / "output" / "fifth_element_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
