#!/usr/bin/env python3
"""f67r2 moons as full and hollow months (analyses/moon_months_prereg.md)

    python analyses/moon_months_test.py
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
ALPHA = 0.025
CENTRE = (1905, 745)  # the 8-pointed star at the middle of the ring, in photo pixels


def bigrams(w):
    s = "^" + w.replace(" ", "") + "$"
    return {s[i:i + 2] for i in range(len(s) - 1)}


def main():
    d = pd.read_csv(ROOT / "analyses" / "moon_months_f67r2.csv")
    d = d[d.colour != "unclear"].copy()
    d["angle"] = [math.degrees(math.atan2(x - CENTRE[0], CENTRE[1] - y)) % 360 for x, y in zip(d.x, d.y)]
    d = d.sort_values("angle").reset_index(drop=True)
    cols = d.colour.tolist()
    n = len(cols)
    changes = lambda c: sum(c[i] != c[(i + 1) % n] for i in range(n))
    a_obs = changes(cols)
    k_red = cols.count("red")
    arrs = [["red" if i in s else "gold" for i in range(n)] for s in itertools.combinations(range(n), k_red)]
    a_null = np.array([changes(c) for c in arrs])
    p1 = float(np.mean(a_null >= a_obs))

    labs = d.zl_label.str.split(" ", n=1).str[1].str.replace(r"[.,]", "", regex=True).tolist()
    B = [bigrams(w) for w in labs]
    J = np.array([[len(B[i] & B[j]) / len(B[i] | B[j]) for j in range(n)] for i in range(n)])
    iu = np.triu_indices(n, 1)

    def w_stat(red_set):
        same = np.array([(i in red_set) == (j in red_set) for i, j in zip(*iu)])
        return J[iu][same].mean() - J[iu][~same].mean()

    red_obs = {i for i, c in enumerate(cols) if c == "red"}
    w_obs = w_stat(red_obs)
    w_null = np.array([w_stat(set(s)) for s in itertools.combinations(range(n), k_red)])
    p2 = float(np.mean(w_null >= w_obs - 1e-12))

    v = lambda p: "SUPPORTED" if p < ALPHA else "NOT SUPPORTED"
    L = ["# f67r2: the 12 moons as full and hollow months", "",
         "Pre-registration: `analyses/moon_months_prereg.md`. Data: `analyses/moon_months_f67r2.csv` (hand readings of "
         "`uploads/yale_hires/f67r_spread.jpg`). Exact enumeration, threshold p < 0.025.", "",
         "## The ring, clockwise from the top", "", "| Moon | Angle | Colour | Label |", "|---|---:|---|---|"]
    L += [f"| {r.moon} | {r.angle:.0f}° | {r.colour} | {lab} |" for r, lab in zip(d.itertuples(), labs)]
    L += ["", f"Colour sequence: {' '.join('R' if c == 'red' else 'G' for c in cols)} ({k_red} red, {n - k_red} gold)", "",
          "## Test 1: do red and gold alternate?", "",
          f"- Colour changes around the ring: **{a_obs}** of a possible {n} (chance mean {a_null.mean():.2f}); "
          f"p = {p1:.3g} over all {len(arrs)} arrangements → **{v(p1)}**", "",
          "## Test 2: do the labels split by colour?", "",
          f"- Same-colour minus different-colour bigram similarity: **{w_obs:+.4f}** (chance mean {w_null.mean():+.4f}); "
          f"p = {p2:.3g} over all {len(w_null)} splits → **{v(p2)}**", ""]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "moon_months_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
