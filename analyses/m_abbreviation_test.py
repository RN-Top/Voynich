#!/usr/bin/env python3
"""
Is line-final -m/-am a space-saving device (H_space) or a unit terminator (H_term)?

Implements analyses/m_abbreviation_prereg.md exactly. Run from the repo root:

    python analyses/m_abbreviation_test.py

Writes output/m_abbreviation_report.md and output/m_abbreviation.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import blind_holdout as bh  # noqa: E402
import structural_validation as sv  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261001
N_PERMS = 10_000
M_ENDINGS = ("am", "m")


def group_shuffle(flags: np.ndarray, groups: np.ndarray, n: int, rng):
    """Yield (b, len) arrays: flags shuffled within each group (groups need not be sorted)."""
    order = np.argsort(groups, kind="stable")
    inverse = np.empty_like(order)
    inverse[order] = np.arange(len(order))
    for block in sv.within_line_shuffles(flags[order], groups[order], n, rng):
        yield block[:, inverse]


def build_tables(df: pd.DataFrame):
    para = df[(df["locus_type"] == "P") & (df["line_len"] >= 2)].copy()
    para["glyphs"] = para["clean"].str.len()
    para["ending"] = para["clean"].map(sv.ending_of)
    para["stem"] = [bh.stem_of(t, c) for t, c in zip(para["clean"], para["control"])]
    para["line_key"] = para["folio"] + "|" + para["header"]

    lines = para.groupby("line_key", sort=False).agg(
        folio=("folio", "first"),
        glyphs=("glyphs", "sum"),
        para_end=("is_para_end", "first"),
    )
    last = para[para["is_line_end"]].set_index("line_key")
    lines["m_final"] = last["ending"].reindex(lines.index).isin(M_ENDINGS).to_numpy()

    finals = para[para["is_line_end"]].copy()
    mid = para[~para["is_line_end"]]
    finals["is_m"] = finals["ending"].isin(M_ENDINGS)
    mid_len = mid.groupby("stem")["glyphs"].mean()
    finals["stem_seen_mid"] = finals["stem"].isin(mid_len.index)
    finals["len_diff"] = finals["glyphs"] - finals["stem"].map(mid_len)
    return lines.reset_index(), finals


def p1_space_pressure(lines, rng):
    sub = lines[~lines["para_end"]].copy()
    sub["dev"] = sub["glyphs"] - sub.groupby("folio")["glyphs"].transform("median")
    dev, m = sub["dev"].to_numpy(float), sub["m_final"].to_numpy()
    groups = pd.factorize(sub["folio"])[0]

    def stat(flags):
        return dev[flags].mean() - dev[~flags].mean()

    obs = float(stat(m))
    null = np.concatenate([[stat(row) for row in block] for block in group_shuffle(m, groups, N_PERMS, rng)])
    return {
        "lines": int(len(sub)), "m_final_lines": int(m.sum()),
        "mean_glyph_excess_m_final": float(dev[m].mean()), "mean_glyph_excess_other": float(dev[~m].mean()),
        "statistic": obs, "null_mean": float(null.mean()),
        "p_one_sided_greater": sv.empirical_p(null, obs),
        "predicted_by_H_space": "> 0",
    }


def p2_paragraph_ends(lines, rng):
    pe, m = lines["para_end"].to_numpy(), lines["m_final"].to_numpy()
    groups = pd.factorize(lines["folio"])[0]

    def stat(flags):
        return m[flags].mean() - m[~flags].mean()

    obs = float(stat(pe))
    null = np.concatenate([[stat(row) for row in block] for block in group_shuffle(pe, groups, N_PERMS, rng)])
    p_two = float((np.sum(np.abs(null - null.mean()) >= abs(obs - null.mean()) - 1e-12) + 1) / (len(null) + 1))
    return {
        "paragraph_final_lines": int(pe.sum()), "other_lines": int((~pe).sum()),
        "m_rate_paragraph_final": float(m[pe].mean()), "m_rate_other": float(m[~pe].mean()),
        "statistic": obs, "null_mean": float(null.mean()), "p_two_sided": p_two,
        "direction": "lower at paragraph ends" if obs < null.mean() else "higher at paragraph ends",
        "predicted_by_H_space": "lower", "predicted_by_H_term": "higher",
    }


def p3_p4_compression(finals, rng):
    m = finals["is_m"].to_numpy()
    seen = finals["stem_seen_mid"].to_numpy()

    # P3: only tokens whose stem occurs mid-line
    d = finals.loc[seen, "len_diff"].to_numpy(float)
    m3 = m[seen]
    obs3 = float(d[m3].mean() - d[~m3].mean())
    null3 = np.array([(lambda f: d[f].mean() - d[~f].mean())(rng.permutation(m3)) for _ in range(N_PERMS)])

    # P4: share of stems seen mid-line
    obs4 = float(seen[m].mean() - seen[~m].mean())
    null4 = np.array([(lambda f: seen[f].mean() - seen[~f].mean())(rng.permutation(m)) for _ in range(N_PERMS)])
    p4 = float((np.sum(np.abs(null4 - null4.mean()) >= abs(obs4 - null4.mean()) - 1e-12) + 1) / (N_PERMS + 1))
    return (
        {
            "tokens": int(seen.sum()), "m_tokens": int(m3.sum()),
            "mean_len_diff_m": float(d[m3].mean()), "mean_len_diff_other": float(d[~m3].mean()),
            "statistic": obs3, "null_mean": float(null3.mean()),
            "p_one_sided_less": float((np.sum(null3 <= obs3 + 1e-12) + 1) / (N_PERMS + 1)),
            "predicted_by_H_space": "< 0 (m-forms shorter than their stem's mid-line forms, relative to other endings)",
        },
        {
            "line_final_tokens": int(len(m)), "m_tokens": int(m.sum()),
            "share_stem_seen_mid_m": float(seen[m].mean()), "share_stem_seen_mid_other": float(seen[~m].mean()),
            "statistic": obs4, "p_two_sided": p4,
        },
    )


def decide(p1, p2, p3) -> str:
    p2_sig = p2["p_two_sided"] < 0.01
    if p2_sig and p2["statistic"] < 0 and (p1["p_one_sided_greater"] < 0.01 or p3["p_one_sided_less"] < 0.01):
        return "H_space supported"
    if p2_sig and p2["statistic"] > 0:
        return "H_term supported"
    return "Inconclusive"


def render(r) -> str:
    p1, p2, p3, p4 = r["P1"], r["P2"], r["P3"], r["P4"]
    return f"""# Is line-final -m/-am a space-saving device?

Pre-registration: `analyses/m_abbreviation_prereg.md` (committed before this code). {N_PERMS:,} permutations, seed {SEED}.

**Decision (pre-registered rule): {r['decision']}**

| Prediction | Observed | p | H_space predicts |
|---|---|---:|---|
| P1 space pressure: m-final lines vs other lines, glyphs above folio median | {p1['mean_glyph_excess_m_final']:+.2f} vs {p1['mean_glyph_excess_other']:+.2f} (diff {p1['statistic']:+.2f}) | {p1['p_one_sided_greater']:.2g} | diff > 0 |
| P2 -m/-am rate at end of paragraph-final lines vs other lines | {p2['m_rate_paragraph_final']:.1%} vs {p2['m_rate_other']:.1%} ({p2['direction']}) | {p2['p_two_sided']:.2g} | lower |
| P3 length of line-final form minus its stem's mid-line forms | -m/-am {p3['mean_len_diff_m']:+.2f} vs other {p3['mean_len_diff_other']:+.2f} glyphs | {p3['p_one_sided_less']:.2g} | -m/-am more negative |
| P4 share of line-final tokens whose stem also occurs mid-line | -m/-am {p4['share_stem_seen_mid_m']:.1%} vs other {p4['share_stem_seen_mid_other']:.1%} | {p4['p_two_sided']:.2g} | not lower (not decisive) |

Counts: P1 {p1['lines']:,} non-final lines ({p1['m_final_lines']} m-final); P2 {p2['paragraph_final_lines']} paragraph-final
lines vs {p2['other_lines']:,} others; P3 {p3['tokens']:,} line-final tokens with a stem seen mid-line ({p3['m_tokens']} -m/-am);
P4 {p4['line_final_tokens']:,} line-final tokens ({p4['m_tokens']} -m/-am).
"""


def main():
    rng = np.random.default_rng(SEED)
    lines, finals = build_tables(parse_zl3b(CORPUS_PATH))
    p1 = p1_space_pressure(lines, rng)
    p2 = p2_paragraph_ends(lines, rng)
    p3, p4 = p3_p4_compression(finals, rng)
    result = {"P1": p1, "P2": p2, "P3": p3, "P4": p4, "decision": decide(p1, p2, p3)}
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    (out / "m_abbreviation.json").write_text(json.dumps(result, indent=2, default=float), encoding="utf-8")
    report = render(result)
    (out / "m_abbreviation_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
