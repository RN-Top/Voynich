#!/usr/bin/env python3
"""
Do the two halves of a folded sheet belong together?

Implements analyses/fold_sheets_prereg.md. Run from the repo root:

    python analyses/fold_sheets_test.py

Writes output/fold_sheets_report.md and output/fold_sheets.json.
"""

from __future__ import annotations

import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261001
N_PERMS = 10_000


def gatherings(path=CORPUS_PATH) -> dict[str, list[int]]:
    """Gathering code -> sorted leaf numbers, from the $Q= codes on folio header lines."""
    out: dict[str, set] = {}
    for line in open(path, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f(\d+)[rv]\d*)>\s+<!(.*)>", line)
        if m:
            q = re.search(r"\$Q=(\w+)", m.group(3))
            if q:
                out.setdefault(q.group(1), set()).add(int(m.group(2)))
    return {k: sorted(v) for k, v in out.items()}


def leaf_of(folio: str) -> int:
    return int(re.match(r"f(\d+)", folio).group(1))


def cosine(a: Counter, b: Counter) -> float:
    dot = sum(a[w] * b[w] for w in set(a) & set(b))
    na = np.sqrt(sum(v * v for v in a.values()))
    nb = np.sqrt(sum(v * v for v in b.values()))
    return float(dot / (na * nb)) if na and nb else 0.0


def lineup(sides_a: list[dict], sides_b: list[dict]) -> float:
    rates = []
    for a in sides_a:
        for b in sides_b:
            common = set(a) & set(b)
            if common:
                rates.append(sum(a[p] == b[p] for p in common) / len(common))
    return float(np.mean(rates)) if rates else 0.0


def build(df):
    df = df.copy()
    df["leaf"] = df["folio"].map(leaf_of)
    df["line_no"] = df["header"].str.extract(r"\.(\d+)")[0].astype(float)
    words = {leaf: Counter(g["clean"]) for leaf, g in df.groupby("leaf")}
    sides = {}
    for leaf, g in df.groupby("leaf"):
        sides[leaf] = [
            {(ln, i): w for ln, i, w in zip(s["line_no"], s["token_idx"], s["clean"])}
            for _, s in g.groupby("folio")
        ]
    return words, sides


def run():
    df = parse_zl3b(CORPUS_PATH)
    words, sides = build(df)
    gath = gatherings()
    present = set(words)

    pair_stats = {}
    sheet_pairs = {}  # gathering -> list of (k, partner)
    for q, leaves in gath.items():
        leaves = [k for k in leaves if k in present]
        lo, hi = min(leaves), max(leaves)
        for a, b in itertools.combinations(leaves, 2):
            pair_stats[(a, b)] = (cosine(words[a], words[b]), lineup(sides[a], sides[b]))
        sheet_pairs[q] = sorted({tuple(sorted((k, lo + hi - k))) for k in leaves
                                 if lo + hi - k in leaves and lo + hi - k != k})

    rng = np.random.default_rng(SEED)
    result = {}
    for version, keep in (("a_all_sheet_pairs", lambda a, b: True),
                          ("b_non_adjacent_sheet_pairs", lambda a, b: abs(a - b) > 1)):
        observed_pairs = {q: [p for p in ps if keep(*p)] for q, ps in sheet_pairs.items()}
        obs_list = [p for ps in observed_pairs.values() for p in ps]
        if not obs_list:
            continue
        obs = np.mean([pair_stats[p] for p in obs_list], axis=0)

        null = np.empty((N_PERMS, 2))
        for i in range(N_PERMS):
            vals = []
            for q, ps in observed_pairs.items():
                m = len(ps)
                if not m:
                    continue
                leaves = [k for k in gath[q] if k in present]
                got = []
                for _ in range(200):  # random re-pairing (matching) within the gathering
                    order = list(rng.permutation(leaves))
                    got = [tuple(sorted(order[j:j + 2])) for j in range(0, len(order) - 1, 2)]
                    got = [p for p in got if keep(*p)]
                    if len(got) >= m:
                        break
                got = got[:m]
                vals += [pair_stats[(int(a), int(b))] for a, b in got]
            null[i] = np.mean(vals, axis=0)
        result[version] = {
            "sheet_pairs": len(obs_list),
            "pairs": [f"f{a}–f{b}" for a, b in obs_list],
            "S1_shared_vocab_observed": float(obs[0]), "S1_null_mean": float(null[:, 0].mean()),
            "S1_p": float((np.sum(null[:, 0] >= obs[0]) + 1) / (N_PERMS + 1)),
            "S2_lineup_observed": float(obs[1]), "S2_null_mean": float(null[:, 1].mean()),
            "S2_p": float((np.sum(null[:, 1] >= obs[1]) + 1) / (N_PERMS + 1)),
        }

    a, b = result.get("a_all_sheet_pairs"), result.get("b_non_adjacent_sheet_pairs")
    sig = lambda r: r is not None and (r["S1_p"] < 0.01 or r["S2_p"] < 0.01)
    result["decision"] = "Supported" if sig(b) else ("Adjacency only" if sig(a) else "Not supported")

    # Descriptive only: the book's first and last leaves (different gatherings, not one sheet).
    all_cos = sorted(cosine(words[x], words[y]) for x, y in itertools.combinations(sorted(present), 2))
    fb = cosine(words[1], words[116]) if 1 in words and 116 in words else None
    result["front_back_of_book"] = None if fb is None else {
        "cosine_f1_f116": fb, "percentile_among_all_leaf_pairs": float(np.mean(np.array(all_cos) <= fb)),
    }
    return result


def render(r) -> str:
    rows = []
    for key, label in (("a_all_sheet_pairs", "(a) all sheet pairs"),
                       ("b_non_adjacent_sheet_pairs", "(b) excluding center-fold / adjacent pairs")):
        x = r.get(key)
        if not x:
            continue
        rows.append(f"| {label} | {x['sheet_pairs']} | {x['S1_shared_vocab_observed']:.3f} vs {x['S1_null_mean']:.3f} | "
                    f"{x['S1_p']:.3g} | {x['S2_lineup_observed']:.4f} vs {x['S2_null_mean']:.4f} | {x['S2_p']:.3g} |")
    fb = r.get("front_back_of_book")
    fb_line = "" if not fb else (
        f"\nDescriptive: the book's first and last leaves (f1, f116; different gatherings, so not one sheet) have shared-"
        f"vocabulary similarity {fb['cosine_f1_f116']:.3f}, higher than {fb['percentile_among_all_leaf_pairs']:.0%} of all leaf pairs.\n")
    return f"""# Do the two halves of a folded sheet belong together?

Pre-registration: `analyses/fold_sheets_prereg.md` (committed before this code). {N_PERMS:,} random re-pairings
within each gathering, seed {SEED}.

**Decision (pre-registered rule): {r['decision']}**

| Version | Sheet pairs | S1 shared vocabulary: sheet pairs vs random pairs | p | S2 same word at same spot | p |
|---|---:|---|---:|---|---:|
{chr(10).join(rows)}
{fb_line}
Sheet pairs tested (b): {', '.join(r['b_non_adjacent_sheet_pairs']['pairs']) if r.get('b_non_adjacent_sheet_pairs') else '—'}
"""


def main():
    r = run()
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    (out / "fold_sheets.json").write_text(json.dumps(r, indent=2), encoding="utf-8")
    report = render(r)
    (out / "fold_sheets_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
