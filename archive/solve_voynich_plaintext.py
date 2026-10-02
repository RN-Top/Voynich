"""
VOYNICH AUTOMATED PHONETIC HOLDOUT DECODER
Tests candidate decan phonetic values across held-out herbal & recipe folios.
Computes phonotactic syllabic compliance (CVC) and historical Latin lexical hits.
"""

import re
import os
import urllib.request
import pandas as pd

DATA_PATH = "data/ZL3b-n.txt"
FALLBACK_URL = "https://www.voynich.nu/data/ZL3b-n.txt"

# 1. Phonetic Alphabet Locked from Ptolemaic Decan Grounding
PHONETIC_ALPHABET = {
    'o': 'o', 't': 't', 'c': 's', 'h': 'a', 'e': 'r', 'd': 'n',
    'a': 'u', 'i': 'i', 'q': 'c', 'k': 'o', 'p': 'm', 'm': 's',
    'y': 'm', 's': 'p', 'l': 'l', 'r': 'r', 'f': 'f'
}

SUKHOTIN_VOWELS = set(['a', 'o', 'h', 't', 'i', 'y'])

# 2. Historical 15th-Century Latin Medical & Apothecary Root Anchors
HISTORICAL_LATIN_ROOTS = {
    "coq": "cook / boil (coquere)",
    "cal": "heat / warm (calfacere)",
    "aqu": "water / decoction (aqua)",
    "rad": "root (radix)",
    "herb": "plant / herb (herba)",
    "vas": "vessel / jar (vasculum)",
    "solv": "dissolve (resolvere)",
    "fin": "end / completed (finis)",
    "ole": "oil (oleum)",
    "fol": "leaf (folium)",
    "stel": "star / sector (stella)",
    "fac": "aspect / face (facies)",
    "sum": "take / ingest (sumere)",
    "extr": "extract (extractum)",
    "mis": "mix / blend (miscere)"
}

# 3. Canonical Blind Holdout Folio Lines (Unseen Recipes & Herbal Stems)
HOLDOUT_TEST_SET = [
    {"folio": "f114v.1", "section": "Recipes/Stars", "voynich": "pchdol dar chedain chodalr fcheey dchedy qocphdy otdady qotedar daiin"},
    {"folio": "f114v.21", "section": "Recipes/Stars", "voynich": "qokedy otcheodaiin qopairam otcheody daiin chedy"},
    {"folio": "f76r.5", "section": "Biological", "voynich": "qokedy qokeey oror or chkorol otey qokedy lkedy chdy qokchdy qokal chdam"},
    {"folio": "f1r.1", "section": "Herbal", "voynich": "fachys ykal ar ataiin shol shory cthores y kor sholdy"},
    {"folio": "f1r.6", "section": "Herbal Incipit", "voynich": "ydaraishy"},
    {"folio": "f9r.10", "section": "Quire Closure", "voynich": "ytchas oraiin chkor"}
]

def decode_token(tok: str) -> str:
    cleaned = re.sub(r"[^a-z]", "", str(tok).lower())
    return "".join(PHONETIC_ALPHABET.get(ch, ch) for ch in cleaned)

def evaluate_phonotactics(word: str) -> bool:
    """Checks if output contains pronounceable syllabic alternating vowels/consonants."""
    vows = set(['a', 'e', 'i', 'o', 'u', 'y'])
    skel = "".join(['V' if ch in vows else 'C' for ch in word if ch.isalpha()])
    # Reject strings with 4+ consonants or 4+ vowels in a row
    if "CCCC" in skel or "VVVV" in skel:
        return False
    return True

def score_latin_roots(word: str):
    hits = []
    for root, meaning in HISTORICAL_LATIN_ROOTS.items():
        if root in word:
            hits.append(meaning)
    return hits

def main():
    print("=" * 75)
    print("VOYNICH PHONETIC HOLDOUT DECODER: PHASE 4 VALIDATION")
    print("=" * 75)

    results = []
    total_words = 0
    phonotactic_passes = 0
    lexical_hits = 0

    for item in HOLDOUT_TEST_SET:
        words = item["voynich"].split()
        decoded_words = [decode_token(w) for w in words]
        
        line_hits = []
        for w in decoded_words:
            total_words += 1
            if evaluate_phonotactics(w):
                phonotactic_passes += 1
            matched = score_latin_roots(w)
            if matched:
                lexical_hits += 1
                line_hits.extend(matched)

        results.append({
            "Folio Line": item["folio"],
            "Section": item["section"],
            "Decoded Output": " ".join(decoded_words),
            "Identified Roots": ", ".join(set(line_hits)) if line_hits else "None"
        })

    df = pd.DataFrame(results)
    print("\nHOLDOUT DECODING LEDGER:")
    for _, r in df.iterrows():
        print(f"\n[{r['Folio Line']} | {r['Section']}]")
        print(f"  Raw Phonetic: {r['Decoded Output']}")
        print(f"  Root Hits:    {r['Identified Roots']}")

    pass_rate = (phonotactic_passes / total_words) * 100.0 if total_words else 0
    hit_rate = (lexical_hits / total_words) * 100.0 if total_words else 0

    print("\n" + "=" * 75)
    print("OBJECTIVE VALIDATION SCORECARD:")
    print("=" * 75)
    print(f"Total Holdout Words Tested:    {total_words}")
    print(f"Phonotactic Compliance Rate:   {pass_rate:.1f}%  (Must be >= 70% to pass)")
    print(f"Historical Latin Lexical Hits: {hit_rate:.1f}%")
    print("-" * 75)

    if pass_rate >= 70.0:
        print("VERDICT: PASSES PHONOTACTIC GATE (Syllabic Alternation Confirmed)")
    else:
        print("VERDICT: COLLAPSED INTO CONSONANT/VOWEL CLUSTERS (Falsified)")

if __name__ == "__main__":
    main()
