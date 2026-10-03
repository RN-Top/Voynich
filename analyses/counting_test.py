#!/usr/bin/env python3
"""Do zodiac labels build up steadily around each wheel? (analyses/counting_prereg.md)

    python analyses/counting_test.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from coordinates_test import MIN_LABELS  # noqa: E402
from freqmatch_test import units  # noqa: E402
from parser import CORPUS_PATH, VoynichParser  # noqa: E402

SEED = 20261003
N_PERMS = 5000


def best_fit(vals):
    """Best Spearman over all starts and both directions. vals: values in clock order."""
    n = len(vals)
    steps = np.arange(n)
    rs = rankdata(steps)
    best = (-2, 0, 1)
    for d in (1, -1):
        v = vals if d == 1 else vals[::-1]
        for s in range(n):
            seq = np.roll(v, -s)
            r = np.corrcoef(rs, rankdata(seq))[0, 1] if np.ptp(seq) > 0 else 0.0
            if r > best[0]:
                best = (r, s, d)
    return best


def main():
    diag = defaultdict(list)
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.(L\w)>\s+<!(\d\d):(\d\d)>(.*)", line)
        if not m:
            continue
        text = re.sub(r"<[^>]*>", "", m.group(5)).strip()
        w = VoynichParser.clean_token(re.split(r"[.,\s]+", text)[0]) if text else ""
        if w:
            diag[m.group(1)].append(((int(m.group(3)) % 12) * 60 + int(m.group(4)), f"{m.group(3)}:{m.group(4)}", w))
    diag = {f: sorted(v) for f, v in diag.items() if len(v) >= MIN_LABELS}
    rng = np.random.default_rng(SEED)
    L = ["# Do zodiac labels build up steadily around each wheel?", "",
         f"Pre-registration: `analyses/counting_prereg.md`. {len(diag)} wheels; best start and direction searched for "
         f"real and shuffled labels alike; {N_PERMS:,} shuffles, seed {SEED}.", ""]
    for measure, fn in (("letters", len), ("S2 symbols", lambda w: len(units(w, "S2")))):
        vals = {f: np.array([fn(w) for _, _, w in v], float) for f, v in diag.items()}
        obs_each = {f: best_fit(v) for f, v in vals.items()}
        S = float(np.mean([b[0] for b in obs_each.values()]))
        null = np.empty(N_PERMS)
        for t in range(N_PERMS):
            null[t] = np.mean([best_fit(rng.permutation(v))[0] for v in vals.values()])
        p = float((np.sum(null >= S) + 1) / (N_PERMS + 1))
        L += [f"## Complexity = {measure}", "",
              f"- Mean best correlation: **{S:.3f}** (shuffled with the same search: {null.mean():.3f}); p = {p:.3g} → "
              f"**{'SUPPORTED' if p < 0.01 else 'NOT SUPPORTED'}**", ""]
        if measure == "letters":
            L += ["| Wheel | Best start | Direction | Correlation |", "|---|---|---|---:|"]
            for f, (r, s, d) in obs_each.items():
                items = diag[f] if d == 1 else diag[f][::-1]
                L.append(f"| {f} | {items[s][1]} | {'clockwise' if d == 1 else 'counter-clockwise'} | {r:.2f} |")
            L.append("")
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "counting_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
