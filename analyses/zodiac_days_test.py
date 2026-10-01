#!/usr/bin/env python3
"""
Are the zodiac figure labels names of days? Implements analyses/zodiac_days_prereg.md.

    python analyses/zodiac_days_test.py

Writes output/zodiac_days_report.md and output/zodiac_days.json.
"""

from __future__ import annotations

import itertools
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from parser import CORPUS_PATH, VoynichParser  # noqa: E402

SEED = 20261001
N_PERMS = 10_000
JOIN = {"f71r": "f70v1", "f72r1": "f71v"}  # second half of Aries / Taurus -> first half


def zodiac_labels(path=CORPUS_PATH) -> dict[str, dict]:
    """Sign -> {'pages': [...], 'name': ..., 'labels': [first word of each Lz label, in order]}."""
    lines = open(path, encoding="utf-8", errors="ignore").read().splitlines()
    signs, current = {}, None
    for i, line in enumerate(lines):
        m = re.match(r"<(f\d+[rv]\d*)>\s+<!(.*)>", line)
        if m:
            folio = m.group(1)
            current = None
            if "$I=Z" in m.group(2):
                key = JOIN.get(folio, folio)
                name = lines[i + 2].lstrip("# ").strip() if i + 2 < len(lines) else folio
                entry = signs.setdefault(key, {"pages": [], "name": name, "labels": []})
                entry["pages"].append(folio)
                current = key
            continue
        m = re.match(r"<(f\d+[rv]\d*)\.\d+,.Lz>\s+(.*)", line)
        if m and current:
            text = re.sub(r"<[^>]*>", "", m.group(2))
            first = re.split(r"[.,\s]+", text.strip())[0]
            word = VoynichParser.clean_token(first)
            if word:
                signs[current]["labels"].append(word)
    return signs


def encode(signs):
    prefixes = sorted({w[:3] for s in signs.values() for w in s["labels"]})
    idx = {p: i for i, p in enumerate(prefixes)}
    return [np.array([idx[w[:3]] for w in s["labels"]]) for s in signs.values()]


def statistic(seqs) -> float:
    scores = []
    for a, b in itertools.combinations(seqs, 2):
        n = min(len(a), len(b))
        a2, b2 = a[:n], b[:n]
        match = a2[:, None] == b2[None, :]                       # (n, n)
        rot = (np.arange(n)[None, :] + np.arange(n)[:, None]) % n  # rot[r, k] = (k + r) % n
        per_rot = match[np.arange(n)[None, :], rot].mean(axis=1)
        scores.append(per_rot.max())
    return float(np.mean(scores))


def run():
    signs = zodiac_labels()
    seqs = encode(signs)
    obs = statistic(seqs)
    rng = np.random.default_rng(SEED)
    null = np.array([statistic([rng.permutation(s) for s in seqs]) for _ in range(N_PERMS)])
    p = float((np.sum(null >= obs - 1e-12) + 1) / (N_PERMS + 1))
    return {
        "signs": {k: {"name": v["name"], "pages": v["pages"], "n_labels": len(v["labels"]), "labels": v["labels"]}
                  for k, v in signs.items()},
        "statistic": obs, "null_mean": float(null.mean()), "null_sd": float(null.std()), "p": p,
        "decision": "Supported" if p < 0.01 else "Not supported",
    }


def render(r) -> str:
    rows = "\n".join(f"| {v['name']} | {', '.join(v['pages'])} | {v['n_labels']} | {' '.join(v['labels'][:8])} … |"
                     for v in r["signs"].values())
    return f"""# Are the zodiac figure labels names of days?

Pre-registration: `analyses/zodiac_days_prereg.md` (committed before this code). {N_PERMS:,} shuffles, seed {SEED}.

**Decision (pre-registered rule): {r['decision']}**

Mean best-rotation positional similarity across sign pairs (same first three letters): **{r['statistic']:.4f}**,
vs {r['null_mean']:.4f} ± {r['null_sd']:.4f} with label order shuffled within each sign. p = {r['p']:.3g}.

| Sign | Pages | Labels | First labels |
|---|---|---:|---|
{rows}
"""


def main():
    r = run()
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    (out / "zodiac_days.json").write_text(json.dumps(r, indent=2), encoding="utf-8")
    report = render(r)
    (out / "zodiac_days_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
