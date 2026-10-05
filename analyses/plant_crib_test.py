#!/usr/bin/env python3
"""Plant-name crib test (analyses/plant_crib_prereg.md, amendment 'names and exact test')."""

from __future__ import annotations

import csv
import re
import string
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261014
N_NULL = 200
RESTARTS, STEPS = 4, 1500
OPEN = {"f9v": "fochor", "f16r": "pocheody", "f6v": "koary", "f2v": "kooiin", "f2r": "kydainy",
        "f15v": "poror", "f42r": "cho", "f32v": "kcheodaiin"}
MULTI = ["cth", "ckh", "cph", "cfh", "ch", "sh", "ee", "ii"]
TARGET = list(string.ascii_lowercase) + [""]


def units(w):
    out, i = [], 0
    while i < len(w):
        for m in MULTI:
            if w.startswith(m, i):
                out.append(m); i += len(m); break
        else:
            out.append(w[i]); i += 1
    return out


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def sim(a, b):
    return 1 - lev(a, b) / max(len(a), len(b), 1)


def fit(words, namelists, rng):
    U = sorted({u for w in words for u in w})
    best_total = -1
    for _ in range(RESTARTS):
        m = {u: TARGET[rng.integers(len(TARGET))] for u in U}
        page = [max(sim("".join(m[u] for u in w), n) for n in ns) for w, ns in zip(words, namelists)]
        score = sum(page)
        for _ in range(STEPS):
            u = U[rng.integers(len(U))]
            old = m[u]; m[u] = TARGET[rng.integers(len(TARGET))]
            new_page = [max(sim("".join(m[x] for x in w), n) for n in ns) if u in w else p
                        for w, ns, p in zip(words, namelists, page)]
            s = sum(new_page)
            if s >= score:
                score, page = s, new_page
            else:
                m[u] = old
        best_total = max(best_total, score / len(words))
    return best_total


def derangement(n, rng):
    while True:
        p = rng.permutation(n)
        if not np.any(p == np.arange(n)):
            return p


def job(args):
    words, namelists, seed = args
    return fit(words, namelists, np.random.default_rng(seed))


def run(folios, label, seed):
    names = {r["folio"]: [re.sub(r"[ '\-]", "", n.lower()) for n in r["names"].split("|")]
             for r in csv.DictReader(open(ROOT / "analyses" / "plant_names.csv"))}
    words = [units(OPEN[f]) for f in folios]
    nl = [names[f] for f in folios]
    rng = np.random.default_rng(seed)
    perms = [derangement(len(folios), rng) for _ in range(N_NULL)]
    tasks = [(words, nl, seed + 1)] + [(words, [nl[i] for i in p], seed + 2 + k) for k, p in enumerate(perms)]
    with Pool(4) as pool:
        res = pool.map(job, tasks)
    obs, null = res[0], np.array(res[1:])
    p = float((np.sum(null >= obs) + 1) / (N_NULL + 1))
    return obs, null, p


def main():
    allf = list(OPEN)
    three = ["f9v", "f16r", "f6v", "f2v"]
    L = ["# Plant-name crib test", "", "Pre-registration: `analyses/plant_crib_prereg.md`. Names: `analyses/plant_names.csv`.",
         f"One shared glyph-to-letter mapping fitted by hill-climbing ({RESTARTS} restarts × {STEPS} steps); "
         f"null = same search with names shuffled among pages ({N_NULL} derangements). Threshold p < 0.01.", ""]
    for label, fs, seed in (("Primary: 8 agreed plants", allf, SEED), ("Secondary: 4 three-way-agreed plants", three, SEED + 999)):
        obs, null, p = run(fs, label, seed)
        verdict = "SUPPORTED" if p < 0.01 else "NOT SUPPORTED"
        L += [f"## {label}", "",
              f"- Best mean similarity with true pairing: **{obs:.3f}**; shuffled pairings: mean {null.mean():.3f}, "
              f"95th pct {np.percentile(null, 95):.3f}, max {null.max():.3f}",
              f"- p = {p:.3g} → **{verdict}**", ""]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "plant_crib_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
