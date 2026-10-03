#!/usr/bin/env python3
"""Star-name crib and sound-shape comparison with other languages. (analyses/sound_shapes_prereg.md)

Requires: pip install wordfreq  (for Part B)

    python analyses/sound_shapes_test.py
"""

from __future__ import annotations

import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from comparison_fingerprint import LATIN_SOURCES, latin_words  # noqa: E402
from freqmatch_test import units  # noqa: E402
from parser import CORPUS_PATH, VoynichParser, parse_zl3b  # noqa: E402

SEED = 20261003
N_DRAWS = 10_000
V_VOY = set("aeoy")
STARS = ("aldebaran algol alhabor algomeisa alhaioth rigel bedalgeuze alramech wega altair deneb alferaz markab "
         "scheat alpheta rasalhague fomalhaut menkar calbalazet azimech calbalacrab algorab benenaz mirach alioth "
         "dubhe denebalgedi athoraye alnath alhena alchameluz enif").split()
GREEK_V = set("αεηιουωάέήίόύώϊϋΐΰ")
LANGS = ["it", "es", "ca", "pt", "fr", "ro", "de", "nl", "en", "sv", "da", "nb", "cs", "sk", "pl", "sl", "sh", "hu",
         "fi", "tr", "lt", "lv", "id", "ms", "fil", "el"]
LATIN_DIR = ROOT.parent / "cltk" / "lat_text_latin_library"


def cv_voynich(word):
    return "".join("V" if u in V_VOY else "C" for u in units(word, "S2"))


def cv_lang(word, lang=None):
    out = []
    for ch in word:
        if lang == "el":
            if ch in GREEK_V:
                out.append("V")
            elif ch.isalpha():
                out.append("C")
            continue
        base = unicodedata.normalize("NFD", ch)[0]
        if base in "aeiouy":
            out.append("V")
        elif ch.isalpha():
            out.append("C")
    return "".join(out)


def profile(pairs):
    c = Counter()
    for pat, w in pairs:
        if pat:
            c[pat if len(pat) <= 10 else "LONG"] += w
    t = sum(c.values())
    return {k: v / t for k, v in c.items()}


def jsd(p, q):
    keys = set(p) | set(q)
    a = np.array([p.get(k, 0) for k in keys])
    b = np.array([q.get(k, 0) for k in keys])
    m = (a + b) / 2
    kl = lambda x, y: np.sum(x[x > 0] * np.log2(x[x > 0] / y[x > 0]))
    return float((kl(a, m) + kl(b, m)) / 2)


def main():
    rng = np.random.default_rng(SEED)
    # Part A
    star_labels, other_labels = [], []
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.(L\w)>\s+(.*)", line)
        if not m:
            continue
        ws = [w for w in (VoynichParser.clean_token(t) for t in re.split(r"[.,\s]+", re.sub(r"<[^>]*>", "", m.group(3)))) if w]
        (star_labels if m.group(2) == "Ls" else other_labels).extend(ws)
    star_cv = {s: cv_lang(s) for s in STARS}

    def score(labels):
        pats = {cv_voynich(w) for w in labels}
        return sum(star_cv[s] in pats for s in STARS)

    obs = score(star_labels)
    null = np.array([score(list(rng.choice(other_labels, len(star_labels), replace=False))) for _ in range(N_DRAWS)])
    pA = float((np.sum(null >= obs) + 1) / (N_DRAWS + 1))
    pairs = [(s, star_cv[s], ", ".join(sorted({w for w in star_labels if cv_voynich(w) == star_cv[s]})))
             for s in STARS if any(cv_voynich(w) == star_cv[s] for w in star_labels)]
    L = ["# Star-name crib and sound shapes", "", f"Pre-registration: `analyses/sound_shapes_prereg.md`. Seed {SEED}.", "",
         "## Part A: star-name crib", "",
         f"- {len(STARS)} star names; {len(star_labels)} star-label words; {len(other_labels)} other label words.",
         f"- Star names whose consonant/vowel pattern matches a star label: **{obs}**; drawing the same number of other "
         f"labels: {null.mean():.1f} on average.",
         f"- p = {pA:.3g} → **{'SUPPORTED' if pA < 0.01 else 'NOT SUPPORTED'}**", "",
         "| Star name | Pattern | Star labels with the same pattern |", "|---|---|---|"]
    L += [f"| {s} | {cv} | {ws} |" for s, cv, ws in pairs]
    # Part B
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.clean.str.len() > 0)]
    prof = {f"Voynich {c}": profile([(cv_voynich(w), 1) for w in p[p.currier == c].clean]) for c in "AB"}
    shuf = {f"Voynich {c} (letters shuffled)": profile([(cv_voynich("".join(rng.permutation(list(w)))), 1)
                                                        for w in p[p.currier == c].clean]) for c in "AB"}
    lat = []
    for name, globs in LATIN_SOURCES.items():
        files = sorted(f for g in globs for f in LATIN_DIR.glob(g))
        lat += latin_words(" ".join(f.read_text(errors="ignore") for f in files))
    langs = {"Latin (medieval texts)": profile([(cv_lang(w), 1) for w in lat])}
    try:
        from wordfreq import top_n_list, word_frequency
        for lg in LANGS:
            ws = top_n_list(lg, 20000)
            langs[lg] = profile([(cv_lang(w.lower(), lg), word_frequency(w, lg)) for w in ws])
    except ImportError:
        L.append("\n(wordfreq not installed: Part B limited to Latin.)")
    L += ["", "## Part B: closest languages by sound shape (descriptive)", ""]
    for c in "AB":
        v = prof[f"Voynich {c}"]
        ranked = sorted(langs.items(), key=lambda kv: jsd(v, kv[1]))
        L.append(f"**Voynich {c}** (distance to its own shuffled-letter version: "
                 f"{jsd(v, shuf[f'Voynich {c} (letters shuffled)']):.3f}). Closest: " +
                 ", ".join(f"{k} {jsd(v, q):.3f}" for k, q in ranked[:8]) +
                 f". Farthest: {', '.join(f'{k} {jsd(v, q):.3f}' for k, q in ranked[-3:])}.")
        L.append("")
        top = sorted(v.items(), key=lambda kv: -kv[1])[:6]
        L.append(f"Most common Voynich {c} word shapes: " + ", ".join(f"{k} {x:.0%}" for k, x in top))
        L.append("")
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "sound_shapes_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
