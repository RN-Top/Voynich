#!/usr/bin/env python3
"""
zodiac_positional_crib.py

Test whether EVA onset clusters track position in the zodiac rotas.

The pictures fix the sign and the clockwise order of the nymphs/stars.
If the same onset family keeps landing in the same relative slot across
two or more signs, that is a positional lock — a candidate crib.
If not, the labels are just more of the same generator.
"""

from collections import defaultdict, Counter
import math
import re


# ---------------------------------------------------------------------------
# 1. Fused inventory (benches + gallows treated as single units)
# ---------------------------------------------------------------------------
FUSE = {
    "ckh": "CKH",
    "cth": "CTH",
    "cph": "CPH",
    "cfh": "CFH",
    "ch": "CH",
    "sh": "SH",
}


def fuse(token: str) -> str:
    t = token.lower()
    t = re.sub(r"[*!:?,.]", "", t)
    t = t.replace(" ", "")
    for k, v in sorted(FUSE.items(), key=lambda kv: len(kv[0]), reverse=True):
        t = t.replace(k, v)
    return t


def onset(token: str) -> str:
    """First fused unit — the candidate role tested for positional lock."""
    f = fuse(token)
    if not f:
        return ""
    if f.startswith(("CKH", "CTH", "CPH", "CFH")):
        return f[:3]
    if f.startswith(("CH", "SH", "qo", "ok", "ot", "yt", "op", "of")):
        return f[:2]
    return f[:2] if len(f) >= 2 else f


# ---------------------------------------------------------------------------
# 2. Hand-curated Grove-ordered labels
#    Each entry: (page, sign, index_0_to_n, eva_label)
#    Replace this list with a full Stolfi/Grove dump when you have it.
# ---------------------------------------------------------------------------
LABELS = [
    # Pisces f70v2 outer ring, clockwise from ~11:30
    ("f70v2", "Pisces", 0, "oty"),
    ("f70v2", "Pisces", 1, "oky.amy"),
    ("f70v2", "Pisces", 2, "oty.ar"),
    ("f70v2", "Pisces", 3, "okaly"),
    ("f70v2", "Pisces", 4, "otody"),
    ("f70v2", "Pisces", 5, "otald"),
    ("f70v2", "Pisces", 6, "otaldar"),
    ("f70v2", "Pisces", 7, "okody"),
    ("f70v2", "Pisces", 8, "opys.am"),
    ("f70v2", "Pisces", 9, "chckhey"),
    ("f70v2", "Pisces", 10, "otaly"),
    ("f70v2", "Pisces", 11, "otal.arar"),
    ("f70v2", "Pisces", 12, "otaldy"),
    ("f70v2", "Pisces", 13, "okeoly"),
    ("f70v2", "Pisces", 14, "okydy"),
    ("f70v2", "Pisces", 15, "okees"),
    ("f70v2", "Pisces", 16, "otalalg"),
    ("f70v2", "Pisces", 17, "okasy"),
    ("f70v2", "Pisces", 18, "otar.r"),
    # Aries light f71r outer, clockwise from 10:30
    ("f71r", "Aries", 0, "oteos.arar"),
    ("f71r", "Aries", 1, "okldam"),
    ("f71r", "Aries", 2, "oteoaldy"),
    ("f71r", "Aries", 3, "oteolar"),
    ("f71r", "Aries", 4, "okeoaly"),
    ("f71r", "Aries", 5, "otaleky"),
    ("f71r", "Aries", 6, "opalsar"),
    ("f71r", "Aries", 7, "cheary"),
    ("f71r", "Aries", 8, "oteotey.sary"),
    ("f71r", "Aries", 9, "otalaly"),
    # Virgo f72v2 outer, clockwise from 10:00
    ("f72v2", "Virgo", 0, "oeedey"),
    ("f72v2", "Virgo", 1, "oeeo.daiin"),
    ("f72v2", "Virgo", 2, "okeoram"),
    ("f72v2", "Virgo", 3, "air.aim"),
    ("f72v2", "Virgo", 4, "ocsesy"),
    ("f72v2", "Virgo", 5, "okeosy"),
    ("f72v2", "Virgo", 6, "cheoekry"),
    ("f72v2", "Virgo", 7, "***"),
    ("f72v2", "Virgo", 8, "csedeky"),
    ("f72v2", "Virgo", 9, "oteodar"),
    ("f72v2", "Virgo", 10, "opchdy.sd"),
    ("f72v2", "Virgo", 11, "oteeod"),
    ("f72v2", "Virgo", 12, "yteody"),
    ("f72v2", "Virgo", 13, "okeody"),
    ("f72v2", "Virgo", 14, "okeoldy"),
    ("f72v2", "Virgo", 15, "ykeeos"),
    ("f72v2", "Virgo", 16, "opaiin.ar"),
    ("f72v2", "Virgo", 17, "cheoldy"),
    # Sagittarius f73v outer, clockwise from ~10:00
    ("f73v", "Sagit", 0, "otoar"),
    ("f73v", "Sagit", 1, "ykeody"),
    ("f73v", "Sagit", 2, "okodeey"),
    ("f73v", "Sagit", 3, "qopchey"),
    ("f73v", "Sagit", 4, "opaiin"),
    ("f73v", "Sagit", 5, "qoteedy"),
    ("f73v", "Sagit", 6, "dpy"),
    ("f73v", "Sagit", 7, "otedy"),
    ("f73v", "Sagit", 8, "csedy"),
    ("f73v", "Sagit", 9, "qokeody"),
    ("f73v", "Sagit", 10, "cheoral"),
    ("f73v", "Sagit", 11, "okedal"),
    ("f73v", "Sagit", 12, "oteody"),
    ("f73v", "Sagit", 13, "shedy"),
    ("f73v", "Sagit", 14, "otesalod"),
    ("f73v", "Sagit", 15, "air.chy"),
]


SKIP = {"***", "-", "", "?"}


def rel_slot(idx: int, n: int) -> float:
    return idx / n if n > 1 else 0.0


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def stdev(xs):
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def main():
    usable = [row for row in LABELS if row[3] not in SKIP]
    sign_n = Counter(sign for _, sign, _, _ in usable)

    onset_slots = defaultdict(list)  # onset -> list of (sign, rel_slot, label)

    for page, sign, idx, lab in usable:
        n = sign_n[sign]
        o = onset(lab)
        if not o:
            continue
        onset_slots[o].append((sign, rel_slot(idx, n), lab))

    print("Onset | signs                  | mean slot | stdev | n")
    print("-" * 68)

    locked = []
    for o, entries in sorted(onset_slots.items(), key=lambda kv: -len(kv[1])):
        signs = sorted({s for s, _, _ in entries})
        if len(signs) < 2:
            continue
        slots = [sl for _, sl, _ in entries]
        m = mean(slots)
        s = stdev(slots)
        print(f"{o:6} | {', '.join(signs):22} | {m:7.2f}   | {s:5.2f} | {len(entries)}")
        if s < 0.15:
            locked.append((o, signs, m, s, len(entries)))

    print()
    print("Signs covered:", dict(sign_n))
    print()
    if locked:
        print("Candidate positional locks (stdev < 0.15 across 2+ signs):")
        for o, signs, m, s, n in locked:
            print(f"  {o}: signs={signs} mean={m:.2f} stdev={s:.2f} n={n}")
    else:
        print("No onset locked to a relative slot across two or more signs.")
        print("On this sample the labels do not know where they are.")


if __name__ == "__main__":
    main()
