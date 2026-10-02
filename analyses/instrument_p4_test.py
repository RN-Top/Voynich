#!/usr/bin/env python3
"""
Instrument hypothesis, prediction P4 (analyses/instrument_prereg.md).

Do non-zodiac circular diagrams repeat the same label at the same angular position?
Labels with a recorded clock position (<!hh:mm>) on non-zodiac circular pages are binned
into 12 clock-hour sectors. Statistic: number of cross-diagram label pairs with the same
first word in the same sector. Null: shuffle sector positions within each diagram
(10,000 times, seed 20261001). One-sided p.

Only line types other than running ring text (Cc/Ca) are used, so that each item is a
discrete label.

    python analyses/instrument_p4_test.py
"""

from __future__ import annotations

import itertools
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, VoynichParser  # noqa: E402

SEED = 20261001
N_PERMS = 10_000
NON_ZODIAC = re.compile(r"^f(57v|6[789]|8[56]|Ros)")


def labels():
    out = defaultdict(list)  # folio -> [(sector, word)]
    for line in open(CORPUS_PATH, encoding="utf-8", errors="ignore"):
        m = re.match(r"<(f[^.]+)\.\d+,.(\w\w)>\s+<!(\d\d):(\d\d)>(.*)", line)
        if not m or not NON_ZODIAC.match(m.group(1)) or m.group(2) in ("Cc", "Ca"):
            continue
        hour = int(m.group(3)) % 12
        word = VoynichParser.clean_token(re.split(r"[.,\s]+", re.sub(r"<[^>]*>", "", m.group(5)).strip())[0])
        if word:
            out[m.group(1)].append((hour, word))
    return dict(out)


def statistic(diagrams):
    count = 0
    for a, b in itertools.combinations(diagrams, 2):
        for (sa, wa) in a:
            for (sb, wb) in b:
                count += sa == sb and wa == wb
    return count


def main():
    lab = labels()
    names = sorted(lab)
    diagrams = [lab[n] for n in names]
    obs = statistic(diagrams)
    rng = np.random.default_rng(SEED)
    null = np.empty(N_PERMS)
    for i in range(N_PERMS):
        shuffled = []
        for d in diagrams:
            sectors = rng.permutation([s for s, _ in d])
            shuffled.append([(s, w) for s, (_, w) in zip(sectors, d)])
        null[i] = statistic(shuffled)
    p = float((np.sum(null >= obs) + 1) / (N_PERMS + 1))
    shared = sorted({w for d in diagrams for _, w in d if sum(w in [x for _, x in e] for e in diagrams) > 1})
    report = f"""# Instrument hypothesis: P4 (labels at the same angular position)

Pre-registration: `analyses/instrument_prereg.md`. {N_PERMS:,} shuffles, seed {SEED}.

- Diagrams with clock-positioned labels (non-zodiac, excluding ring text): {', '.join(f'{n} ({len(lab[n])})' for n in names)}
- Same word in the same clock sector across diagrams: **{obs}** (shuffled: {null.mean():.2f} on average)
- p = {p:.3g} → **{'PASS' if p < 0.01 else 'FAIL'}**
- Words that appear on more than one of these diagrams at all: {', '.join(shared) if shared else 'none'}

Caveat: only {len(names)} diagrams have positioned labels, so this test has little power.
"""
    (ROOT / "output").mkdir(exist_ok=True)
    (ROOT / "output" / "instrument_p4_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
