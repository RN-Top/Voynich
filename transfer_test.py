#!/usr/bin/env python3
"""
transfer_test.py
----------------
Do the surviving structural results hold under a different representation
of the manuscript text?

The rules stay frozen. Only the input text changes. Built-in representations:

  zl_canonical   ZL3b, first alternative reading, "," (uncertain space) splits words
  zl_alternate   ZL3b, last alternative reading, "," does NOT split words

Any other IVTFF transcription can be added with --corpus, for example the
Takahashi transliteration (IT2a-n.txt from voynich.nu):

    python transfer_test.py --corpus data/IT2a-n.txt

Writes output/transfer_report.md and output/transfer.json.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import blind_holdout as bh
import structural_validation as sv
from parser import CORPUS_PATH, parse_zl3b

OUTDIR = Path(__file__).resolve().parent / "output"


def core_results(df, holdout, n_perms, seed):
    rng = np.random.default_rng(seed)
    para = sv.Corpus(df[df["locus_type"] == "P"])
    m = sv.test_line_end_enrichment(para, n_perms, rng)["m_family"]
    cyc = sv.test_cycle_nulls(para, min(n_perms, 2000), 200, rng)
    rank = sv.order_ranking(para)
    blind = bh.run(df, holdout, n_perms, seed)
    return {
        "tokens": int(len(df)),
        "m_line_end_share": m["at_line_end"] / m["tokens"] if m["tokens"] else None,
        "m_odds_ratio": m["odds_ratio"],
        "m_shuffle_p": m["within_line_shuffle"]["p"],
        "cycle_vs_shuffle_p": cyc["within_line_shuffle"]["pair_p"],
        "cycle_vs_markov1_p": cyc["markov1_twins"]["pair_p"],
        "cycle_vs_markov2_p": cyc["markov2_twins"]["pair_p"],
        "clpr_rank_of_24": rank["linear_rank_of_CLPR"],
        "blind_A_auc": blind["A_line_end_by_ending"]["auc"],
        "blind_A_p": blind["A_line_end_by_ending"]["p"],
        "blind_B_auc": blind["B_layout_by_ending"]["auc"],
        "blind_B_p": blind["B_layout_by_ending"]["p"],
        "blind_C_acc": blind["C_section"]["accuracy"],
        "blind_C_baseline": blind["C_section"]["majority_baseline"],
        "blind_D_bits": blind["D_carrier_stems"]["bits_gain_per_token"],
        "blind_D_p": blind["D_carrier_stems"]["p"],
    }


ROWS = [
    ("Tokens", "tokens", "{:,}"),
    ("-m/-am share at line end", "m_line_end_share", "{:.1%}"),
    ("-m/-am line-end odds ratio", "m_odds_ratio", "{:.1f}"),
    ("-m/-am within-line shuffle p", "m_shuffle_p", "{:.1g}"),
    ("C→L→P→R vs shuffle p", "cycle_vs_shuffle_p", "{:.2g}"),
    ("C→L→P→R vs Markov-1 p", "cycle_vs_markov1_p", "{:.2g}"),
    ("C→L→P→R vs Markov-2 p", "cycle_vs_markov2_p", "{:.2g}"),
    ("C→L→P→R rank (of 24)", "clpr_rank_of_24", "{}"),
    ("Blind A: line-final AUC", "blind_A_auc", "{:.3f}"),
    ("Blind A: p", "blind_A_p", "{:.2g}"),
    ("Blind B: layout AUC", "blind_B_auc", "{:.3f}"),
    ("Blind B: p", "blind_B_p", "{:.2g}"),
    ("Blind C: section accuracy", "blind_C_acc", "{:.1%}"),
    ("Blind C: majority baseline", "blind_C_baseline", "{:.1%}"),
    ("Blind D: stem → ending bits/token", "blind_D_bits", "{:.3f}"),
    ("Blind D: p", "blind_D_p", "{:.2g}"),
]


def render(results: dict) -> str:
    names = list(results)
    out = [
        "# Representation / transcription transfer",
        "",
        "Frozen rules, different input text. Holdout folios are the pre-registered "
        "`data/blind_holdout_v1.json` list in every column.",
        "",
        "| Result | " + " | ".join(f"`{n}`" for n in names) + " |",
        "|---|" + "---:|" * len(names),
    ]
    for label, key, f in ROWS:
        cells = []
        for n in names:
            v = results[n].get(key)
            cells.append("not computed" if v is None else f.format(v))
        out.append(f"| {label} | " + " | ".join(cells) + " |")
    out += [
        "",
        "`zl_alternate` uses the last alternative reading in `[a:b]` and does not split words at "
        "uncertain spaces. It tests sensitivity to ZL's editorial choices. It is not an independent "
        "transcription; add one with `--corpus`.",
    ]
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", action="append", default=[], help="extra IVTFF transcription file(s)")
    ap.add_argument("--perms", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261001)
    ap.add_argument("--outdir", default=str(OUTDIR))
    args = ap.parse_args(argv)

    holdout = bh.load_holdout()
    reps = {
        "zl_canonical": parse_zl3b(CORPUS_PATH),
        "zl_alternate": parse_zl3b(CORPUS_PATH, reading="last", uncertain_spaces_split=False),
    }
    for path in args.corpus:
        reps[Path(path).stem] = parse_zl3b(path)

    results = {name: core_results(df, holdout, args.perms, args.seed) for name, df in reps.items()}
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "transfer.json").write_text(json.dumps(results, indent=2, default=float), encoding="utf-8")
    report = render(results)
    (outdir / "transfer_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
