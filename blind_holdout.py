#!/usr/bin/env python3
"""
blind_holdout.py
----------------
Clean blind test of the frozen morphology on pre-registered holdout folios.

The holdout list lives in data/blind_holdout_v1.json. It was drawn at random
(fixed seed) from folios never used for cribs, the dossier or the old
holdout, and committed before this scorer existed. Do not edit it.

The model is trained ONLY on the remaining folios. Its single input is each
token's ending class from the frozen parser rules (structural_validation.
ending_of, which reproduces parser.map_macrostate). Every target is
something the token's own spelling does not determine:

  A. Line position   - which token ends its physical line
  B. Layout          - paragraph text vs label / ring / radius text
  C. Section         - which manuscript section a holdout folio belongs to

Each score is compared with a baseline and with a permutation null that
keeps the structure of the holdout data (lines, layout blocks, folios).

    python blind_holdout.py                  # writes output/blind_holdout_report.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

import structural_validation as sv
from parser import CORPUS_PATH, parse_zl3b

ROOT = Path(__file__).resolve().parent
HOLDOUT_FILE = ROOT / "data" / "blind_holdout_v1.json"
OUTDIR = ROOT / "output"

LABELS = list(sv.ENDINGS) + ["?"]
GROUPING = {e: sv.ENDING_STATE.get(e, "?") for e in LABELS}


def load_holdout(path: Path = HOLDOUT_FILE) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def auc(scores: np.ndarray, labels: np.ndarray) -> float:
    """Area under the ROC curve (Mann-Whitney, ties averaged)."""
    pos, neg = labels.sum(), (~labels).sum()
    if pos == 0 or neg == 0:
        return float("nan")
    ranks = pd.Series(scores).rank().to_numpy()
    return float((ranks[labels].sum() - pos * (pos + 1) / 2) / (pos * neg))


def fit_rates(features: pd.Series, target: np.ndarray) -> dict:
    """P(target | feature) with add-one smoothing."""
    df = pd.DataFrame({"f": features.to_numpy(), "y": target})
    g = df.groupby("f")["y"].agg(["sum", "count"])
    return ((g["sum"] + 1) / (g["count"] + 2)).to_dict()


def bits_gain(p: np.ndarray, base: float, y: np.ndarray) -> float:
    """Log-loss of the base rate minus log-loss of the model, in bits per token."""
    p = np.clip(p, 1e-6, 1 - 1e-6)
    ll_model = -np.mean(np.where(y, np.log2(p), np.log2(1 - p)))
    ll_base = -np.mean(np.where(y, np.log2(base), np.log2(1 - base)))
    return float(ll_base - ll_model)


def binary_target(train, test, target_col, feature, null_groups, n_perms, rng):
    """Train P(target | feature) on train, score test, permutation null on test."""
    rates = fit_rates(train[feature], train[target_col].to_numpy())
    base = float(train[target_col].mean())
    scores = test[feature].map(rates).fillna(base).to_numpy()
    y = test[target_col].to_numpy().astype(bool)
    obs = auc(scores, y)

    # Null: shuffle labels within groups (lines) or across groups (blocks),
    # so clustering in the holdout data is preserved.
    null = np.empty(n_perms)
    if null_groups == "within_line":
        line_id = pd.factorize(test["folio"] + "|" + test["header"])[0]
        order = np.argsort(line_id, kind="stable")
        y_sorted = y[order]
        for i, shuffled in enumerate(sv.within_line_shuffles(y_sorted, line_id[order], n_perms, rng)):
            for j, row in enumerate(shuffled):
                null[i * 250 + j] = auc(scores[order], row)
    else:
        line_key = test["folio"] + "|" + test["header"]
        line_label = test.groupby(line_key, sort=False)[target_col].first()
        idx = line_key.map({k: i for i, k in enumerate(line_label.index)}).to_numpy()
        lab = line_label.to_numpy().astype(bool)
        for i in range(n_perms):
            null[i] = auc(scores, rng.permutation(lab)[idx])
    return {
        "test_tokens": int(len(test)), "positives": int(y.sum()),
        "auc": obs, "null_auc_mean": float(np.nanmean(null)), "null_auc_sd": float(np.nanstd(null)),
        "p": sv.empirical_p(null[~np.isnan(null)], obs),
        "bits_gain_per_token": bits_gain(scores, base, y),
    }


def section_target(train, test, n_perms, rng):
    """Nearest-centroid section prediction from each folio's ending profile."""
    def profiles(df):
        counts = pd.crosstab(df["folio"], df["ending"]).reindex(columns=LABELS, fill_value=0)
        return counts.div(counts.sum(axis=1), axis=0)

    tr_prof, te_prof = profiles(train), profiles(test)
    tr_sec = train.groupby("folio")["section"].first().reindex(tr_prof.index)
    te_sec = test.groupby("folio")["section"].first().reindex(te_prof.index).to_numpy()
    centroids = tr_prof.groupby(tr_sec).mean()

    def cos(a, b):
        a = a / np.linalg.norm(a, axis=1, keepdims=True)
        b = b / np.linalg.norm(b, axis=1, keepdims=True)
        return a @ b.T

    pred = centroids.index.to_numpy()[np.argmax(cos(te_prof.to_numpy(), centroids.to_numpy()), axis=1)]
    acc = float(np.mean(pred == te_sec))
    majority = tr_sec.value_counts().idxmax()
    base = float(np.mean(te_sec == majority))
    null = np.array([np.mean(pred == rng.permutation(te_sec)) for _ in range(n_perms)])
    return {
        "test_folios": int(len(te_sec)), "accuracy": acc,
        "majority_baseline": base, "majority_section": majority,
        "null_mean": float(null.mean()), "p": sv.empirical_p(null, acc),
        "per_folio": [{"folio": f, "section": s, "predicted": p}
                      for f, s, p in zip(te_prof.index, te_sec, pred)],
    }


def run(df: pd.DataFrame, holdout: dict, n_perms: int = 2000, seed: int = 20261001) -> dict:
    rng = np.random.default_rng(seed)
    df = df.copy()
    df["ending"] = df["clean"].map(sv.ending_of)
    df["state4"] = df["ending"].map(GROUPING)
    df["not_paragraph"] = df["locus_type"] != "P"
    is_test = df["folio"].isin(holdout["holdout_folios"])
    train, test = df[~is_test], df[is_test]

    multi_tr = train[(train["line_len"] >= 2) & (train["locus_type"] == "P")]
    multi_te = test[(test["line_len"] >= 2) & (test["locus_type"] == "P")]
    return {
        "holdout": {k: holdout[k] for k in ("name", "created_at", "seed", "corpus_sha256")},
        "train_folios": int(train["folio"].nunique()), "test_folios": int(test["folio"].nunique()),
        "A_line_end_by_ending": binary_target(multi_tr, multi_te, "is_line_end", "ending", "within_line", n_perms, rng),
        "A_line_end_by_state": binary_target(multi_tr, multi_te, "is_line_end", "state4", "within_line", n_perms, rng),
        "B_layout_by_ending": binary_target(train, test, "not_paragraph", "ending", "lines", n_perms, rng),
        "C_section": section_target(train, test, n_perms, rng),
    }


def verdict(p: float, score: float | None = None, baseline: float | None = None) -> str:
    if p >= 0.01:
        return "FAIL"
    if score is not None and baseline is not None and score <= baseline:
        return "FAIL (ties or trails the majority baseline)"
    return "PASS"


def render(r: dict) -> str:
    a, a4, b, c = r["A_line_end_by_ending"], r["A_line_end_by_state"], r["B_layout_by_ending"], r["C_section"]
    h = r["holdout"]
    out = [
        "# Blind holdout report",
        "",
        f"Holdout `{h['name']}`: {r['test_folios']} folios drawn with seed {h['seed']} and committed "
        f"{h['created_at']}, before this scorer existed. The model is trained on the other "
        f"{r['train_folios']} folios only. PASS means p < 0.01.",
        "",
        "Only input: each token's ending class from the frozen parser rules. Every target is something "
        "that spelling does not determine.",
        "",
        "| Target | Holdout size | Score | Chance / baseline | p | Verdict |",
        "|---|---:|---:|---:|---:|---|",
        f"| A. Line-final token (15 endings) | {a['test_tokens']:,} tokens | AUC {a['auc']:.3f} | "
        f"{a['null_auc_mean']:.3f} | {a['p']:.2g} | **{verdict(a['p'])}** |",
        f"| A. Line-final token (4 states C/L/P/R) | {a4['test_tokens']:,} tokens | AUC {a4['auc']:.3f} | "
        f"{a4['null_auc_mean']:.3f} | {a4['p']:.2g} | **{verdict(a4['p'])}** |",
        f"| B. Label / diagram vs paragraph | {b['test_tokens']:,} tokens | AUC {b['auc']:.3f} | "
        f"{b['null_auc_mean']:.3f} | {b['p']:.2g} | **{verdict(b['p'])}** |",
        f"| C. Section of each folio | {c['test_folios']} folios | {c['accuracy']:.1%} correct | "
        f"{c['majority_baseline']:.1%} (always '{c['majority_section']}'); shuffled {c['null_mean']:.1%} | "
        f"{c['p']:.2g} | **{verdict(c['p'], c['accuracy'], c['majority_baseline'])}** |",
        "",
        f"Information gain for line-final prediction: {a['bits_gain_per_token']:.4f} bits/token with 15 endings, "
        f"{a4['bits_gain_per_token']:.4f} with the 4-state grouping.",
        "",
        "Rule note (added after the first run, and stricter only): section prediction must also beat "
        "the always-guess-the-majority-section baseline to pass. No scores changed.",
        "",
        "AUC is the chance that a randomly chosen positive (e.g. a line-final token) gets a higher score "
        "than a randomly chosen negative. 0.5 is chance.",
        "",
        "## Section predictions per holdout folio",
        "",
        "| folio | true section | predicted |",
        "|---|---|---|",
    ]
    out += [f"| {x['folio']} | {x['section']} | {x['predicted']} |" for x in c["per_folio"]]
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--perms", type=int, default=2000)
    ap.add_argument("--outdir", default=str(OUTDIR))
    args = ap.parse_args(argv)
    result = run(parse_zl3b(CORPUS_PATH), load_holdout(), args.perms)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "blind_holdout.json").write_text(json.dumps(result, indent=2, default=float), encoding="utf-8")
    report = render(result)
    (outdir / "blind_holdout_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
