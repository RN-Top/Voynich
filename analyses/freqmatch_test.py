#!/usr/bin/env python3
"""Can a letter-for-letter key turn the Voynich into Latin? (analyses/freqmatch_prereg.md)

    python analyses/freqmatch_test.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from comparison_fingerprint import LATIN_SOURCES, latin_words  # noqa: E402
from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

SEED = 20261003
RESTARTS, ITERS = 5, 20_000
LATIN_DIR = ROOT.parent / "cltk" / "lat_text_latin_library"
B = "_"
CLUSTERS = ["cth", "ckh", "cph", "cfh", "ch", "sh"]


def units(word: str, scheme: str):
    if scheme == "S1":
        return list(word)
    out, i = [], 0
    while i < len(word):
        for c in CLUSTERS:
            if word.startswith(c, i):
                out.append(c)
                i += len(c)
                break
        else:
            out.append(word[i])
            i += 1
    return out


def seq(words, scheme="S1"):
    s = [B]
    for w in words:
        s += units(w, scheme) + [B]
    return s


class Model:
    def __init__(self, train_seq):
        self.letters = sorted(set(train_seq) - {B}, key=lambda c: -train_seq.count(c))
        self.alpha = self.letters + [B]
        ix = {c: i for i, c in enumerate(self.alpha)}
        n = len(self.alpha)
        C = np.full((n, n), 0.5)
        a = np.array([ix[c] for c in train_seq])
        np.add.at(C, (a[:-1], a[1:]), 1)
        self.logp = np.log2(C / C.sum(1, keepdims=True))
        self.ix = ix

    def score_true(self, s):
        a = np.array([self.ix[c] for c in s])
        return float(self.logp[a[:-1], a[1:]].mean())


def solve(s, model: Model, rng):
    """s: symbol sequence with B boundaries. Returns (best score, key dict symbol->letter)."""
    L = len(model.letters)
    freq = Counter(c for c in s if c != B)
    syms = [c for c, _ in freq.most_common()]
    keep = syms[:L - 1] if len(syms) > L else syms
    other = len(keep) < len(syms)
    sym_list = keep + (["<other>"] if other else []) + [B]
    six = {c: i for i, c in enumerate(sym_list)}
    a = np.array([six.get(c, six.get("<other>", 0)) if c != B else six[B] for c in s])
    n = len(sym_list)
    C = np.zeros((n, n))
    np.add.at(C, (a[:-1], a[1:]), 1)
    total = C.sum()
    nb = n - 1  # non-boundary symbols, all mapped to distinct letters
    best_s, best_key = -1e9, None
    for r in range(RESTARTS):
        key = np.arange(nb) if r == 0 else rng.permutation(L)[:nb]
        key = np.append(key, model.ix[B])
        pool = [i for i in range(L) if i not in set(key[:nb])]

        def sc(k):
            return float((C * model.logp[np.ix_(k, k)]).sum() / total)

        cur = sc(key)
        for _ in range(ITERS):
            k2 = key.copy()
            i = rng.integers(nb)
            if pool and rng.random() < 0.3:
                j = rng.integers(len(pool))
                k2[i], pool_val = pool[j], k2[i]
                new = sc(k2)
                if new > cur:
                    pool[j] = pool_val
                    key, cur = k2, new
            else:
                j = rng.integers(nb)
                k2[i], k2[j] = k2[j], k2[i]
                new = sc(k2)
                if new > cur:
                    key, cur = k2, new
        if cur > best_s:
            best_s, best_key = cur, {sym_list[i]: model.alpha[key[i]] for i in range(nb)}
    return best_s, best_key


def main():
    rng = np.random.default_rng(SEED)
    train, held = [], []
    for name, globs in LATIN_SOURCES.items():
        files = sorted(f for g in globs for f in LATIN_DIR.glob(g))
        w = latin_words(" ".join(f.read_text(errors="ignore") for f in files))
        cut = int(len(w) * 0.8)
        train += w[:cut]
        held += w[cut:]
    model = Model(seq(train))
    held = held[:30000]
    held_seq = seq(held)
    ceiling = model.score_true(held_seq)
    # control: random substitution of held-out Latin
    letters = model.letters
    perm = dict(zip(letters, rng.permutation(letters)))
    inv = {v: k for k, v in perm.items()}
    enc = [perm[c] if c != B else B for c in held_seq]
    ctrl_score, ctrl_key = solve(enc, model, rng)
    correct = sum(ctrl_key.get(c) == inv[c] for c in enc if c != B) / sum(c != B for c in enc)
    # floor: letters shuffled within words
    shuf_words = ["".join(rng.permutation(list(w))) for w in held]
    floor, _ = solve(seq(shuf_words), model, rng)
    ok = correct >= 0.9
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.clean.str.len() > 0)]
    first_line = p[(p.folio == "f1r")].groupby("header", sort=False).clean.apply(list).iloc[0]
    L = ["# Can a letter-for-letter key turn the Voynich into Latin?", "",
         f"Pre-registration: `analyses/freqmatch_prereg.md`. Latin model: letter pairs from three Latin texts (80%); "
         f"{RESTARTS} restarts × {ITERS:,} swaps per solve; seed {SEED}.", "",
         f"- Ceiling (real held-out Latin): {ceiling:.3f} bits/char",
         f"- Control (Latin under a random key, solved): {ctrl_score:.3f}; letters recovered **{correct:.0%}** → "
         f"{'method works' if ok else 'METHOD FAILED: results uninformative'}",
         f"- Floor (Latin letters shuffled within words, solved): {floor:.3f}", "",
         "| Text | Symbols | Best score | Position (0 = floor, 1 = Latin) | f1r line 1 under best key |",
         "|---|---|---:|---:|---|"]
    positions = []
    for cur in ("A", "B"):
        words = p[p.currier == cur].clean.tolist()
        for scheme in ("S1", "S2"):
            s = seq(words, scheme)
            sc, key = solve(s, model, rng)
            pos = (sc - floor) / (ceiling - floor)
            positions.append(pos)
            demo = " ".join("".join(key.get(u, "?") for u in units(w, scheme)) for w in first_line)
            L.append(f"| Voynich {cur} | {scheme} | {sc:.3f} | {pos:.2f} | {demo} |")
    if not ok:
        verdict = "UNINFORMATIVE (control failed)"
    elif all(x < 0.5 for x in positions):
        verdict = "NOT SIMPLE-SUBSTITUTION LATIN"
    elif any(x >= 0.9 for x in positions):
        verdict = "CONSISTENT WITH SUBSTITUTION"
    else:
        verdict = "UNCLEAR"
    L += ["", f"**Verdict: {verdict}.**"]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "freqmatch_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
