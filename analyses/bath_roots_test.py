#!/usr/bin/env python3
"""Do the bath-page roots appear in the bath-picture labels? (analyses/bath_roots_prereg.md)

    python analyses/bath_roots_test.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from scipy.stats import fisher_exact

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from parser import CORPUS_PATH, VoynichParser, parse_zl3b  # noqa: E402
from root_dictionary_test import root_of  # noqa: E402

BATH_ROOTS = {"rsh", "sheckh", "lsh", "lch"}
ALPHA = 0.01


def main():
    section = parse_zl3b(CORPUS_PATH).groupby("folio")["section"].first().to_dict()
    rows = []  # (folio, code, word, hit)
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.(L\w)>\s+(.*)", line)
        if not m:
            continue
        for t in re.split(r"[.,\s]+", re.sub(r"<[^>]*>", "", m.group(3))):
            w = VoynichParser.clean_token(t)
            if w:
                rows.append((m.group(1), m.group(2), w, root_of(w) in BATH_ROOTS))
    bio = [r for r in rows if section.get(r[0]) == "Biological"]
    rest = [r for r in rows if section.get(r[0]) != "Biological"]
    hb, hr = sum(r[3] for r in bio), sum(r[3] for r in rest)
    L = ["# Do the bath-page roots appear in the bath-picture labels?", "",
         "Pre-registration: `analyses/bath_roots_prereg.md`. Bath roots: rsh, sheckh, lsh, lch.", "",
         f"- Bath-page label words: {len(bio)}, hits **{hb}** ({hb / len(bio):.1%})",
         f"- Other label words: {len(rest)}, hits {hr} ({hr / len(rest):.1%})"]
    if hb + hr < 5:
        L.append("- **M1: too few to test** (fewer than 5 hits in total).")
    else:
        _, p = fisher_exact([[hb, len(bio) - hb], [hr, len(rest) - hr]], alternative="greater")
        L.append(f"- M1: one-sided Fisher p = {p:.3g} → **{'SUPPORTED' if p < ALPHA else 'NOT SUPPORTED'}**")
    pools = [r for r in bio if r[1] == "Lt"]
    figs = [r for r in bio if r[1] == "Ln"]
    hp, hf = sum(r[3] for r in pools), sum(r[3] for r in figs)
    _, p2 = fisher_exact([[hp, len(pools) - hp], [hf, len(figs) - hf]])
    L += ["", "## M2. Pools/tubes vs bathing figures (descriptive)", "",
          f"- Pool/tube label words: {len(pools)}, hits {hp}; figure label words: {len(figs)}, hits {hf}; "
          f"two-sided Fisher p = {p2:.3g}", "",
          "Hit words: " + (", ".join(f"{w} ({c}, {f})" for f, c, w, h in rows if h) or "none")]
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "bath_roots_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
