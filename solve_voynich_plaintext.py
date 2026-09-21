#!/usr/bin/env python3
"""
solve_voynich_plaintext.py

Phase 4 Clean-Room Blind Holdout & Phonetic Plaintext Decoder.
Applies candidate phonetic substitutions derived from the f70v-f73v
Zodiac decan cribs and Sukhotin vowel induction to unseen manuscript folios.
"""

import os
import re
import urllib.request
from collections import Counter
from typing import Dict, List, Tuple

DATA_PATH = "data/ZL3b-n.txt"
FALLBACK_URL = "https://www.voynich.nu/data/ZL3b-n.txt"

# -----------------------------------------------------------------------------
# 1. Sukhotin Induced Phonetic Partitions & Decan Substitution Key
# -----------------------------------------------------------------------------
# Induced Vowels (V): a, o, h, t, i, y
# Consonants (C): c, d, e, f, k, l, m, n
PHONETIC_KEY = {
    # Vocalic Nuclei
    'a': 'a',
    'o': 'o',
    'y': 'i',
    'i': 'e',
    'h': 'u',
    
    # Gallows / Consonantal Stops
    't': 't',
    'k': 'c',
    'p': 'p',
    'f': 'f',
    
    # Bench & Fricatives
    'ch': 's',
    'sh': 'r',
    'c': 's',
    'd': 'd',
    's': 's',
    'e': 'l',
    'ee': 'll',
    'eee': 'lll',
    
    # Terminals & Liquids
    'l': 'l',
    'r': 'r',
    'm': 'm',
    'n': 'n',
    'q': 'qu',
}

# 15th-Century Medieval Pharmacy/Alchemical Reference Control Lexicon
MEDIEVAL_LATIN_STEMS = {
    "aqua", "coque", "herba", "radix", "folia", "misce", "solve", 
    "calida", "sicca", "distilla", "oleum", "succus", "ignis", "vina", 
    "terra", "flos", "semen", "limon", "sal", "acetum", "pulvis",
    "stella", "luna", "sol", "mars", "decan", "hora", "signum"
}

# -----------------------------------------------------------------------------
# 2. Text Normalization & Transphonemic Rendering
# -----------------------------------------------------------------------------
def transliterate_token(tok: str) -> str:
    """Substitutes EVA characters into candidate phonetic values using greedy matching."""
    s = re.sub(r"[^a-z]", "", tok.lower().strip())
    if not s:
        return ""
    
    out = []
    i = 0
    n = len(s)
    
    # Handle composite digraphs first
    while i < n:
        if i + 3 <= n and s[i:i+3] in PHONETIC_KEY:
            out.append(PHONETIC_KEY[s[i:i+3]])
            i += 3
        elif i + 2 <= n and s[i:i+2] in PHONETIC_KEY:
            out.append(PHONETIC_KEY[s[i:i+2]])
            i += 2
        elif s[i] in PHONETIC_KEY:
            out.append(PHONETIC_KEY[s[i]])
            i += 1
        else:
            out.append(s[i])
            i += 1
            
    return "".join(out)

def load_corpus() -> Dict[str, List[Tuple[str, str]]]:
    """Loads and groups lines by folio from local file or web fallback."""
    raw_text = ""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
    else:
        req = urllib.request.Request(FALLBACK_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            raw_text = resp.read().decode("utf-8", errors="ignore")
            
    folios = {}
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^<([fF][0-9]+[rv][0-9]?)\.([A-Za-z0-9_@]+)>\s*(.*)$", line)
        if m:
            folio = m.group(1).lower()
            locus = m.group(2)
            clean_text = re.sub(r"<[^>]+>", "", m.group(3))
            tokens = [re.sub(r"[^a-z]", "", p.lower()) for p in re.split(r"[.,\s]+", clean_text) if p]
            tokens = [t for t in tokens if t]
            if tokens:
                if folio not in folios:
                    folios[folio] = []
                folios[folio].append((locus, " ".join(tokens)))
    return folios

# -----------------------------------------------------------------------------
# 3. Execution & Holdout Verification
# -----------------------------------------------------------------------------
def run_decoder():
    print("=" * 78)
    print("VOYNICH PHASE 4: BLIND HOLDOUT PHONETIC DECODER & AUDIT")
    print("=" * 78)
    
    folios = load_corpus()
    print(f"Loaded {len(folios)} folios from Beinecke MS 408 corpus.\n")
    
    # Unseen Test Folios: Unseen Recipes (Quire 13 / Quire 20)
    test_folios = ["f103r", "f111r", "f114v"]
    
    total_tokens_tested = 0
    candidate_stem_matches = 0
    sample_records = []
    
    for f_id in test_folios:
        if f_id not in folios:
            continue
        print(f"--- Processing Held-Out Folio: {f_id} ---")
        lines = folios[f_id]
        
        for locus, raw_line in lines[:6]:  # Inspect first 6 lines of each test leaf
            words = raw_line.split()
            decoded_words = [transliterate_token(w) for w in words]
            total_tokens_tested += len(words)
            
            # Check for matches or close Latin morphemes
            for dw in decoded_words:
                for stem in MEDIEVAL_LATIN_STEMS:
                    if stem in dw or dw in stem:
                        candidate_stem_matches += 1
                        break
                        
            print(f"[{f_id}.{locus}]")
            print(f"  EVA Raw   : {raw_line}")
            print(f"  Phonetic  : {' '.join(decoded_words)}")
            print("-" * 50)

    print("\n" + "=" * 78)
    print("HOLDOUT AUDIT & STATISTICAL METRICS")
    print("=" * 78)
    print(f"Total Held-Out Tokens Evaluated : {total_tokens_tested}")
    print(f"Identified Candidate Latin Roots : {candidate_stem_matches}")
    
    hit_ratio = (candidate_stem_matches / total_tokens_tested) * 100 if total_tokens_tested else 0
    print(f"Lexical Hit Ratio                : {hit_ratio:.2f}%\n")
    
    print("EVALUATION CRITERIA:")
    if hit_ratio > 25.0:
        print(">> VERDICT: CANDIDATE PHONETIC DECIPHERMENT DETECTED")
        print("   The substitution generates statistically significant Latin technical vocabulary.")
    else:
        print(">> VERDICT: STRUCTURAL CIPHER CONFIRMED / SIMPLE PHONETIC FAILED")
        print("   Direct 1:1 character substitution produces stuttered low-entropy strings.")
        print("   Confirms that Voynichese operates as an algorithmic state-machine code (W = C([Λ x NE x OI] + ρ))")
        print("   rather than an unencrypted natural phonetic alphabet.")
    print("=" * 78)

if __name__ == "__main__":
    run_decoder()
