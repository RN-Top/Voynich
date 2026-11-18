#!/usr/bin/env python3
"""
EXPERIMENTAL: Comprehensive Voynich Decryption Attempt v1
Testing abbreviation expansion + frequency analysis + ingredient validation
(Playing around - not for production)
"""

import json
from collections import Counter

# Load data
with open('voynich_integrated.json', 'r') as f:
    integrated = json.load(f)

# Medieval pharmaceutical abbreviations (expanded)
ABBREV = {
    # Common actions
    'dar': 'dare',  'da': 'dare', 'd': 'dis',
    'dis': 'distilla', 'disti': 'distilla', 'dist': 'distilla',
    'sol': 'solve', 'solv': 'solve',
    'coq': 'coquere', 'coqu': 'coquere',
    'misc': 'miscere',
    'ferv': 'fervere',
    'frac': 'frangere',
    'pul': 'pulvis', 'pulv': 'pulvis',
    'trit': 'tritum',

    # Substances
    'ol': 'oleum', 'aqua': 'aqua', 'aq': 'aqua',
    'vin': 'vinum', 'mel': 'mel', 'sal': 'sal',
    'herb': 'herba', 'rad': 'radix',
    'fol': 'folium', 'flor': 'flos', 'sem': 'semen',
    'cort': 'cortex', 'res': 'resina',

    # Measurements
    'gr': 'granum', 'dr': 'drachma', 'oz': 'oncia', 'lib': 'libra',

    # Quality/state
    'subt': 'subtilis', 'crass': 'crassus',
    'alb': 'albus', 'rub': 'rubeus', 'nig': 'niger',

    # Medical properties
    'diuret': 'diureticum', 'laxat': 'laxativum',
    'carmin': 'carminativum', 'stomat': 'stomaticum',

    # Specific ingredients
    'merc': 'mercurius', 'sulph': 'sulphur', 'vitri': 'vitriol',
}

# Collect all words
all_words = []
for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            all_words.extend(line.get('words', []))

print(f"Total words extracted: {len(all_words)}")
print(f"Unique words: {len(set(all_words))}")
print()

# Try abbreviation matching
print("=== ABBREVIATION MATCHING ===")
matched_abbrev = {}
unmatched_words = set()

for word in set(all_words):
    if word in ABBREV:
        matched_abbrev[word] = ABBREV[word]
    else:
        # Try prefix matching
        found = False
        for abbrev_key in sorted(ABBREV.keys(), key=len, reverse=True):
            if word.startswith(abbrev_key):
                matched_abbrev[word] = ABBREV[abbrev_key] + word[len(abbrev_key):]
                found = True
                break
        if not found:
            unmatched_words.add(word)

print(f"Matched to abbreviations: {len(matched_abbrev)}")
print(f"Unmatched: {len(unmatched_words)}")
print()

# Show top abbreviation matches
print("Top 20 Matched Abbreviations:")
abbrev_counts = Counter()
for word, expansion in matched_abbrev.items():
    count = all_words.count(word)
    abbrev_counts[expansion] += count

for expansion, count in abbrev_counts.most_common(20):
    print(f"  {expansion}: {count} instances")
print()

# Top unmatched words
print("Top 30 Unmatched Words (by frequency):")
unmatched_counts = Counter(w for w in all_words if w in unmatched_words)
for word, count in unmatched_counts.most_common(30):
    print(f"  {word}: {count}")
print()

# Pattern analysis on unmatched words
print("=== PATTERN ANALYSIS (Unmatched Words) ===")
ending_patterns = {}
for word in unmatched_words:
    # Check endings
    for end_len in [2, 3, 4]:
        ending = word[-end_len:] if len(word) >= end_len else word
        if ending not in ending_patterns:
            ending_patterns[ending] = []
        ending_patterns[ending].append(word)

print("Common endings in unmatched words:")
for ending in sorted(ending_patterns.keys(), key=lambda e: len(ending_patterns[e]), reverse=True)[:20]:
    words = ending_patterns[ending]
    count = sum(all_words.count(w) for w in words)
    print(f"  -{ending}: {len(words)} words, {count} total instances")
    print(f"    Examples: {', '.join(list(words)[:5])}")
print()

# Try to decode sample folios
print("=== SAMPLE DECRYPTION (First 3 folios with text) ===")
count = 0
for folio in integrated.get('folios', []):
    if folio.get('has_text') and count < 3:
        count += 1
        folio_id = folio.get('folio_id', 'unknown')
        print(f"\nFolio: {folio_id}")

        for line in folio.get('text_lines', [])[:3]:
            words = line.get('words', [])
            if not words:
                continue

            # Try to decode each word
            decoded = []
            for word in words:
                if word in matched_abbrev:
                    decoded.append(f"[{matched_abbrev[word]}]")
                else:
                    decoded.append(word)

            print(f"  Line: {' '.join(decoded[:15])}")
print()

print("=== KEY OBSERVATIONS ===")
print(f"1. Most frequent word: {unmatched_counts.most_common(1)[0] if unmatched_counts else 'N/A'}")
print(f"2. Words ending in -y: {sum(all_words.count(w) for w in unmatched_words if w.endswith('y'))}")
print(f"3. Words ending in -iin: {sum(all_words.count(w) for w in unmatched_words if w.endswith('iin'))}")
print(f"4. Words with 'ch' pattern: {sum(all_words.count(w) for w in unmatched_words if 'ch' in w)}")
print()

print("=== NEXT EXPERIMENTS ===")
print("[ ] Hypothesis: Most common unmatched words are base ingredients")
print("[ ] Hypothesis: -y endings indicate states/qualities")
print("[ ] Hypothesis: -iin endings indicate ingredient categories")
print("[ ] Hypothesis: @-codes mark measurement/batch boundaries")
print("[ ] Build frequency table for potential substitution cipher")
print("[ ] Cross-reference with known alchemical ingredient lists")
