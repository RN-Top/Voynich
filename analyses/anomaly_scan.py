#!/usr/bin/env python3
"""
Exploratory anomaly scan: which pages behave least like their peers?

Each page side is measured on a few text features and compared with pages of the
same section AND the same Currier language (its peers), using robust z-scores
(median / MAD). Section-to-section differences therefore do not count as anomalies.

Features
  single_glyph_words   share of words that are a single character (key-like lists)
  rare_letters         share of characters outside the common EVA set
  mean_word_length     average word length
  ending_distance      how far the page's ending mix is from its peers (total variation)
  letter_pair_distance how far the page's letter-pair mix is from its peers (total variation)

This is a discovery list, not a test: anything it flags needs its own follow-up.

    python analyses/anomaly_scan.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import structural_validation as sv  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

COMMON = set("acdehiklnoqrsty")
MIN_WORDS = 40
FEATURES = ["single_glyph_words", "rare_letters", "mean_word_length", "ending_distance", "letter_pair_distance"]
KNOWN_KEY_LIKE = {"f1r", "f49v", "f57v", "f58r"}  # flagged as key-like in the ZL3b notes


def tv(p: Counter, q: Counter) -> float:
    sp, sq = sum(p.values()), sum(q.values())
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p[k] / sp - q[k] / sq) for k in keys) if sp and sq else float("nan")


def scan(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ending"] = df["clean"].map(sv.ending_of)
    pages = []
    for folio, g in df.groupby("folio", sort=False):
        words = g["clean"].tolist()
        if len(words) < MIN_WORDS:
            continue
        chars = "".join(words)
        pages.append({
            "folio": folio,
            "section": g["section"].iloc[0],
            "currier": g["currier"].iloc[0],
            "words": len(words),
            "single_glyph_words": float(np.mean([len(w) == 1 for w in words])),
            "rare_letters": sum(c not in COMMON for c in chars) / max(len(chars), 1),
            "mean_word_length": float(np.mean([len(w) for w in words])),
            "_endings": Counter(g["ending"]),
            "_pairs": Counter(a + b for w in words for a, b in zip(w, w[1:])),
        })
    pages = pd.DataFrame(pages)
    pages["peer_group"] = pages["section"] + " / " + pages["currier"]

    for i, row in pages.iterrows():
        peers = pages[(pages["peer_group"] == row["peer_group"]) & (pages.index != i)]
        end_ref, pair_ref = Counter(), Counter()
        for _, p in peers.iterrows():
            end_ref.update(p["_endings"])
            pair_ref.update(p["_pairs"])
        pages.loc[i, "ending_distance"] = tv(row["_endings"], end_ref)
        pages.loc[i, "letter_pair_distance"] = tv(row["_pairs"], pair_ref)
        pages.loc[i, "n_peers"] = len(peers)

    # Robust z-scores within each peer group (median / MAD, MAD floored to avoid division blow-ups).
    for f in FEATURES:
        z = np.full(len(pages), np.nan)
        for grp, idx in pages.groupby("peer_group").groups.items():
            vals = pages.loc[idx, f].to_numpy(float)
            if len(vals) < 5:
                continue
            med = np.median(vals)
            mad = np.median(np.abs(vals - med)) * 1.4826
            mad = max(mad, 0.25 * np.std(vals), 1e-9)
            z[pages.index.get_indexer(idx)] = (vals - med) / mad
        pages[f"z_{f}"] = z

    zcols = [f"z_{f}" for f in FEATURES]
    pages["anomaly_score"] = pages[zcols].abs().max(axis=1)
    pages["main_reason"] = pages[zcols].abs().idxmax(axis=1).str.replace("z_", "", regex=False)
    pages["known_key_like"] = pages["folio"].isin(KNOWN_KEY_LIKE)
    keep = ["folio", "section", "currier", "words", "n_peers", "anomaly_score", "main_reason", "known_key_like"] + FEATURES
    return pages[keep].sort_values("anomaly_score", ascending=False).reset_index(drop=True)


def key_sequences() -> dict:
    """Descriptive look at the key-like character sequences recorded in ZL3b."""
    f57v = "o l d r v x k m f @169 v t r @170 @171 y I @172".split()
    f49v = "f o r y e @140 k s p o @192 y e @140 @164 p o @192 y e @140 d y e k y".split()
    df = parse_zl3b(CORPUS_PATH)
    text = "".join(df[df["locus_type"] == "P"]["clean"])
    freq = Counter(text)
    total = sum(freq.values())
    ranked = [c for c, _ in freq.most_common()]
    out = {}
    for name, seq in (("f57v_ring_cycle", f57v), ("f49v_margin_column", f49v)):
        plain = sorted({s for s in seq if len(s) == 1})
        out[name] = {
            "sequence": " ".join(seq),
            "plain_glyphs": plain,
            "glyph_share_of_running_text": {c: round(freq[c] / total, 4) for c in plain},
            "running_text_top10_missing_from_sequence": [c for c in ranked[:10] if c not in plain],
            "rare_symbols_in_sequence": sorted({s for s in seq if s.startswith("@")}),
        }
    return out


def main():
    df = parse_zl3b(CORPUS_PATH)
    res = scan(df)
    keys = key_sequences()
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    res.to_csv(out / "anomaly_scan.csv", index=False)
    (out / "key_sequences.json").write_text(json.dumps(keys, indent=2), encoding="utf-8")

    top = res.head(15)
    known = res[res["known_key_like"]][["folio", "anomaly_score", "main_reason"]]
    ranks = {f: int(res.index[res["folio"] == f][0]) + 1 for f in known["folio"]}
    lines = [
        "# Anomaly scan (exploratory)",
        "",
        f"{len(res)} page sides with at least {MIN_WORDS} words, each compared with pages of the same section and "
        "Currier language (robust z-scores). This is a list of candidates to look at, not a test.",
        "",
        "| Rank | Page | Section / language | Words | Score | Main reason | Known key-like? |",
        "|---:|---|---|---:|---:|---|---|",
    ]
    for i, r in top.iterrows():
        lines.append(f"| {i + 1} | {r['folio']} | {r['section']} / {r['currier']} | {r['words']} | "
                     f"{r['anomaly_score']:.1f} | {r['main_reason'].replace('_', ' ')} | {'yes' if r['known_key_like'] else ''} |")
    lines += ["", "Ranks of the pages the transcription notes call key-like: " +
              ", ".join(f"{f} #{k}" for f, k in sorted(ranks.items(), key=lambda x: x[1])), "",
              "## Key-like sequences", ""]
    for name, k in keys.items():
        lines += [f"**{name}**: `{k['sequence']}`",
                  f"- Plain glyphs: {', '.join(k['plain_glyphs'])}; rare symbols: {', '.join(k['rare_symbols_in_sequence'])}",
                  f"- Most common running-text letters missing from it: {', '.join(k['running_text_top10_missing_from_sequence'])}",
                  ""]
    report = "\n".join(lines) + "\n"
    (out / "anomaly_scan_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
