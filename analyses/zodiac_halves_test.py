#!/usr/bin/env python3
"""Do the two halves of the same zodiac sign share label vocabulary? (analyses/zodiac_halves_prereg.md)

    python analyses/zodiac_halves_test.py
"""

from __future__ import annotations

import itertools
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, VoynichParser  # noqa: E402

PAGES = ["f70v1", "f70v2", "f71r", "f71v", "f72r1", "f72r2", "f72r3", "f72v1", "f72v2", "f72v3", "f73r", "f73v"]
SAME_SIGN = [("f70v1", "f71r"), ("f71v", "f72r1")]
CLOSE_DIFFERENT = [("f70v1", "f70v2"), ("f72r1", "f72r2"), ("f72r1", "f72r3"), ("f72r2", "f72r3"),
                   ("f72v1", "f72v2"), ("f72v1", "f72v3"), ("f72v2", "f72v3"), ("f70v2", "f71r"), ("f71r", "f71v")]
ALPHA = 0.01


def page_labels():
    out = {p: [] for p in PAGES}
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.Lz>\s+(.*)", line)
        if not m or m.group(1) not in out:
            continue
        text = re.sub(r"<[^>]*>", "", m.group(2)).strip()
        w = VoynichParser.clean_token(re.split(r"[.,\s]+", text)[0]) if text else ""
        if len(w) >= 2:
            out[m.group(1)].append(w)
    return out


def cosine(a: Counter, b: Counter) -> float:
    keys = set(a) | set(b)
    va, vb = np.array([a[k] for k in keys], float), np.array([b[k] for k in keys], float)
    return float(va @ vb / (np.linalg.norm(va) * np.linalg.norm(vb)))


def main():
    lab = page_labels()
    beg = {p: Counter(w[:2] for w in ws) for p, ws in lab.items()}
    sim = {frozenset(pr): cosine(beg[pr[0]], beg[pr[1]]) for pr in itertools.combinations(PAGES, 2)}
    same = [sim[frozenset(p)] for p in SAME_SIGN]
    S = float(np.mean(same))
    diff_pairs = [k for k in sim if k not in {frozenset(p) for p in SAME_SIGN}]
    means = [np.mean([sim[a], sim[b]]) for a, b in itertools.combinations(diff_pairs, 2)]
    p = float(np.mean(np.array(means) >= S))
    close = float(np.mean([sim[frozenset(p_)] for p_ in CLOSE_DIFFERENT]))
    z1, z2 = p < ALPHA, S > close
    words_shared = {f"{a}+{b}": sorted(set(lab[a]) & set(lab[b])) for a, b in SAME_SIGN}
    report = f"""# Do the two halves of the same zodiac sign share label vocabulary?

Pre-registration: `analyses/zodiac_halves_prereg.md`. Labels per page: {', '.join(f'{p} {len(lab[p])}' for p in PAGES)}.

| | Similarity of label beginnings |
|---|---:|
| Aries halves (f70v1 + f71r) | {same[0]:.3f} |
| Taurus halves (f71v + f72r1) | {same[1]:.3f} |
| **Same-sign mean S** | **{S:.3f}** |
| All different-sign pairs, mean | {np.mean([sim[k] for k in diff_pairs]):.3f} |
| Physically close different-sign pairs, mean | {close:.3f} |

- Z1: p = {p:.3g} ({len(means):,} pairs of different-sign pairs) → **{'PASS' if z1 else 'FAIL'}**
- Z2: S {'>' if z2 else '≤'} close-pair mean → **{'PASS' if z2 else 'FAIL'}**

**Verdict: {'SUPPORTED' if z1 and z2 else 'NOT SUPPORTED'}.**

Exact words shared by the two halves (descriptive): {'; '.join(f"{k}: {', '.join(v) if v else 'none'}" for k, v in words_shared.items())}.
"""
    (ROOT / "output" / "zodiac_halves_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
