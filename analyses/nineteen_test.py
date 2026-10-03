#!/usr/bin/env python3
"""Is there a 19 (Metonic) structure in the diagrams? (analyses/nineteen_prereg.md)

    python analyses/nineteen_test.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH  # noqa: E402

SEED = 20261003
N_PERMS = 10_000
TARGETS = {19, 235, 6940}


def clean_text(t: str) -> str:
    t = re.sub(r"<![^>]*>", "", t)
    t = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", t)
    t = re.sub(r"<[^>]*>|[{}'*?]", "", t)
    return t


def glyphs(t: str):
    t = re.sub(r"[.,\s]+", "", t)
    return re.findall(r"@\d+;|[a-z]", t)


def words(t: str):
    return [w for w in re.split(r"[.,\s]+", t) if w]


def matches(seqs, k):
    return sum(sum(a == b for a, b in zip(s, s[k:])) for s in seqs)


def perm_test(seqs, k, rng):
    obs = matches(seqs, k)
    null = np.empty(N_PERMS)
    arrs = [np.array(s) for s in seqs]
    for i in range(N_PERMS):
        null[i] = sum(int(np.sum(a[:-k] == a[k:])) if len(a) > k else 0 for a in (rng.permutation(x) for x in arrs))
    return obs, float(null.mean()), float((np.sum(null >= obs) + 1) / (N_PERMS + 1))


def main():
    rings = defaultdict(list)  # folio -> list of ring texts
    counts = defaultdict(Counter)
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.(\w)(\w)>\s+(.*)", line)
        if not m:
            continue
        f, t1, t2, text = m.group(1), m.group(2), m.group(3), clean_text(m.group(4))
        if t1 == "C":
            rings[f].append(text)
            counts[f]["ring loci"] += 1
        elif t1 == "R":
            counts[f]["radial loci"] += 1
        elif t1 == "L":
            counts[f][f"labels L{t2}"] += 1
    found, n_counts = [], 0
    for f, c in counts.items():
        for k, v in c.items():
            n_counts += 1
            if v in TARGETS:
                found.append(f"{f}: {k} = {v}")
        for i, t in enumerate(rings.get(f, []), 1):
            n_counts += 1
            if len(words(t)) in TARGETS:
                found.append(f"{f}: words in ring {i} = {len(words(t))}")
    rng = np.random.default_rng(SEED)
    ctrl = perm_test([glyphs(t) for t in rings["f57v"]], 17, rng)
    all_w = [words(t) for ts in rings.values() for t in ts]
    all_g = [glyphs(t) for ts in rings.values() for t in ts]
    n1 = perm_test(all_w, 19, rng)
    n2 = perm_test(all_g, 19, rng)
    ok = ctrl[2] < 0.01
    v = lambda r, a: ("PASS" if r[2] < a else "FAIL") if ok else "uninformative (control failed)"
    L = ["# Is there a 19 (Metonic) structure in the diagrams?", "",
         f"Pre-registration: `analyses/nineteen_prereg.md`. {N_PERMS:,} shuffles within each ring, seed {SEED}.", "",
         "## Part 1: counts equal to 19, 235 or 6,940 (descriptive)", "",
         f"{n_counts} counts examined (ring, radial and label loci per page, and words per ring). Matches: " +
         ("; ".join(found) if found else "none"), "",
         "## Part 2: repetition with period 19 in ring texts", "",
         "| Test | Matching positions | Shuffled mean | p | Result |", "|---|---:|---:|---:|---|",
         f"| Control: f57v ring, glyphs, lag 17 | {ctrl[0]} | {ctrl[1]:.1f} | {ctrl[2]:.3g} | {'PASS' if ok else 'FAIL'} |",
         f"| N1: all rings, words, lag 19 | {n1[0]} | {n1[1]:.1f} | {n1[2]:.3g} | {v(n1, 0.005)} |",
         f"| N2: all rings, glyphs, lag 19 | {n2[0]} | {n2[1]:.1f} | {n2[2]:.3g} | {v(n2, 0.005)} |", "",
         f"Ring texts: {sum(len(ts) for ts in rings.values())} loci on {len(rings)} pages."]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "nineteen_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
