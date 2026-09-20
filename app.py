#!/usr/bin/env python3
"""
zodiac_positional_crib.py
Test whether EVA onset clusters track position in the zodiac rotas.

This is the only non-linguistic ground truth available: the pictures fix
the sign and the clockwise order of the nymphs/stars. If the same onset
family keeps landing in the same relative slot across two signs, you have
a crib. If not, the labels are just more of the generator.
"""

from collections import defaultdict, Counter
import re

# ---------------------------------------------------------------------------
# 1. Fused inventory  (benches + gallows treated as single units)
# ---------------------------------------------------------------------------
FUSE = {
    "ch": "CH", "sh": "SH",
    "ckh": "CKH", "cth": "CTH", "cph": "CPH", "cfh": "CFH",
    "ck": "CK", "ct": "CT", "cp": "CP", "cf": "CF",
}

def fuse(token: str) -> str:
    t = token.lower()
    for k, v in sorted(FUSE.items(), key=len, reverse=True):
        t = t.replace(k, v)
    return t

def onset(token: str) -> str:
    """First fused unit — the candidate 'role' we test for positional lock."""
    f = fuse(token)
    # strip leading uncertain markers
    f = re.sub(r"[*! :2] if len(f) >= 2 else f

# ---------------------------------------------------------------------------
# 2. Hand-curated Grove-ordered labels (replace with full Stolfi file)
#    Each entry: (page, sign, index_0_to_n, eva_label)
# ---------------------------------------------------------------------------
LABELS = [
    # Pisces f70v2 outer ring, clockwise from ~11:30  (19 labels)
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

    # Aries light f71r outer, clockwise from 10:30  (10 labels)
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

    # Virgo f72v2 outer, clockwise from 10:00  (18 labels)
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

    # Sagittarius f73v outer, clockwise from ~10:00  (16 labels)
    ("f73v", "Sagit", 0, "otoar"),
    ("f73v", "Sagit", 1, "ykeody"),
    ("f73v", "Sagit", 2, "okodeey"),
    ("f73v", "Sagit", 3, "qopchey"),
    ("f73v", "Sagit", 4, "opaiin"),
    ("f73v", "Sagit", 5, "qoteedy"),
    ("f73v", "Sagit", 6, "dp y"),
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

# ---------------------------------------------------------------------------
# 3. Normalize each label to a relative slot in [0, 1)
# ---------------------------------------------------------------------------
def rel_slot(idx: int, n: int) -> float:
    return idx / n if n > 1 else 0.0

# ---------------------------------------------------------------------------
# 4. Build per-onset distribution across signs
# ---------------------------------------------------------------------------
onset_slots = defaultdict(list)   # onset -> list of (sign, rel_slot)
sign_counts = Counter()

for page, sign, idx, lab in LABELS:
    if lab in ("***", "-", ""):
        continue
    n = sum(1 for p, s, i, l in LABELS if s == sign and l not in ("***", "-", ""))
    sign_counts = n
    o = onset(lab)
    onset_slots .append((sign, rel_slot(idx, n)))

# ---------------------------------------------------------------------------
# 5. Report: which onsets cluster in the same relative band across signs?
# ---------------------------------------------------------------------------
print("Onset | signs it appears in | mean rel slot | stdev | n")
print("-" * 70)
for o, entries in sorted(onset_slots.items(), key=lambda x: -len(x[1])):
    signs = sorted({s for s, _ in entries})
    if len(signs) < 2:
        continue
    slots = mean = sum(slots) / len(slots)
    var = sum((x - mean) ** 2 for x in slots) / len(slots)
    std = var ** 0.5
    print(f"{o:6} | {', '.join(signs):20} | {mean:5.2f}        | {std:5.2f} | {len(entries)}")

print()
print("Signs covered:", dict(sign_counts))
print()
print("If any onset shows low stdev (< 0.15) across 2+ signs, that's a")
print("positional lock — a candidate crib. Otherwise the labels are")
print("just more of the same generator.")