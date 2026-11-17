#!/usr/bin/env python3
"""Does the manuscript read better backwards? Runs the four pre-registered tests in
analyses/backwards_prereg.md and writes output/backwards_report.md.

    python3 analyses/backwards_test.py
"""

import json
import math
import random
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "voynich_integrated.json"
REF = ROOT / "Data" / "reference"
OUT = ROOT / "output" / "backwards_report.md"
SEED = 408
PERMS = 10_000
BOOTS = 2_000
GROUPS = ["cth", "ckh", "cph", "cfh", "iin", "ch", "sh", "ii", "ee"]


def binom_two_sided(k, n):
    """Exact two-sided binomial test, p = 0.5."""
    probs = [math.comb(n, i) / 2 ** n for i in range(n + 1)]
    return min(1.0, sum(q for q in probs if q <= probs[k] * (1 + 1e-9)))


def load():
    return json.load(open(DATA, encoding="utf-8"))["folios"]


def para_lines(folios):
    return [ln for f in folios for ln in f["text_lines"] if ln["unit"] == "paragraph"]


# ---------- Test 1: words in a line ----------

def edge_stats(lines):
    n = len(lines)
    d_len = sum(len(ws[0]) - len(ws[-1]) for ws in lines) / n
    d_m = sum(ws[-1].endswith("m") for ws in lines) / n - sum(ws[0].endswith("m") for ws in lines) / n
    return d_len, d_m


def test1(folios, rng):
    lines = [ln["words"] for ln in para_lines(folios) if ln["word_count"] >= 4]
    obs = edge_stats(lines)
    ge = [0, 0]
    null = [[], []]
    for _ in range(PERMS):
        sh = [rng.sample(ws, len(ws)) for ws in lines]
        s = edge_stats(sh)
        for i in range(2):
            null[i].append(s[i])
            if abs(s[i]) >= abs(obs[i]):
                ge[i] += 1
    p = [(g + 1) / (PERMS + 1) for g in ge]
    first_len = sum(len(ws[0]) for ws in lines) / len(lines)
    last_len = sum(len(ws[-1]) for ws in lines) / len(lines)
    mid_len = sum(sum(len(w) for w in ws[1:-1]) / (len(ws) - 2) for ws in lines) / len(lines)
    m_last = sum(ws[-1].endswith("m") for ws in lines)
    m_first = sum(ws[0].endswith("m") for ws in lines)
    if all(o > 0 for o in obs) and all(q < 0.01 for q in p):
        verdict = "left to right (forwards)"
    elif all(o < 0 for o in obs) and all(q < 0.01 for q in p):
        verdict = "right to left (backwards)"
    else:
        verdict = "inconclusive"
    return dict(n=len(lines), d_len=obs[0], d_m=obs[1], p_len=p[0], p_m=p[1],
                first_len=first_len, mid_len=mid_len, last_len=last_len,
                m_first=m_first, m_last=m_last, verdict=verdict)


# ---------- Test 2: lines in a paragraph ----------

def test2(folios):
    B = T = ties = n = 0
    for f in folios:
        lines = {ln["line"]: ln for ln in f["text_lines"]}
        for u in f["text_units"]:
            if u["unit"] != "paragraph" or len(u["lines"]) < 3:
                continue
            n += 1
            lens = [len("".join(lines[i]["words"])) for i in u["lines"]]
            m = min(lens)
            if lens.count(m) > 1:
                ties += 1
                continue
            if lens[-1] == m:
                B += 1
            elif lens[0] == m:
                T += 1
    p = binom_two_sided(B, B + T) if B + T else 1.0
    if B > T and p < 0.01:
        verdict = "top to bottom (forwards)"
    elif T > B and p < 0.01:
        verdict = "bottom to top (backwards)"
    else:
        verdict = "inconclusive"
    return dict(n=n, bottom=B, top=T, ties=ties, middle=n - B - T - ties, p=p, verdict=verdict)


# ---------- Test 3: letters in a word ----------

def entropy(counter):
    tot = sum(counter.values())
    return -sum(c / tot * math.log2(c / tot) for c in counter.values())


def tokenize(word, grouped):
    if not grouped:
        return list(word)
    out, i = [], 0
    while i < len(word):
        for g in GROUPS:
            if word.startswith(g, i):
                out.append(g)
                i += len(g)
                break
        else:
            out.append(word[i])
            i += 1
    return out


def L(words, k, grouped=False):
    start, end = Counter(), Counter()
    for w in words:
        t = tokenize(w, grouped)
        if len(t) >= k + 1:
            start[tuple(t[:k])] += 1
            end[tuple(t[-k:])] += 1
    return math.log(entropy(end) / entropy(start))


def clean_voynich(w):
    return "?" not in w and "@" not in w and "'" not in w


def test3(folios, rng):
    pages = [[w for ln in f["text_lines"] for w in ln["words"] if clean_voynich(w)] for f in folios]
    allw = [w for p in pages for w in p]
    refs = {}
    for fp in sorted(REF.glob("*.txt")):
        ws = open(fp, encoding="utf-8").read().split()
        refs[fp.stem] = {k: L(ws, k) for k in (1, 2, 3)}
    res = {"refs": refs, "voynich": {}, "voynich_grouped": {}}
    for grouped, key in ((False, "voynich"), (True, "voynich_grouped")):
        for k in (1, 2, 3):
            obs = L(allw, k, grouped)
            boots = []
            for _ in range(BOOTS):
                sample = [w for p in rng.choices(pages, k=len(pages)) for w in p]
                boots.append(L(sample, k, grouped))
            boots.sort()
            lo, hi = boots[int(0.025 * BOOTS)], boots[int(0.975 * BOOTS) - 1]
            res[key][k] = (obs, lo, hi)
    void = not all(v < 0 for r in refs.values() for v in r.values())
    v = res["voynich"]
    if void:
        verdict = "void (reference texts do not all show the expected pattern)"
    elif all(v[k][2] < 0 for k in (1, 2, 3)):
        verdict = "same direction as Latin/Italian (forwards)"
    elif all(v[k][1] > 0 for k in (1, 2, 3)):
        verdict = "like Latin/Italian spelled backwards (mirror)"
    else:
        verdict = "inconclusive"
    res["verdict"] = verdict
    res["n_words"] = len(allw)
    return res


# ---------- Test 4: pages in the book ----------

def test4(folios):
    open_end, open_start, n = [], [], 0
    for f in folios:
        P = [ln for ln in f["text_lines"] if ln["unit"] == "paragraph"]
        if not P:
            continue
        n += 1
        if "<$>" not in P[-1]["text"]:
            open_end.append(f["folio_id"])
        if "<%>" not in P[0]["text"]:
            open_start.append(f["folio_id"])
    testable = len(open_end) >= 10
    return dict(n=n, open_end=open_end, open_start=open_start, testable=testable,
                verdict="cannot be tested from the text" if not testable else "see report")


def fmt_p(p):
    return f"{p:.2g}" if p >= 1e-4 else "< 1e-4"


def report(t1, t2, t3, t4):
    r = []
    r.append("# Does the manuscript read better backwards?\n")
    r.append("Pre-registration: `analyses/backwards_prereg.md`. Code: `analyses/backwards_test.py` "
             f"(seed {SEED}). Data: `voynich_integrated.json` (ZL3b).\n")
    r.append("| Direction | Result |\n|---|---|")
    r.append(f"| Words in a line | **{t1['verdict']}** |")
    r.append(f"| Lines in a paragraph | **{t2['verdict']}** |")
    r.append(f"| Letters in a word | **{t3['verdict']}** |")
    r.append(f"| Pages in the book | **{t4['verdict']}** |\n")

    r.append("## Test 1: words in a line\n")
    r.append(f"{t1['n']} paragraph lines with 4+ words.\n")
    r.append(f"- Word length: first word {t1['first_len']:.2f} letters, middle words {t1['mid_len']:.2f}, "
             f"last word {t1['last_len']:.2f}. First minus last = {t1['d_len']:+.3f}, "
             f"within-line shuffle p = {fmt_p(t1['p_len'])}.")
    r.append(f"- Ending in -m: {t1['m_last']} last words vs {t1['m_first']} first words. "
             f"Difference in share = {t1['d_m']:+.4f}, p = {fmt_p(t1['p_m'])}.")
    r.append(f"- Decision: **{t1['verdict']}**.\n")

    r.append("## Test 2: lines in a paragraph\n")
    r.append(f"{t2['n']} paragraphs with 3+ lines. Shortest line is the bottom line in {t2['bottom']}, "
             f"the top line in {t2['top']}, a middle line in {t2['middle']}, tied in {t2['ties']}.")
    r.append(f"Binomial test bottom vs top: p = {fmt_p(t2['p'])}. Decision: **{t2['verdict']}**.\n")

    r.append("## Test 3: letters in a word\n")
    r.append("L_k = ln(variety of word endings / variety of word beginnings), k letters. "
             "Below 0: endings less varied. Reading backwards flips the sign.\n")
    r.append("| Text | k=1 | k=2 | k=3 |\n|---|---|---|---|")
    for name, v in t3["refs"].items():
        r.append(f"| {name} | {v[1]:+.3f} | {v[2]:+.3f} | {v[3]:+.3f} |")
    for key, label in (("voynich", "Voynich (EVA letters)"), ("voynich_grouped", "Voynich (letter groups, robustness)")):
        v = t3[key]
        r.append(f"| {label} | " + " | ".join(f"{v[k][0]:+.3f} [{v[k][1]:+.3f}, {v[k][2]:+.3f}]" for k in (1, 2, 3)) + " |")
    r.append(f"\n{t3['n_words']} Voynich words (words with unreadable or rare-character marks left out). "
             "Brackets: 95% interval from resampling pages.\n")
    r.append(f"Decision: **{t3['verdict']}**.\n")

    r.append("## Test 4: pages in the book\n")
    r.append(f"{t4['n']} pages have paragraph text. Pages that end without a paragraph end: "
             f"{', '.join(t4['open_end']) or 'none'}. Pages that start without a paragraph start: "
             f"{', '.join(t4['open_start']) or 'none'}.")
    r.append(f"Fewer than 10 pages run on, so, as fixed in advance, **page direction {t4['verdict']}**. "
             "Almost every page starts and finishes its own text, so nothing in the writing shows which "
             "page comes next.\n")

    r.append("## Limits\n")
    r.append("- German could not be included as a reference (see `Data/reference/SOURCES.md`).")
    r.append("- Test 3 compares with Latin and Italian only. A language that puts its variety at word ends "
             "would look \"mirrored\" without being written backwards.")
    r.append("- Test 1's -m measure repeats a known result; the word-length measure is new.")
    return "\n".join(r) + "\n"


def main():
    rng = random.Random(SEED)
    folios = load()
    t1 = test1(folios, rng)
    t2 = test2(folios)
    t3 = test3(folios, rng)
    t4 = test4(folios)
    OUT.parent.mkdir(exist_ok=True)
    text = report(t1, t2, t3, t4)
    OUT.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
