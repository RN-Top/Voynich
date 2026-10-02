#!/usr/bin/env python3
"""Does the manuscript favour Fibonacci numbers? (analyses/fibonacci_prereg.md)

    python analyses/fibonacci_test.py
"""

from __future__ import annotations

import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402

ALPHA = 0.005
FIB = [5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
DOUBLED = [10, 16, 26, 42]


def binom_sf(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def counts():
    df = parse_zl3b(CORPUS_PATH)
    p = df[(df.locus_type == "P") & (df.clean.str.len() > 0)].copy()
    p["line"] = p.folio + "|" + p.header
    p["para"] = (p.groupby("folio")["is_para_end"].shift(fill_value=False).astype(int)).groupby(p.folio).cumsum()
    out = {
        "words per line": p.groupby("line").size().tolist(),
        "letters per word": p.clean.str.len().tolist(),
        "lines per paragraph": p.groupby(["folio", "para"])["line"].nunique().tolist(),
        "paragraph lines per page": p.groupby("folio")["line"].nunique().tolist(),
        "paragraph words per page": p.groupby("folio").size().tolist(),
    }
    labels = Counter()
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.L\w>", line)
        if m:
            labels[m.group(1)] += 1
    out["labels per page"] = list(labels.values())
    return out


def run(targets, data):
    rows, hits, total = [], 0, 0
    for name, vals in data.items():
        c = Counter(vals)
        for t in targets:
            w = c[t - 1] + c[t] + c[t + 1]
            if w:
                rows.append((name, t, c[t - 1], c[t], c[t + 1]))
                hits += c[t]
                total += w
    return rows, hits, total


def main():
    data = counts()
    L = ["# Does the manuscript favour Fibonacci numbers?", "",
         "Pre-registration: `analyses/fibonacci_prereg.md`. Each target is compared with its two neighbours; "
         "no preference means about 1 in 3 of the values in each window land on the target.", ""]
    for label, targets in (("F: Fibonacci", FIB), ("D: doubled sequence", DOUBLED)):
        rows, hits, total = run(targets, data)
        p = binom_sf(hits, total, 1 / 3) if total else 1.0
        L += [f"## {label}", "",
              f"- On target: **{hits} of {total}** ({hits / total:.1%}; no preference ≈ 33.3%)" if total else "- no data",
              f"- p = {p:.3g} → **{'PASS' if p < ALPHA else 'FAIL'}**", "",
              "| Count | Target | One below | On target | One above |", "|---|---:|---:|---:|---:|"]
        L += [f"| {n} | {t} | {a} | {b} | {c} |" for n, t, a, b, c in rows]
        L.append("")
    report = "\n".join(L)
    (ROOT / "output" / "fibonacci_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
