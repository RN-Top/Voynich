#!/usr/bin/env python3
"""
Exploratory: how does Voynich text compare with real texts and with known
text-generating methods on the same structural measurements?

Every text goes through the same generic pipeline (lowercase letters, words,
"ending" = last 2 letters, "stem" = the rest), so no Voynich-specific rule
gives Voynich an advantage.

Texts
  voynich_native     ZL3b paragraph text, real manuscript lines
  voynich_reflowed   the same words, set into new lines of the same widths
  latin_*            Latin texts from the CLTK Latin Library, set into lines of
                     Voynich widths (modern editions keep no manuscript lines)
  cipher_*           a Latin text enciphered with a fixed verbose cipher
                     (each letter -> 1-3 EVA glyphs)
  voynich_shuffled   Voynich words in random order (no word-order structure)
  extra files        any .txt in data/comparison/ (e.g. Italian or German)

    python analyses/comparison_fingerprint.py --latin-dir /path/to/lat_text_latin_library

Writes output/comparison_fingerprint_report.md and .json.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261001
MAX_TOKENS = 35_000
EVA = "acdefghiklmnopqrsty"

LATIN_SOURCES = {
    "latin_apicius_recipes": ["apicius/*.txt"],
    "latin_albertanus_13c": ["albertanus/*.txt"],
    "latin_bede_8c": ["bede/*.txt"],
}


# -----------------------------------------------------------------------------
# Text preparation
# -----------------------------------------------------------------------------
def latin_words(text: str) -> list[str]:
    text = text.lower().replace("j", "i").replace("v", "u")
    return re.findall(r"[a-z]+", text)


def reflow(words: list[str], widths: np.ndarray, rng) -> list[list[str]]:
    """Greedy line filling to widths sampled from the Voynich width distribution."""
    lines, cur, width, target = [], [], 0, rng.choice(widths)
    for w in words:
        add = len(w) + (1 if cur else 0)
        if cur and width + add > target:
            lines.append(cur)
            cur, width, target = [], 0, rng.choice(widths)
            add = len(w)
        cur.append(w)
        width += add
    if cur:
        lines.append(cur)
    return lines


def verbose_cipher(words: list[str], rng) -> list[str]:
    """Fixed random substitution: each Latin letter -> 1-3 EVA glyphs."""
    table = {}
    for ch in "abcdefghiklmnopqrstuxyz":
        n = rng.choice([1, 1, 2, 3])
        table[ch] = "".join(rng.choice(list(EVA), size=n))
    return ["".join(table.get(c, "") for c in w) for w in words]


# -----------------------------------------------------------------------------
# Measurements (identical for every text)
# -----------------------------------------------------------------------------
def char_entropies(words: list[str]) -> tuple[float, float]:
    s = " ".join(words)
    uni = Counter(s)
    n = sum(uni.values())
    h1 = -sum(c / n * math.log2(c / n) for c in uni.values())
    bi = Counter(zip(s, s[1:]))
    nb = sum(bi.values())
    h_joint = -sum(c / nb * math.log2(c / nb) for c in bi.values())
    return h1, h_joint - h1


def ending(w: str) -> str:
    return w[-2:] if len(w) > 2 else w


def stem(w: str) -> str:
    return w[:-2] if len(w) > 2 else ""


def stem_ending_gain(words: list[str]) -> float:
    # Alternate words between train and test, so both halves span the whole text.
    tr, te = words[0::2], words[1::2]
    ends = Counter(ending(w) for w in tr)
    k = len(ends) + 1
    tot = sum(ends.values())
    uni = {e: (c + 1) / (tot + k) for e, c in ends.items()}
    floor = 1 / (tot + k)
    by_stem: dict[str, Counter] = {}
    for w in tr:
        by_stem.setdefault(stem(w), Counter())[ending(w)] += 1
    alpha, gains = 2.0, []
    for w in te:
        s, e = stem(w), ending(w)
        if s not in by_stem:
            continue
        pu = uni.get(e, floor)
        c = by_stem[s]
        pc = (c[e] + alpha * pu) / (sum(c.values()) + alpha)
        gains.append(math.log2(pc) - math.log2(pu))
    return float(np.mean(gains)) if gains else float("nan")


def line_end_effect(lines: list[list[str]]) -> dict:
    end, mid = Counter(), Counter()
    for ln in lines:
        if len(ln) < 2:
            continue
        for i, w in enumerate(ln):
            (end if i == len(ln) - 1 else mid)[ending(w)] += 1
    te, tm = sum(end.values()), sum(mid.values())
    best, best_e = 0.0, None
    for e in set(end) | set(mid):
        a, b = end[e], mid[e]
        if a + b < 30:
            continue
        odds = ((a + 0.5) / (te - a + 0.5)) / ((b + 0.5) / (tm - b + 0.5))
        if odds > best:
            best, best_e = odds, e
    return {"max_line_end_odds_ratio": best, "most_line_final_ending": best_e}


def fingerprint(lines: list[list[str]]) -> dict:
    words = [w for ln in lines for w in ln][:MAX_TOKENS]
    h1, h2 = char_entropies(words)
    first = words[:30_000]
    return {
        "tokens": len(words),
        "mean_word_length": float(np.mean([len(w) for w in words])),
        "type_token_ratio_30k": len(set(first)) / len(first),
        "char_entropy_h1": h1,
        "conditional_char_entropy_h2": h2,
        "adjacent_repeat_rate": float(np.mean([a == b for a, b in zip(words, words[1:])])),
        "stem_predicts_ending_bits": stem_ending_gain(words),
        **line_end_effect(lines),
    }


ROWS = [
    ("Tokens", "tokens", "{:,}"),
    ("Mean word length", "mean_word_length", "{:.2f}"),
    ("Distinct words / tokens (first 30k)", "type_token_ratio_30k", "{:.3f}"),
    ("Character entropy h1 (bits)", "char_entropy_h1", "{:.2f}"),
    ("Conditional character entropy h2 (bits)", "conditional_char_entropy_h2", "{:.2f}"),
    ("Same word twice in a row", "adjacent_repeat_rate", "{:.2%}"),
    ("Stem → ending information (bits/word)", "stem_predicts_ending_bits", "{:.3f}"),
    ("Strongest line-final ending: odds ratio", "max_line_end_odds_ratio", "{:.1f}"),
    ("Strongest line-final ending", "most_line_final_ending", "`-{}`"),
]


def render(results: dict) -> str:
    names = list(results)
    out = [
        "# Comparison fingerprint (exploratory)",
        "",
        "Same generic measurements for every text: lowercase letters, words, ending = last 2 letters. "
        "Only `voynich_native` keeps real manuscript lines; every other text is set into lines whose widths "
        "are sampled from the Voynich paragraph lines.",
        "",
        "| Measurement | " + " | ".join(f"`{n}`" for n in names) + " |",
        "|---|" + "---:|" * len(names),
    ]
    for label, key, f in ROWS:
        cells = []
        for n in names:
            v = results[n].get(key)
            cells.append("—" if v is None or (isinstance(v, float) and math.isnan(v)) else f.format(v))
        out.append(f"| {label} | " + " | ".join(cells) + " |")
    out += [
        "",
        "Caveats: h1/h2 depend on the alphabet (EVA vs Latin letters), so compare their *pattern*, not exact "
        "values. A self-citation (Timm & Schinner) comparison is not included: a faithful implementation of the published algorithm is still needed. Line-end "
        "measures for re-lined texts show only what line filling alone produces; a fair comparison of real "
        "line-end behaviour needs diplomatic transcriptions of medieval manuscripts that keep the original "
        "line breaks.",
    ]
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--latin-dir", default=str(ROOT.parent / "cltk" / "lat_text_latin_library"))
    ap.add_argument("--extra-dir", default=str(ROOT / "data" / "comparison"))
    args = ap.parse_args(argv)
    rng = np.random.default_rng(SEED)

    df = parse_zl3b(CORPUS_PATH)
    para = df[(df["locus_type"] == "P")]
    native = [g["clean"].tolist() for _, g in para.groupby(["folio", "header"], sort=False)]
    widths = np.array([sum(len(w) for w in ln) + len(ln) - 1 for ln in native if len(ln) >= 2])
    v_words = [w for ln in native for w in ln]

    texts: dict[str, list[list[str]]] = {
        "voynich_native": native,
        "voynich_reflowed": reflow(v_words, widths, rng),
    }
    shuffled = list(rng.permutation(v_words))
    lens = [len(ln) for ln in native]
    texts["voynich_shuffled"] = [shuffled[sum(lens[:i]):sum(lens[:i + 1])] for i in range(len(lens))] \
        if len(lens) < 6000 else []

    latin_dir = Path(args.latin_dir)
    first_latin = None
    for name, globs in LATIN_SOURCES.items():
        files = sorted(f for g in globs for f in latin_dir.glob(g))
        if not files:
            continue
        words = latin_words(" ".join(f.read_text(errors="ignore") for f in files))[:MAX_TOKENS]
        texts[name] = reflow(words, widths, rng)
        first_latin = first_latin or (name, words)
    if first_latin:
        texts[f"cipher_{first_latin[0].split('_', 1)[1]}"] = reflow(verbose_cipher(first_latin[1], rng), widths, rng)

    extra = Path(args.extra_dir)
    if extra.is_dir():
        for f in sorted(extra.glob("*.txt")):
            words = [w for w in re.findall(r"[^\W\d_]+", f.read_text(errors="ignore").lower())][:MAX_TOKENS]
            texts[f.stem] = reflow(words, widths, rng)

    results = {name: fingerprint(lines) for name, lines in texts.items() if lines}
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    (out / "comparison_fingerprint.json").write_text(json.dumps(results, indent=2, default=float), encoding="utf-8")
    report = render(results)
    (out / "comparison_fingerprint_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
