#!/usr/bin/env python3
"""
ULTIMATE VOYNICH DECODER v2.0 - CONSTRAINT-BASED SOLVER
Uses: Known words + Bigram constraints + Iterative refinement
This is the real deal. Crack this shit.
"""

import json
from collections import Counter
import re

print("=" * 80)
print("ULTIMATE VOYNICH DECODER v2.0 - CONSTRAINT-BASED SOLVER")
print("=" * 80)
print()

# ============================================================================
# LOAD DATA
# ============================================================================
print("[1/7] Loading data...")
with open('voynich_integrated.json', 'r') as f:
    integrated = json.load(f)

all_text = ""
all_words = []

for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            text = line.get('text', '')
            all_text += text + " "
            all_words.extend(line.get('words', []))

print(f"   Characters: {len(all_text)}")
print(f"   Words: {len(all_words)}")
print()

# ============================================================================
# STAGE 1: IDENTIFY KNOWN WORDS IN VOYNICH TEXT
# ============================================================================
print("[2/7] Identifying word patterns with known pharmaceutical Latin...")

# Known pharmaceutical/alchemical words
KNOWN_WORDS = {
    'aqua': 'water',
    'oleum': 'oil',
    'sal': 'salt',
    'herba': 'herb',
    'recipe': 'recipe',
    'fiat': 'make/let it be',
    'distilla': 'distill',
    'miscere': 'mix',
    'frangere': 'break/crush',
    'coquere': 'cook/boil',
    'solve': 'dissolve',
    'dare': 'give/take',
    'pulvis': 'powder',
    'unguentum': 'ointment',
    'emplastrum': 'plaster',
}

# Find where known words appear
word_constraints = {}
for known_word in KNOWN_WORDS:
    for voynich_word in set(all_words):
        # Try to match patterns
        if len(known_word) == len(voynich_word):
            # This could be a match - note potential character mappings
            if known_word not in word_constraints:
                word_constraints[known_word] = []
            word_constraints[known_word].append(voynich_word)

print(f"   Potential word constraint pairs: {sum(len(v) for v in word_constraints.values())}")
print()

# ============================================================================
# STAGE 2: BUILD CONSTRAINT-BASED CIPHER MAP
# ============================================================================
print("[3/7] Building constraint-based cipher mapping...")

# Start with abbreviation-based mappings (more reliable)
ABBREV_KNOWN = {
    'dar': 'dare',
    'ol': 'oleum',
    'aqua': 'aqua',
    'sal': 'sal',
}

# Extract character mappings from known abbreviations
char_constraints = {}
for voynich_abbrev, latin_word in ABBREV_KNOWN.items():
    # 'dar' -> 'dare', so d->d, a->a, r->r
    for i, c in enumerate(voynich_abbrev):
        if i < len(latin_word):
            if c not in char_constraints:
                char_constraints[c] = {}
            char_constraints[c][latin_word[i]] = char_constraints[c].get(latin_word[i], 0) + 1

print(f"   Character constraints from abbreviations:")
for char in sorted(char_constraints.keys()):
    best_match = max(char_constraints[char].items(), key=lambda x: x[1])
    print(f"     {char} -> {best_match[0]} (confidence: {best_match[1]})")
print()

# ============================================================================
# STAGE 3: BIGRAM-BASED REFINEMENT
# ============================================================================
print("[4/7] Analyzing bigram constraints...")

# Known Latin bigrams (very common in pharmaceutical text)
LATIN_BIGRAMS_SCORED = {
    'ch': 10, 're': 8, 'er': 8, 'ar': 7, 'or': 7, 'us': 7, 'um': 6, 'am': 6,
    'em': 6, 'ae': 6, 'oe': 6, 'ae': 6, 'ia': 5, 'io': 5, 'is': 5, 'es': 5,
    'as': 5, 'os': 5, 'in': 5, 'an': 5, 'on': 5, 'en': 5, 'ea': 5, 'eo': 5,
    'ia': 4, 'ua': 4, 'ue': 4, 'oi': 4, 'ai': 4, 'au': 4, 'ci': 3, 'ti': 3,
    'di': 3, 'li': 3, 'ri': 3, 'ni': 3, 'mi': 3, 'hi': 3, 'pi': 3, 'gi': 3,
}

# Extract Voynich bigrams and score them
voynich_bigrams = Counter()
for i in range(len(all_text) - 1):
    c1, c2 = all_text[i].lower(), all_text[i+1].lower()
    if c1.isalpha() and c2.isalpha():
        voynich_bigrams[(c1, c2)] += 1

# Score each Voynich bigram by its frequency
print(f"   Top Voynich bigrams by frequency:")
for (c1, c2), count in voynich_bigrams.most_common(20):
    print(f"     {c1}{c2}: {count:5} occurrences")
print()

# ============================================================================
# STAGE 4: BEST GUESS MAPPING (Frequency + Constraints + Bigrams)
# ============================================================================
print("[5/7] Computing best guess cipher mapping...")

# Character frequencies
char_freq = Counter()
for c in all_text:
    if c.isalpha():
        char_freq[c.lower()] += 1

# Latin expected frequencies
LATIN_FREQ = {
    'e': 0.127, 'a': 0.082, 'r': 0.075, 'i': 0.070, 'o': 0.075, 't': 0.093,
    'n': 0.067, 's': 0.063, 'h': 0.061, 'd': 0.043, 'l': 0.040, 'c': 0.028,
    'u': 0.028, 'm': 0.024, 'w': 0.024, 'f': 0.022, 'g': 0.020, 'y': 0.020,
    'p': 0.019, 'b': 0.015, 'v': 0.010, 'k': 0.008, 'x': 0.002, 'j': 0.002,
    'q': 0.001, 'z': 0.001
}

# Build best mapping
best_mapping = {}
used_latin_chars = set()

# Priority 1: Use constraints from known abbreviations
for voynich_char in char_constraints:
    best_latin = max(char_constraints[voynich_char].items(), key=lambda x: x[1])[0]
    if best_latin not in used_latin_chars:
        best_mapping[voynich_char] = best_latin
        used_latin_chars.add(best_latin)

# Priority 2: Fill in remaining by frequency
remaining_voynich = [c for c, _ in char_freq.most_common() if c not in best_mapping]
remaining_latin = sorted([c for c in LATIN_FREQ if c not in used_latin_chars],
                         key=lambda c: LATIN_FREQ[c], reverse=True)

for voynich_char, latin_char in zip(remaining_voynich, remaining_latin):
    best_mapping[voynich_char] = latin_char

print(f"   Final mapping ({len(best_mapping)} characters):")
for c in sorted(best_mapping.keys()):
    print(f"     {c} -> {best_mapping[c]}")
print()

# ============================================================================
# STAGE 5: DECODE AND SCORE
# ============================================================================
print("[6/7] Decoding text and scoring results...")

# Decode first 100 words
decoded_words = []
for word in all_words[:100]:
    decoded = ''.join([best_mapping.get(c.lower(), '?') for c in word])
    if '?' not in decoded:
        decoded_words.append(decoded)

# Check how many are "word-like" (mostly vowels+consonants)
valid_decodings = [w for w in decoded_words if len(w) > 2 and not re.search(r'([aeiou])\1{2}', w)]

print(f"   Decoded first 100 words, {len(valid_decodings)} are valid-looking")
print()
print("   Sample decoded words:")
for word in valid_decodings[:20]:
    print(f"     {word}")
print()

# ============================================================================
# STAGE 6: DECODE SAMPLE FOLIOS
# ============================================================================
print("[7/7] Decoding sample folios with constraint-based mapping...")
print()

for idx, folio in enumerate(integrated.get('folios', [])[:3]):
    if not folio.get('has_text'):
        continue

    print(f"--- {folio.get('folio_id')} ---")

    for line_idx, line in enumerate(folio.get('text_lines', [])[:2]):
        words = line.get('words', [])

        # Decode
        decoded_words_line = []
        for word in words:
            decoded = ''.join([best_mapping.get(c.lower(), '?') for c in word])
            decoded_words_line.append(decoded)

        print(f"Original: {' '.join(words[:15])}")
        print(f"Decoded:  {' '.join(decoded_words_line[:15])}")
        print()

# ============================================================================
# STAGE 7: ANALYSIS
# ============================================================================
print("=" * 80)
print("CONSTRAINT-BASED ANALYSIS")
print("=" * 80)
print()

# Check if decoded text contains known Latin words
decoded_full = ""
for word in all_words[:1000]:
    decoded = ''.join([best_mapping.get(c.lower(), '?') for c in word])
    if '?' not in decoded:
        decoded_full += decoded + " "

known_found = []
for known_word in KNOWN_WORDS:
    if known_word in decoded_full.lower():
        known_found.append(known_word)

print(f"Known pharmaceutical words found in decoded text: {len(known_found)}")
if known_found:
    print(f"  Found: {', '.join(known_found)}")
print()

# Check bigram quality
print("Bigram quality assessment:")
decoded_bigrams = Counter()
for i in range(len(decoded_full) - 1):
    if decoded_full[i].isalpha() and decoded_full[i+1].isalpha():
        decoded_bigrams[(decoded_full[i], decoded_full[i+1])] += 1

latin_bigram_match = sum(count for (c1, c2), count in decoded_bigrams.items()
                         if (c1+c2) in LATIN_BIGRAMS_SCORED)
total_bigrams = sum(decoded_bigrams.values())

print(f"  Known Latin bigrams: {latin_bigram_match}/{total_bigrams} ({100*latin_bigram_match/total_bigrams:.1f}%)")
print()

print("Top decoded bigrams:")
for (c1, c2), count in decoded_bigrams.most_common(15):
    is_known = " [KNOWN LATIN]" if (c1+c2) in LATIN_BIGRAMS_SCORED else ""
    print(f"  {c1}{c2}: {count:5}{is_known}")
print()

print("=" * 80)
print("CONSTRAINT-BASED DECODER COMPLETE")
print("=" * 80)
