"""
Fold overlay: lay one page over another as if the sheet were folded, and see
which words land on each other.

The transcription gives line numbers and word order, not coordinates, so
positions are approximated: a word's horizontal position is the middle of its
characters as a fraction of the line's length, and line k of one page lands on
line k of the other. Folding mirrors the page left-right, so position x lands
on 1 - x.

The fair comparison: overlay every other page onto the same target in the same
way and see where the chosen page ranks.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import structural_validation as sv  # noqa: E402


def page_lines(df: pd.DataFrame) -> dict[str, list[list[tuple[str, float, float]]]]:
    """folio -> lines of paragraph text -> (word, start, end) as fractions of the line length."""
    para = df[df["locus_type"] == "P"].copy()
    para["line_no"] = para["header"].str.extract(r"\.(\d+)")[0].astype(int)
    pages = {}
    for folio, g in para.groupby("folio", sort=False):
        lines = []
        for _, ln in g.sort_values(["line_no", "token_idx"]).groupby("line_no", sort=True):
            words = ln["clean"].tolist()
            total = sum(len(w) for w in words) + len(words) - 1
            pos, out = 0, []
            for w in words:
                out.append((w, pos / total, (pos + len(w)) / total))
                pos += len(w) + 1
            lines.append(out)
        pages[folio] = lines
    return pages


def overlay(a, b, mirror: bool = True) -> list[dict]:
    """Every word of page a, and the word of page b it lands on (same line index)."""
    landed = []
    for i, (la, lb) in enumerate(zip(a, b)):
        for w, x0, x1 in la:
            x = (x0 + x1) / 2
            x = 1 - x if mirror else x
            hit = next((v for v, y0, y1 in lb if y0 <= x <= y1), None)
            if hit is None:  # landed in a gap between words: take the nearest word
                hit = min(lb, key=lambda t: min(abs(t[1] - x), abs(t[2] - x)))[0]
            landed.append({"line": i + 1, "word_a": w, "word_b": hit,
                           "same_word": w == hit, "same_ending": sv.ending_of(w) == sv.ending_of(hit)})
    return landed


def score(landed: list[dict]) -> dict:
    if not landed:
        return {"pairs": 0, "same_word": float("nan"), "same_ending": float("nan")}
    return {
        "pairs": len(landed),
        "same_word": float(np.mean([r["same_word"] for r in landed])),
        "same_ending": float(np.mean([r["same_ending"] for r in landed])),
    }


def rank_against_all(pages, folded: str, target: str, mirror: bool = True, min_pairs: int = 20) -> dict:
    """Score of `folded` laid on `target`, versus every other page laid on `target` the same way."""
    obs = score(overlay(pages[folded], pages[target], mirror))
    others = {}
    for f, lines in pages.items():
        if f in (folded, target):
            continue
        s = score(overlay(lines, pages[target], mirror))
        if s["pairs"] >= min_pairs:
            others[f] = s
    out = {"observed": obs, "n_other_pages": len(others)}
    for key in ("same_word", "same_ending"):
        vals = np.array([s[key] for s in others.values()])
        out[f"{key}_share_of_pages_scoring_at_least_as_high"] = (
            float((np.sum(vals >= obs[key]) + 1) / (len(vals) + 1)) if len(vals) else float("nan"))
        out[f"{key}_typical"] = float(np.median(vals)) if len(vals) else float("nan")
    return out
