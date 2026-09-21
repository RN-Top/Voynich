#!/usr/bin/env python3
"""
break_phonetic_cribs.py

Topological & Phonetic Crib Matcher for Voynich Zodiac Rotas (f70v-f73v).
Matches radial label stems against Ptolemaic/medieval decan rulers using
Sukhotin-derived CV skeletal structures.
"""

import os
import re
from typing import Dict, List, Tuple

# ---------------------------------------------------------
# 1. Phonological Partition (Sukhotin Algorithm Grounding)
# ---------------------------------------------------------
VOWELS = set(['a', 'o', 'h', 't', 'i', 'y'])
CONSONANTS = set(['c', 'd', 'e', 'f', 'k', 'l', 'm', 'n'])

# ---------------------------------------------------------
# 2. Historical 15th-Century Decan Ground Truth Rota
# Canonical Ptolemaic/Alfonsine astrological faces & rulers
# ---------------------------------------------------------
CANONICAL_DECANS = [
    # Aries (March/April)
    ("Aries I", "Mars", "CVCC"),
    ("Aries II", "Sol", "CVC"),
    ("Aries III", "Venus", "CVCVC"),
    # Taurus (April/May)
    ("Taurus I", "Mercurius", "CVCCVCVVC"),
    ("Taurus II", "Luna", "CVCV"),
    ("Taurus III", "Saturnus", "CVCVCCVC"),
    # Gemini (May/June)
    ("Gemini I", "Jupiter", "CVCVCVC"),
    ("Gemini II", "Mars", "CVCC"),
    ("Gemini III", "Sol", "CVC"),
    # Cancer (June/July)
    ("Cancer I", "Venus", "CVCVC"),
    ("Cancer II", "Mercurius", "CVCCVCVVC"),
    ("Cancer III", "Luna", "CVCV"),
    # Leo (July/August)
    ("Leo I", "Saturnus", "CVCVCCVC"),
    ("Leo II", "Jupiter", "CVCVCVC"),
    ("Leo III", "Mars", "CVCC"),
    # Virgo (August/September)
    ("Virgo I", "Sol", "CVC"),
    ("Virgo II", "Venus", "CVCVC"),
    ("Virgo III", "Mercurius", "CVCCVCVVC"),
    # Libra (September/October)
    ("Libra I", "Luna", "CVCV"),
    ("Libra II", "Saturnus", "CVCVCCVC"),
    ("Libra III", "Jupiter", "CVCVCVC"),
    # Scorpio (October/November)
    ("Scorpio I", "Mars", "CVCC"),
    ("Scorpio II", "Sol", "CVC"),
    ("Scorpio III", "Venus", "CVCVC"),
    # Sagittarius (November/December)
    ("Sagittarius I", "Mercurius", "CVCCVCVVC"),
    ("Sagittarius II", "Luna", "CVCV"),
    ("Sagittarius III", "Saturnus", "CVCVCCVC"),
    # Capricorn (December/January)
    ("Capricorn I", "Jupiter", "CVCVCVC"),
    ("Capricorn II", "Mars", "CVCC"),
    ("Capricorn III", "Sol", "CVC"),
    # Aquarius (January/February)
    ("Aquarius I", "Venus", "CVCVC"),
    ("Aquarius II", "Mercurius", "CVCCVCVVC"),
    ("Aquarius III", "Luna", "CVCV"),
    # Pisces (February/March)
    ("Pisces I", "Saturnus", "CVCVCCVC"),
    ("Pisces II", "Jupiter", "CVCVCVC"),
    ("Pisces III", "Mars", "CVCC")
]

# ---------------------------------------------------------
# 3. Text Processing & Morphotactic Isolation
# ---------------------------------------------------------
def strip_carrier(tok: str) -> str:
    """Strips operational prefixes and exit switches to isolate carrier core Lambda."""
    s = re.sub(r"[^a-z]", "", str(tok).lower().strip())
    if not s:
        return ""
    # Strip prefixes
    for p in ("qk", "dk", "qo", "ch", "sh", "q", "k", "d", "t"):
        if s.startswith(p):
            s = s[len(p):]
            break
    # Strip exit suffixes
    for ep in ("aiiin", "aiin", "ain", "eedy", "edy", "eey", "ey", "al", "ar", "am", "or", "ol", "m", "y"):
        if s.endswith(ep):
            s = s[:-len(ep)]
            break
    return s if s else "core"

def word_to_cv_skeleton(word: str) -> str:
    """Converts a word into a CV skeletal pattern based on Sukhotin partition."""
    skel = []
    for c in word.lower():
        if c in VOWELS:
            skel.append("V")
        elif c in CONSONANTS:
            skel.append("C")
        else:
            # Fallback for standard Latin characters in cribs
            if c in "aeiouy":
                skel.append("V")
            elif c.isalpha():
                skel.append("C")
    return "".join(skel)

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates edit distance between two strings/skeletons."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

# ---------------------------------------------------------
# 4. Corpus Parsing: Extract Zodiac Ring Labels
# ---------------------------------------------------------
def load_zodiac_tokens() -> List[Dict[str, str]]:
    """Loads tokens specifically located in zodiac folios (f70v to f73v)."""
    target_folios = {"f70v", "f71r", "f71v", "f72r1", "f72r2", "f72r3", 
                     "f72v1", "f72v2", "f72v3", "f73r", "f73v", "f74r"}
    
    extracted = []
    filepath = "data/ZL3b-n.txt"
    
    if not os.path.exists(filepath):
        # Fallback minimal corpus for testing if file missing
        sample_astro = [
            ("f70v", "otcheodal"), ("f70v", "opairam"), ("f71r", "oteodal"),
            ("f72r2", "okaly"), ("f72v1", "airam"), ("f73r", "oeeodal")
        ]
        return [{"folio": f, "token": t, "core": strip_carrier(t)} for f, t in sample_astro]

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if not line.startswith("<f"):
                continue
            
            # Extract header and tokens
            try:
                header, text = line.split(">", 1)
                header = header.replace("<", "").strip()
                folio = header.split(".")[0]
                
                if folio in target_folios:
                    # Strip markup annotations
                    clean_text = re.sub(r"<[^>]*>", "", text)
                    words = re.split(r"[.,\s]+", clean_text)
                    for w in words:
                        clean_w = re.sub(r"[^a-z]", "", w.lower())
                        if len(clean_w) >= 3:
                            extracted.append({
                                "folio": folio,
                                "token": clean_w,
                                "core": strip_carrier(clean_w)
                            })
            except Exception:
                continue

    return extracted

# ---------------------------------------------------------
# 5. Core Execution & Matcher
# ---------------------------------------------------------
def run_crib_analysis():
    print("=" * 70)
    print("VOYNICH TOPOLOGICAL DECIPHERMENT: ZODIAC RADIAL CRIB MATCHER")
    print("=" * 70)
    
    zodiac_tokens = load_zodiac_tokens()
    print(f"Loaded {len(zodiac_tokens)} label tokens across folios f70v-f74r.")
    
    # Isolate unique carriers and compute skeletons
    unique_entries = {}
    for entry in zodiac_tokens:
        core = entry["core"]
        if core not in unique_entries:
            unique_entries[core] = {
                "sample_token": entry["token"],
                "folio": entry["folio"],
                "count": 1,
                "cv_skel": word_to_cv_skeleton(core)
            }
        else:
            unique_entries[core]["count"] += 1

    print(f"Isolated {len(unique_entries)} invariant carrier cores (Lambda).")
    print("\n--- Skeletal Alignment Against Canonical 15th-C. Decan Rulers ---")

    best_matches = []
    for decan_id, ruler_name, ruler_skel in CANONICAL_DECANS:
        for core, data in unique_entries.items():
            core_skel = data["cv_skel"]
            dist = levenshtein_distance(core_skel, ruler_skel)
            
            # Match score scaled by length
            max_len = max(len(core_skel), len(ruler_skel))
            similarity = 1.0 - (dist / max_len)
            
            if similarity >= 0.70 and len(core) >= 3:
                best_matches.append({
                    "decan": decan_id,
                    "ruler": ruler_name,
                    "ruler_skel": ruler_skel,
                    "voynich_carrier": core,
                    "sample_token": data["sample_token"],
                    "carrier_skel": core_skel,
                    "folio": data["folio"],
                    "similarity": similarity
                })

    # Sort by similarity descending
    best_matches.sort(key=lambda x: x["similarity"], reverse=True)

    # Display Top Candidates
    seen_pairs = set()
    displayed = 0
    for m in best_matches:
        pair_key = (m["ruler"], m["voynich_carrier"])
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)
        
        print(f"Match [{m['similarity']*100:.1f}%] -> {m['decan']} ({m['ruler']})")
        print(f"  Ruler Skeletal CV : {m['ruler_skel']}")
        print(f"  Voynich Carrier   : {m['voynich_carrier']} (from '{m['sample_token']}' on {m['folio']})")
        print(f"  Voynich Skeletal  : {m['carrier_skel']}")
        print("-" * 50)
        displayed += 1
        if displayed >= 15:
            break

if __name__ == "__main__":
    run_crib_analysis()
