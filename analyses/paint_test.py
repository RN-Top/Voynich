#!/usr/bin/env python3
"""Measured paint colours on the plant pages (analyses/paint_prereg.md)

    python analyses/paint_test.py   (needs images/yale/ from fetch_yale_images.py)
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analyses"))

from parser import CORPUS_PATH, parse_zl3b  # noqa: E402
from root_dictionary_test import root_of  # noqa: E402
from scribes_test import hands  # noqa: E402

SEED = 20261013
N = 10_000
EXTRA = {"f87r": "87r", "f87v": "87v", "f90r1": "90r", "f90v1": "90v (part)", "f93r": "93r", "f93v": "93v",
         "f94r": "94r", "f95v1": "95v (part)", "f96r": "96r", "f96v": "96v"}
FAM = ["red", "ochre", "yellow", "green", "blue", "other"]


def profile(path):
    im = Image.open(path).convert("RGB")
    im = im.resize((800, int(800 * im.height / im.width)))
    hsv = np.asarray(im.convert("HSV")).astype(float) / 255.0
    h, s, v = hsv[..., 0] * 360, hsv[..., 1], hsv[..., 2]
    H, W = s.shape
    b = max(1, int(0.05 * min(H, W)))
    border = np.concatenate([s[:b].ravel(), s[-b:].ravel(), s[:, :b].ravel(), s[:, -b:].ravel()])
    paint = (s > np.median(border) + 0.12) & (v > 0.25)
    hh = h[paint]
    fam = np.full(hh.shape, 5)
    fam[(hh >= 345) | (hh < 15)] = 0
    fam[(hh >= 15) & (hh < 45)] = 1
    fam[(hh >= 45) & (hh < 70)] = 2
    fam[(hh >= 70) & (hh < 170)] = 3
    fam[(hh >= 170) & (hh < 260)] = 4
    c = np.bincount(fam, minlength=6).astype(float)
    return c / max(c.sum(), 1), int(paint.sum())


def main():
    idx = {r["label"]: r["file"] for r in csv.DictReader(open(ROOT / "images" / "yale" / "index.csv"))}
    df = parse_zl3b(CORPUS_PATH)
    herb = list(dict.fromkeys(df[df.section == "Herbal"].folio)) + list(EXTRA)
    lab = {f: EXTRA.get(f, f[1:]) for f in herb}
    P, npx = {}, {}
    for f in herb:
        P[f], npx[f] = profile(ROOT / "images" / "yale" / idx[lab[f]])
    pdat = df[(df.locus_type == "P") & (df.folio.isin(herb)) & (df.clean.str.len() > 0)]
    pages = [f for f in herb if (pdat.folio == f).any()]
    cur = pdat.groupby("folio").currier.agg(lambda s: s.mode()[0])
    quire = df.groupby("folio").quire.first()
    hand = hands()
    vecs = {f: Counter(pdat[pdat.folio == f].clean.map(root_of)) for f in pages}
    vocab = sorted(set().union(*vecs.values())); ix = {v: i for i, v in enumerate(vocab)}
    M = np.zeros((len(pages), len(vocab)))
    for i, f in enumerate(pages):
        for k, v in vecs[f].items():
            M[i, ix[k]] = v
    M /= np.linalg.norm(M, axis=1, keepdims=True)
    TD = 1 - M @ M.T
    C = np.array([P[f] for f in pages])
    CD = np.abs(C[:, None, :] - C[None, :, :]).sum(-1) / 2
    iu = np.triu_indices(len(pages), 1)
    rt = rankdata(TD[iu])

    def rho(order):
        cd = CD[np.ix_(order, order)][iu]
        a, b = rankdata(cd) - (len(rt) + 1) / 2, rt - (len(rt) + 1) / 2
        return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum()))

    base = np.arange(len(pages))
    obs = rho(base)
    groups = [np.flatnonzero(np.array([cur[f] for f in pages]) == c) for c in ("A", "B")]
    rng = np.random.default_rng(SEED)
    null = np.empty(N)
    for t in range(N):
        o = base.copy()
        for g in groups:
            o[g] = base[g][rng.permutation(len(g))]
        null[t] = rho(o)
    p = float((np.sum(null >= obs) + 1) / (N + 1))

    # exploratory
    allp = np.array([P[f] for f in herb])
    D = np.abs(allp[:, None] - allp[None]).sum(-1) / 2
    odd = np.argsort(-D.mean(1))[:5]
    from scipy.cluster.vq import kmeans2
    _, km = kmeans2(allp, 4, seed=SEED, minit="++")
    L = ["# Measured paint colours on the plant pages", "",
         f"Pre-registration: `analyses/paint_prereg.md`. {len(herb)} plant pages measured from full-resolution Yale images "
         f"({len(pages)} with paragraph text used in the test).", "",
         "## Confirmatory: does colour go with text?", "",
         f"- Spearman ρ (colour distance vs text distance): **{obs:+.4f}** (shuffled {null.mean():+.4f}); p = {p:.3g} → "
         f"**{'SUPPORTED' if p < 0.05 else 'NOT SUPPORTED'}**", "",
         "## Exploratory: overall palette (share of painted pixels)", "",
         "| " + " | ".join(FAM) + " |", "|" + "---:|" * 6,
         "| " + " | ".join(f"{x:.0%}" for x in allp.mean(0)) + " |", "",
         "## Exploratory: the 5 most unusual pages", "",
         "| Page | " + " | ".join(FAM) + " |", "|---|" + "---:|" * 6]
    L += [f"| {herb[i]} | " + " | ".join(f"{x:.0%}" for x in allp[i]) + " |" for i in odd]
    L += ["", "## Exploratory: four colour groups", "", "| Group | Pages | Mean profile | Scribes | Currier | Example pages |",
          "|---|---:|---|---|---|---|"]
    for g in range(4):
        fs = [f for f, k in zip(herb, km) if k == g]
        if not fs:
            continue
        prof = allp[km == g].mean(0)
        top = ", ".join(f"{FAM[j]} {prof[j]:.0%}" for j in np.argsort(-prof)[:3])
        L.append(f"| {g + 1} | {len(fs)} | {top} | {dict(Counter(hand.get(f, '?') for f in fs))} | "
                 f"{dict(Counter(cur.get(f, '?') for f in fs))} | {', '.join(fs[:8])}{' …' if len(fs) > 8 else ''} |")
    L += ["", "## Exploratory: colour by quire", "", "| Quire | Pages | " + " | ".join(FAM) + " |", "|---|---:|" + "---:|" * 6]
    for q in sorted({quire[f] for f in herb}):
        fs = [i for i, f in enumerate(herb) if quire[f] == q]
        L.append(f"| {q} | {len(fs)} | " + " | ".join(f"{x:.0%}" for x in allp[fs].mean(0)) + " |")
    with open(ROOT / "analyses" / "paint_profiles.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["folio", "paint_pixels", *FAM, "group"])
        for f, k in zip(herb, km):
            w.writerow([f, npx[f], *[f"{x:.4f}" for x in P[f]], k + 1])
    report = "\n".join(L) + "\n"
    (ROOT / "output" / "paint_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
