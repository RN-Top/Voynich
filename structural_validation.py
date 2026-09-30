#!/usr/bin/env python3
"""
structural_validation.py
------------------------
Meaning-free validation ladder for the morphotactic model.

Every test here uses ONLY:
  * the canonical parser (parser.parse_zl3b),
  * the frozen macrostate rules (parser.VoynichParser.map_macrostate),
  * physical position in the manuscript (line, folio, section, Currier hand).

No Venetian / German / apparatus glosses are used, except in test 6, which
exists specifically to check whether the glosses predict anything the
structure alone does not.

Run from the repo root:

    python structural_validation.py                 # default settings
    python structural_validation.py --quick         # fewer permutations
    python structural_validation.py --perms 20000 --twins 2000 --seed 7

Writes:
    output/structural_validation.json
    output/structural_validation_report.md

Tests
  1. Terminal-ending line-end enrichment (-m/-am and every other ending class)
       Fisher exact test + within-line shuffle null.
  2. C->L->P->R cycle vs. within-line shuffle, Markov-1 and Markov-2 twins.
  3. State-order tournament: all 24 orders, on the full corpus and on
       independent splits (folio halves, Currier A, Currier B).
  4. Predictive-state test on held-out folios (information gain in bits).
  5. Affix-role tournament: the observed endings stay fixed, the grouping of
       endings into the four states is permuted.
  6. Semantic permutation tournament: glosses from lexicon.py are permuted
       among their tokens; does the published assignment predict section
       better than shuffled assignments?
  7. Holdout hygiene: overlap between declared holdout folios and folios the
       project has already used; dictionary coverage on untouched folios.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from blind_test import SEEN_FOLIOS  # folios already used for dossier recipes / cribs
from parser import CORPUS_PATH, HOLDOUT_FOLIOS, parse_zl3b

ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "output"

STATES = ("C", "L", "P", "R", "?")
S_IDX = {s: i for i, s in enumerate(STATES)}
N_STATES = len(STATES)
UNKNOWN = S_IDX["?"]
HYPOTHESIS_ORDER = ("C", "L", "P", "R")

# Ending labels in the exact priority used by VoynichParser.map_macrostate.
# Within a group the longest suffix is tried first.
ENDING_GROUPS = {
    "R": ("am", "m"),
    "C": ("eedy", "edy", "eey", "ey", "dy"),
    "L": ("aiiin", "aiin", "ain", "or", "ar"),
    "P": ("ol", "al", "y"),
}
ENDINGS = tuple(e for g in ("R", "C", "L", "P") for e in ENDING_GROUPS[g])
ENDING_STATE = {e: g for g, es in ENDING_GROUPS.items() for e in es}

# Test 6 pre-registration: which manuscript section each gloss domain should
# favour IF the gloss is right. Freeze this before looking at test-6 output.
DOMAIN_EXPECTED_SECTIONS = {
    "Botanical": {"Herbal"},
    "Humoral": {"Herbal"},
    "Astronomical": {"Astronomical/Zodiac", "Cosmological"},
    "Solvent": {"Biological"},
    "Compounding": {"Pharmaceutical", "Stars/Recipes"},
}


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def ending_of(token: str) -> str:
    """Ending label consistent with map_macrostate, or '?' if none."""
    if token.endswith("am"):
        return "am"
    if token.endswith("m") and not token.endswith(("im", "am")):
        return "m"
    for group in ("C", "L", "P"):
        for suffix in ENDING_GROUPS[group]:
            if token.endswith(suffix):
                return suffix
    return "?"


def log_hypergeom_pmf(k: int, row1: int, col1: int, n: int) -> float:
    return (
        math.lgamma(col1 + 1) - math.lgamma(k + 1) - math.lgamma(col1 - k + 1)
        + math.lgamma(n - col1 + 1) - math.lgamma(row1 - k + 1)
        - math.lgamma(n - col1 - row1 + k + 1)
        - (math.lgamma(n + 1) - math.lgamma(row1 + 1) - math.lgamma(n - row1 + 1))
    )


def fisher_exact(a: int, b: int, c: int, d: int) -> dict:
    """2x2 table [[a, b], [c, d]]. Returns odds ratio, one-sided (greater) and two-sided p."""
    row1, col1, n = a + b, a + c, a + b + c + d
    lo, hi = max(0, row1 + col1 - n), min(row1, col1)
    logp = {k: log_hypergeom_pmf(k, row1, col1, n) for k in range(lo, hi + 1)}
    p_obs = logp[a]
    greater = sum(math.exp(v) for k, v in logp.items() if k >= a)
    two_sided = sum(math.exp(v) for v in logp.values() if v <= p_obs + 1e-9)
    odds = (a * d) / (b * c) if b * c > 0 else float("inf")
    return {"odds_ratio": odds, "p_greater": min(1.0, greater), "p_two_sided": min(1.0, two_sided)}


def empirical_p(null: np.ndarray, observed: float) -> float:
    """One-sided (null >= observed) with the +1 correction."""
    return float((np.sum(null >= observed - 1e-12) + 1) / (len(null) + 1))


def folio_half(folio: str, salt: str) -> int:
    return int(hashlib.sha256(f"{salt}:{folio}".encode()).hexdigest(), 16) % 2


# -----------------------------------------------------------------------------
# Corpus preparation
# -----------------------------------------------------------------------------
class Corpus:
    def __init__(self, df: pd.DataFrame):
        self.df = df.reset_index(drop=True)
        self.states = self.df["state"].map(S_IDX).to_numpy(dtype=np.int8)
        self.line_id = pd.factorize(self.df["folio"] + "|" + self.df["header"])[0]
        self.T = len(self.df)
        same = self.line_id[1:] == self.line_id[:-1]
        self.pair_mask = same
        self.quad_mask = same[:-2] & same[1:-1] & same[2:] if self.T >= 4 else np.zeros(0, bool)
        starts = np.r_[0, np.flatnonzero(~same) + 1]
        self.line_starts = starts
        self.line_lens = np.diff(np.r_[starts, self.T])

    def subset(self, mask) -> "Corpus":
        return Corpus(self.df[np.asarray(mask)])


def cycle_tables(order):
    """Lookup tables marking bigrams / 4-grams that follow the cyclic order."""
    idx = [S_IDX[s] for s in order]
    pair = np.zeros(N_STATES * N_STATES, dtype=bool)
    quad = np.zeros(N_STATES ** 4, dtype=bool)
    for r in range(4):
        a, b, c, d = (idx[(r + j) % 4] for j in range(4))
        pair[a * N_STATES + b] = True
        quad[((a * N_STATES + b) * N_STATES + c) * N_STATES + d] = True
    return pair, quad


def linear_pair_table(order):
    idx = [S_IDX[s] for s in order]
    pair = np.zeros(N_STATES * N_STATES, dtype=bool)
    for a, b in zip(idx[:-1], idx[1:]):
        pair[a * N_STATES + b] = True
    return pair


def cycle_scores(states: np.ndarray, corpus: Corpus, pair_tab, quad_tab):
    """states: (B, T) int array. Returns (pair_score, quad_score) arrays of shape (B,)."""
    s = states.astype(np.int16)
    a, b = s[:, :-1], s[:, 1:]
    both_known = (a != UNKNOWN) & (b != UNKNOWN) & corpus.pair_mask
    code = a * N_STATES + b
    pair_hits = (pair_tab[code] & corpus.pair_mask).sum(1)
    pair_score = pair_hits / np.maximum(both_known.sum(1), 1)

    if corpus.T < 4:
        return pair_score, np.zeros(len(s))
    q = ((s[:, :-3] * N_STATES + s[:, 1:-2]) * N_STATES + s[:, 2:-1]) * N_STATES + s[:, 3:]
    quad_hits = (quad_tab[q] & corpus.quad_mask).sum(1)
    quad_score = quad_hits / max(int(corpus.quad_mask.sum()), 1)
    return pair_score, quad_score


def within_line_shuffles(values: np.ndarray, line_id: np.ndarray, n: int, rng, batch: int = 250):
    """Yield (b, T) arrays, each row a within-line permutation of values."""
    done = 0
    while done < n:
        b = min(batch, n - done)
        keys = line_id[None, :].astype(np.float64) + rng.random((b, len(values)))
        order = np.argsort(keys, axis=1, kind="stable")
        yield values[order]
        done += b


def markov_twins(corpus: Corpus, order: int, n: int, rng, batch: int = 200):
    """Yield (b, T) state arrays drawn from a within-line Markov chain of the given order,
    fitted to the corpus, preserving every line length."""
    s = corpus.states.astype(np.int64)
    starts, lens = corpus.line_starts, corpus.line_lens
    init = np.bincount(s[starts], minlength=N_STATES).astype(float) + 1e-9
    init /= init.sum()

    m1 = np.full((N_STATES, N_STATES), 1e-9)
    np.add.at(m1, (s[:-1][corpus.pair_mask], s[1:][corpus.pair_mask]), 1)
    m1 /= m1.sum(1, keepdims=True)

    m2 = np.full((N_STATES, N_STATES, N_STATES), 1e-9)
    if corpus.T >= 3:
        tri = corpus.pair_mask[:-1] & corpus.pair_mask[1:]
        np.add.at(m2, (s[:-2][tri], s[1:-1][tri], s[2:][tri]), 1)
    # back off to M1 where a context was never observed
    unseen = m2.sum(2) < 1e-6
    m2[unseen] = m1[np.nonzero(unseen)[1]]
    m2 /= m2.sum(2, keepdims=True)

    c_init, c1, c2 = np.cumsum(init), np.cumsum(m1, 1), np.cumsum(m2, 2)
    max_len = int(lens.max())
    done = 0
    while done < n:
        b = min(batch, n - done)
        out = np.empty((b, corpus.T), dtype=np.int8)
        for t in range(max_len):
            active = lens > t
            pos = starts[active] + t
            u = rng.random((b, len(pos)))
            if t == 0:
                out[:, pos] = (u[..., None] > c_init[None, None, :]).sum(-1)
            elif order == 1 or t == 1:
                prev = out[:, pos - 1]
                out[:, pos] = (u[..., None] > c1[prev]).sum(-1)
            else:
                prev2, prev = out[:, pos - 2], out[:, pos - 1]
                out[:, pos] = (u[..., None] > c2[prev2, prev]).sum(-1)
        np.minimum(out, N_STATES - 1, out=out)
        yield out
        done += b


# -----------------------------------------------------------------------------
# Test 1: line-end enrichment of terminal endings
# -----------------------------------------------------------------------------
def test_line_end_enrichment(corpus: Corpus, n_perms: int, rng) -> dict:
    df = corpus.df
    endings = df["clean"].map(ending_of).to_numpy()
    is_end = df["is_line_end"].to_numpy()
    lens = corpus.line_lens
    multi = np.repeat(lens >= 2, lens)  # single-token lines carry no positional information

    rows = []
    for label in list(ENDINGS) + ["?"]:
        hit = endings == label
        a = int((hit & is_end & multi).sum())
        b = int((hit & ~is_end & multi).sum())
        c = int((~hit & is_end & multi).sum())
        d = int((~hit & ~is_end & multi).sum())
        if a + b == 0:
            continue
        fe = fisher_exact(a, b, c, d)
        rows.append({
            "ending": label, "state": ENDING_STATE.get(label, "?"), "n": a + b,
            "line_end": a, "line_end_rate": a / (a + c) if a + c else 0.0,
            "mid_line_rate": b / (b + d) if b + d else 0.0,
            "share_at_line_end": a / (a + b),
            **fe,
        })

    # Within-line shuffle null for the -m / -am family specifically.
    m_family = np.isin(endings, ("am", "m")) & multi
    k_per_line = np.add.reduceat(m_family.astype(int), corpus.line_starts)
    p_last = k_per_line / lens
    observed = int((m_family & is_end).sum())
    null = np.zeros(n_perms, dtype=np.int32)
    active = p_last > 0
    step = 5000
    for i in range(0, n_perms, step):
        b = min(step, n_perms - i)
        null[i:i + b] = (rng.random((b, int(active.sum()))) < p_last[active]).sum(1)

    m_rows = {r["ending"]: r for r in rows}
    a = sum(m_rows[e]["line_end"] for e in ("am", "m") if e in m_rows)
    n_m = sum(m_rows[e]["n"] for e in ("am", "m") if e in m_rows)
    total_end = int((is_end & multi).sum())
    total_mid = int((~is_end & multi).sum())
    fe = fisher_exact(a, n_m - a, total_end - a, total_mid - (n_m - a))
    return {
        "m_family": {
            "tokens": n_m, "at_line_end": a,
            "line_end_incidence": a / total_end if total_end else 0.0,
            "mid_line_incidence": (n_m - a) / total_mid if total_mid else 0.0,
            **fe,
            "within_line_shuffle": {
                "observed": observed, "null_mean": float(null.mean()),
                "null_sd": float(null.std()), "p": empirical_p(null, observed), "perms": n_perms,
            },
        },
        "by_ending": sorted(rows, key=lambda r: -r["odds_ratio"] if math.isfinite(r["odds_ratio"]) else -1e9),
    }


# -----------------------------------------------------------------------------
# Test 2: cycle vs. shuffle and Markov twins
# -----------------------------------------------------------------------------
def test_cycle_nulls(corpus: Corpus, n_perms: int, n_twins: int, rng) -> dict:
    pair_tab, quad_tab = cycle_tables(HYPOTHESIS_ORDER)
    obs_pair, obs_quad = cycle_scores(corpus.states[None, :], corpus, pair_tab, quad_tab)
    obs_pair, obs_quad = float(obs_pair[0]), float(obs_quad[0])

    def run(gen):
        pairs, quads = [], []
        for block in gen:
            p, q = cycle_scores(block, corpus, pair_tab, quad_tab)
            pairs.append(p)
            quads.append(q)
        return np.concatenate(pairs), np.concatenate(quads)

    out = {"observed": {"pair_score": obs_pair, "cycle4_rate": obs_quad}}
    nulls = {
        "within_line_shuffle": run(within_line_shuffles(corpus.states, corpus.line_id, n_perms, rng)),
        "markov1_twins": run(markov_twins(corpus, 1, n_twins, rng)),
        "markov2_twins": run(markov_twins(corpus, 2, n_twins, rng)),
    }
    for name, (p, q) in nulls.items():
        out[name] = {
            "n": len(p),
            "pair_null_mean": float(p.mean()), "pair_p": empirical_p(p, obs_pair),
            "cycle4_null_mean": float(q.mean()), "cycle4_p": empirical_p(q, obs_quad),
        }
    return out


# -----------------------------------------------------------------------------
# Test 3: state-order tournament
# -----------------------------------------------------------------------------
def order_ranking(corpus: Corpus) -> dict:
    s = corpus.states.astype(np.int16)
    code = (s[:-1] * N_STATES + s[1:])[corpus.pair_mask]
    counts = np.bincount(code, minlength=N_STATES * N_STATES)
    linear, cyclic = [], {}
    for order in itertools.permutations(HYPOTHESIS_ORDER):
        linear.append(("".join(order), int(counts[linear_pair_table(order)].sum())))
        canon = min("".join(order[r:] + order[:r]) for r in range(4))
        cyclic[canon] = int(counts[cycle_tables(order)[0]].sum())
    linear.sort(key=lambda x: -x[1])
    cyc = sorted(cyclic.items(), key=lambda x: -x[1])
    target = "".join(HYPOTHESIS_ORDER)
    target_cyc = min(target[r:] + target[:r] for r in range(4))
    rank = lambda table, key: 1 + sum(1 for _, v in table if v > dict(table)[key])
    return {
        "tokens": corpus.T,
        "linear_rank_of_CLPR": rank(linear, target), "linear_of": 24,
        "cyclic_rank_of_CLPR": rank(cyc, target_cyc), "cyclic_of": 6,
        "linear_top3": linear[:3], "cyclic_top3": cyc[:3],
    }


def test_order_tournament(corpus: Corpus, salt: str) -> dict:
    df = corpus.df
    half = df["folio"].map(lambda f: folio_half(f, salt)).to_numpy()
    splits = {
        "full_corpus": np.ones(corpus.T, bool),
        "folio_half_A": half == 0,
        "folio_half_B": half == 1,
        "currier_A": (df["currier"] == "A").to_numpy(),
        "currier_B": (df["currier"] == "B").to_numpy(),
        "untouched_folios": ~df["folio"].isin(SEEN_FOLIOS).to_numpy(),
    }
    return {name: order_ranking(corpus.subset(m)) for name, m in splits.items() if m.sum() > 100}


# -----------------------------------------------------------------------------
# Test 4: predictive-state test on held-out folios
# -----------------------------------------------------------------------------
def test_predictive_state(corpus: Corpus, salt: str) -> dict:
    half = corpus.df["folio"].map(lambda f: folio_half(f, salt)).to_numpy()
    train, test = corpus.subset(half == 0), corpus.subset(half == 1)

    def bigrams(c: Corpus):
        s = c.states.astype(int)
        return s[:-1][c.pair_mask], s[1:][c.pair_mask]

    a_tr, b_tr = bigrams(train)
    a_te, b_te = bigrams(test)
    uni = np.bincount(b_tr, minlength=N_STATES) + 1.0
    uni /= uni.sum()
    cond = np.ones((N_STATES, N_STATES))
    np.add.at(cond, (a_tr, b_tr), 1)
    cond /= cond.sum(1, keepdims=True)

    acc_base = float(np.mean(b_te == np.argmax(uni)))
    acc_model = float(np.mean(b_te == np.argmax(cond, 1)[a_te]))
    h_uni = float(-np.mean(np.log2(uni[b_te])))
    h_bi = float(-np.mean(np.log2(cond[a_te, b_te])))
    return {
        "train_pairs": int(len(a_tr)), "test_pairs": int(len(a_te)),
        "majority_baseline_accuracy": acc_base, "state_conditioned_accuracy": acc_model,
        "unigram_bits": h_uni, "bigram_bits": h_bi, "information_gain_bits": h_uni - h_bi,
        "note": "Information gain measures how much the current state tells you about the "
                "next one. It is a property of the state labels, not of the C->L->P->R order.",
    }


# -----------------------------------------------------------------------------
# Test 5: affix-role tournament
# -----------------------------------------------------------------------------
def test_affix_role(corpus: Corpus, n_perms: int, rng) -> dict:
    labels = list(ENDINGS) + ["?"]
    lab_idx = {e: i for i, e in enumerate(labels)}
    tok_end = corpus.df["clean"].map(lambda t: lab_idx[ending_of(t)]).to_numpy()

    # Sanity: the ending map reproduces map_macrostate exactly.
    rebuilt = np.array([S_IDX[ENDING_STATE.get(labels[i], "?")] for i in tok_end], dtype=np.int8)
    mismatch = int((rebuilt != corpus.states).sum())

    group_sizes = [len(ENDING_GROUPS[g]) for g in HYPOTHESIS_ORDER]
    cyc_tabs = []
    for order in itertools.permutations(HYPOTHESIS_ORDER):
        if order[0] == HYPOTHESIS_ORDER[0]:  # one representative per cycle
            cyc_tabs.append(("".join(order), cycle_tables(order)[0]))

    a_idx, b_idx = tok_end[:-1][corpus.pair_mask], tok_end[1:][corpus.pair_mask]
    n_lab = len(labels)
    pair_counts = np.bincount(a_idx * n_lab + b_idx, minlength=n_lab * n_lab).reshape(n_lab, n_lab)

    def score(mapping: np.ndarray):
        # mapping: label index -> state index. Collapse label bigrams into state bigrams.
        m = np.zeros((n_lab, N_STATES))
        m[np.arange(n_lab), mapping] = 1
        sc = m.T @ pair_counts @ m
        known = sc[:4, :4].sum()
        best = max((float(sc.reshape(-1)[tab].sum() / known), name) for name, tab in cyc_tabs)
        return best

    original = np.array([S_IDX[ENDING_STATE.get(e, "?")] for e in labels])
    obs, obs_cycle = score(original)
    base = np.repeat([S_IDX[g] for g in HYPOTHESIS_ORDER], group_sizes)
    null = np.empty(n_perms)
    for i in range(n_perms):
        mapping = original.copy()
        mapping[:len(ENDINGS)] = rng.permutation(base)
        null[i] = score(mapping)[0]
    return {
        "parser_consistency_mismatches": mismatch,
        "observed_best_cycle_score": obs, "observed_best_cycle": obs_cycle,
        "null_mean": float(null.mean()), "null_sd": float(null.std()),
        "p": empirical_p(null, obs), "perms": n_perms,
        "note": "Endings stay fixed; which ending belongs to which state is shuffled "
                "(group sizes preserved), and each shuffle gets its best of the 6 cycles.",
    }


# -----------------------------------------------------------------------------
# Test 6: semantic permutation tournament
# -----------------------------------------------------------------------------
def test_semantic_permutation(corpus: Corpus, n_perms: int, rng) -> dict:
    from lexicon import MASTER_LEXICON

    entries = [(tok, info["domain"]) for tok, info in MASTER_LEXICON.items()
               if info["domain"] in DOMAIN_EXPECTED_SECTIONS]
    sections = corpus.df.groupby("clean")["section"].agg(list).to_dict()
    toks = [t for t, _ in entries if t in sections]
    domains = np.array([d for t, d in entries if t in sections])
    if len(toks) < 3:
        return {"status": "not computed", "reason": "fewer than 3 glossed tokens occur in the corpus"}

    # hits[i, j]: occurrences of token i that fall in the sections expected for domain j
    dom_list = sorted(DOMAIN_EXPECTED_SECTIONS)
    hits = np.array([[sum(s in DOMAIN_EXPECTED_SECTIONS[d] for s in sections[t]) for d in dom_list]
                     for t in toks], dtype=float)
    totals = np.array([len(sections[t]) for t in toks], dtype=float)
    dom_idx = np.array([dom_list.index(d) for d in domains])

    def rate(assign):
        return float(hits[np.arange(len(toks)), assign].sum() / totals.sum())

    obs = rate(dom_idx)
    null = np.array([rate(rng.permutation(dom_idx)) for _ in range(n_perms)])
    return {
        "glossed_tokens_tested": len(toks), "occurrences": int(totals.sum()),
        "observed_section_hit_rate": obs,
        "null_mean": float(null.mean()), "null_sd": float(null.std()),
        "p": empirical_p(null, obs), "perms": n_perms,
        "domain_expected_sections": {k: sorted(v) for k, v in DOMAIN_EXPECTED_SECTIONS.items()},
        "per_token": [
            {"token": t, "domain": d, "n": int(n),
             "hit_rate_for_own_domain": float(hits[i, dom_list.index(d)] / n)}
            for i, (t, d, n) in enumerate(zip(toks, domains, totals))
        ],
        "note": "Glosses are shuffled among the glossed tokens. Only section preference is "
                "tested; operational glosses (heat, drain, ...) have no independent target "
                "in the manuscript yet and cannot be scored.",
    }


# -----------------------------------------------------------------------------
# Test 7: holdout hygiene and dictionary coverage
# -----------------------------------------------------------------------------
def test_holdout_hygiene(corpus: Corpus) -> dict:
    from lexicon import MASTER_LEXICON

    overlap = sorted(set(HOLDOUT_FOLIOS) & SEEN_FOLIOS)
    untouched = corpus.df[~corpus.df["folio"].isin(SEEN_FOLIOS | set(HOLDOUT_FOLIOS))]
    covered = int(untouched["clean"].isin(MASTER_LEXICON).sum())
    return {
        "declared_holdout": list(HOLDOUT_FOLIOS),
        "holdout_also_in_seen_folios": overlap,
        "holdout_is_clean": not overlap,
        "untouched_tokens": int(len(untouched)),
        "untouched_tokens_in_dictionary": covered,
        "dictionary_coverage_untouched": covered / len(untouched) if len(untouched) else 0.0,
    }


# -----------------------------------------------------------------------------
# Report
# -----------------------------------------------------------------------------
def fmt_p(p: float) -> str:
    return "< 1e-300" if p == 0 else f"{p:.1e}"


def verdict(p: float, alpha: float = 0.01) -> str:
    return "PASS" if p < alpha else "FAIL"


def render_markdown(r: dict) -> str:
    m = r["test1_line_end"]["m_family"]
    c = r["test2_cycle"]
    lines = [
        "# Structural validation report",
        "",
        f"Generated {r['meta']['generated_at']} by `structural_validation.py` "
        f"(seed {r['meta']['seed']}, corpus SHA-256 `{r['meta']['corpus_sha256'][:16]}…`).",
        f"Scope: locus types {r['meta']['locus_types']}, {r['meta']['tokens']:,} tokens, "
        f"{r['meta']['lines']:,} lines, {r['meta']['folios']} folios.",
        "",
        "Every number below is recomputed from the corpus on each run. Nothing is hard-coded.",
        "Significance threshold for PASS: p < 0.01.",
        "",
        "## 1. Line-end enrichment of -m / -am",
        "",
        f"- {m['tokens']} tokens end in -m/-am; {m['at_line_end']} are line-final.",
        f"- Line-end incidence {m['line_end_incidence']:.1%} vs mid-line {m['mid_line_incidence']:.1%}; "
        f"odds ratio {m['odds_ratio']:.2f}; Fisher p (greater) {fmt_p(m['p_greater'])}.",
        f"- Within-line shuffle ({m['within_line_shuffle']['perms']:,} perms): observed "
        f"{m['within_line_shuffle']['observed']} vs null mean {m['within_line_shuffle']['null_mean']:.1f}, "
        f"p = {m['within_line_shuffle']['p']:.2e} → **{verdict(m['within_line_shuffle']['p'])}**",
        "",
        "All ending classes, for comparison (lines of ≥ 2 tokens):",
        "",
        "| ending | state | n | share line-final | odds ratio | Fisher p (greater) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for e in r["test1_line_end"]["by_ending"]:
        lines.append(f"| `{e['ending']}` | {e['state']} | {e['n']} | {e['share_at_line_end']:.1%} | "
                     f"{e['odds_ratio']:.2f} | {fmt_p(e['p_greater'])} |")
    lines += [
        "",
        "## 2–3. C→L→P→R cycle against lower-order nulls",
        "",
        f"Observed: {c['observed']['pair_score']:.4f} of known-state adjacent pairs follow the cycle; "
        f"{c['observed']['cycle4_rate']:.4f} of 4-token windows run a full cycle step.",
        "",
        "| null | n | pair-score mean | pair p | 4-window mean | 4-window p |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name in ("within_line_shuffle", "markov1_twins", "markov2_twins"):
        n = c[name]
        lines.append(f"| {name} | {n['n']} | {n['pair_null_mean']:.4f} | {n['pair_p']:.3g} ({verdict(n['pair_p'])}) | "
                     f"{n['cycle4_null_mean']:.5f} | {n['cycle4_p']:.3g} ({verdict(n['cycle4_p'])}) |")
    lines += [
        "",
        "A Markov-1 twin reproduces the bigram table by construction, so the pair score cannot beat it; "
        "the 4-window score is the one that could show structure beyond adjacent pairs.",
        "",
        "## 3b. State-order tournament",
        "",
        "| split | tokens | CLPR rank (linear, of 24) | CLPR rank (cyclic, of 6) | top linear orders |",
        "|---|---:|---:|---:|---|",
    ]
    for name, t in r["test3_order_tournament"].items():
        top = ", ".join(f"{o} ({v})" for o, v in t["linear_top3"])
        lines.append(f"| {name} | {t['tokens']:,} | {t['linear_rank_of_CLPR']} | {t['cyclic_rank_of_CLPR']} | {top} |")
    p4 = r["test4_predictive_state"]
    a5 = r["test5_affix_role"]
    s6 = r["test6_semantic_permutation"]
    h7 = r["test7_holdout_hygiene"]
    lines += [
        "",
        "## 4. Predictive-state test (train on one folio half, test on the other)",
        "",
        f"- Majority baseline accuracy {p4['majority_baseline_accuracy']:.1%}; "
        f"state-conditioned accuracy {p4['state_conditioned_accuracy']:.1%}.",
        f"- Information gain {p4['information_gain_bits']:.4f} bits/token "
        f"({p4['unigram_bits']:.3f} → {p4['bigram_bits']:.3f}).",
        f"- {p4['note']}",
        "",
        "## 5. Affix-role tournament",
        "",
        f"- Parser consistency check: {a5['parser_consistency_mismatches']} mismatches.",
        f"- Observed best cycle score {a5['observed_best_cycle_score']:.4f} (best cycle {a5['observed_best_cycle']}); "
        f"shuffled groupings mean {a5['null_mean']:.4f} ± {a5['null_sd']:.4f}; "
        f"p = {a5['p']:.3g} → **{verdict(a5['p'])}**",
        f"- {a5['note']}",
        "",
        "## 6. Semantic permutation tournament",
        "",
    ]
    if s6.get("status") == "not computed":
        lines.append(f"Not computed: {s6['reason']}")
    else:
        lines += [
            f"- {s6['glossed_tokens_tested']} glossed tokens, {s6['occurrences']:,} occurrences.",
            f"- Published glosses place {s6['observed_section_hit_rate']:.1%} of occurrences in the expected section; "
            f"shuffled glosses {s6['null_mean']:.1%} ± {s6['null_sd']:.1%}; p = {s6['p']:.3g} → **{verdict(s6['p'])}**",
            f"- Pre-registered domain → section map: `{json.dumps(s6['domain_expected_sections'])}`",
            f"- {s6['note']}",
        ]
    lines += [
        "",
        "## 7. Holdout hygiene",
        "",
        f"- Declared holdout folios: {', '.join(h7['declared_holdout'])}",
        f"- Also listed as already-used (SEEN_FOLIOS): {', '.join(h7['holdout_also_in_seen_folios']) or 'none'} → "
        f"**{'CLEAN' if h7['holdout_is_clean'] else 'CONTAMINATED'}**",
        f"- On untouched folios, {h7['untouched_tokens_in_dictionary']:,} of {h7['untouched_tokens']:,} tokens "
        f"({h7['dictionary_coverage_untouched']:.1%}) are exact dictionary entries.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", default=CORPUS_PATH)
    ap.add_argument("--seed", type=int, default=20260930)
    ap.add_argument("--perms", type=int, default=20000, help="shuffle / permutation count")
    ap.add_argument("--twins", type=int, default=1000, help="Markov twin count")
    ap.add_argument("--locus-types", default="P", help="IVTFF locus types to include (P=paragraph, L=label, C=circular, R=radial)")
    ap.add_argument("--quick", action="store_true", help="2,000 perms / 200 twins")
    ap.add_argument("--outdir", default=str(OUTDIR))
    args = ap.parse_args(argv)
    if args.quick:
        args.perms, args.twins = 2000, 200

    rng = np.random.default_rng(args.seed)
    salt = str(args.seed)
    df = parse_zl3b(args.corpus)
    df = df[df["locus_type"].isin(list(args.locus_types))]
    corpus = Corpus(df)

    corpus_bytes = Path(args.corpus).read_bytes()
    results = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "seed": args.seed, "perms": args.perms, "twins": args.twins,
            "locus_types": args.locus_types, "corpus": str(args.corpus),
            "corpus_sha256": hashlib.sha256(corpus_bytes).hexdigest(),
            "tokens": corpus.T, "lines": int(len(corpus.line_lens)),
            "folios": int(df["folio"].nunique()),
        },
        "test1_line_end": test_line_end_enrichment(corpus, args.perms, rng),
        "test2_cycle": test_cycle_nulls(corpus, min(args.perms, 5000), args.twins, rng),
        "test3_order_tournament": test_order_tournament(corpus, salt),
        "test4_predictive_state": test_predictive_state(corpus, salt),
        "test5_affix_role": test_affix_role(corpus, args.perms, rng),
        "test6_semantic_permutation": test_semantic_permutation(corpus, args.perms, rng),
        "test7_holdout_hygiene": test_holdout_hygiene(corpus),
    }

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "structural_validation.json").write_text(json.dumps(results, indent=2, default=float), encoding="utf-8")
    report = render_markdown(results)
    (outdir / "structural_validation_report.md").write_text(report, encoding="utf-8")
    print(report)
    return results


if __name__ == "__main__":
    main()
