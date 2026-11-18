#!/usr/bin/env python3
"""
ULTIMATE VOYNICH DECODER v1.0
Integrates: Frequency analysis + Abbreviation expansion + Bigram validation + Latin validation
Everything combined. This is it. Figure this shit out.
"""

import json
from collections import Counter
import re

print("=" * 80)
print("ULTIMATE VOYNICH DECODER v1.0")
print("=" * 80)
print()

# ============================================================================
# LOAD DATA
# ============================================================================
print("[1/6] Loading data...")
with open('voynich_integrated.json', 'r') as f:
    integrated = json.load(f)

# Extract all text
all_text = ""
all_chars = []
all_words = []

for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            text = line.get('text', '')
            all_text += text + "\n"
            all_words.extend(line.get('words', []))
            # Character frequency
            for char in text:
                if char.isalpha():
                    all_chars.append(char.lower())

print(f"   Total characters: {len(all_chars)}")
print(f"   Total words: {len(all_words)}")
print(f"   Total lines: {len([f for f in integrated.get('folios', []) if f.get('has_text')])}")
print()

# ============================================================================
# STAGE 1: ABBREVIATION DICTIONARY (Comprehensive)
# ============================================================================
print("[2/6] Building comprehensive abbreviation dictionary...")
ABBREV = {
    # Actions/Verbs
    'dar': 'dare', 'da': 'dare', 'd': 'dis',
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

    # Medical properties
    'diuret': 'diureticum', 'laxat': 'laxativum',
    'carmin': 'carminativum', 'stomat': 'stomaticum',

    # Specific ingredients
    'merc': 'mercurius', 'sulph': 'sulphur', 'vitri': 'vitriol',
}

# Try to expand words with abbreviations
abbrev_matches = {}
for word in set(all_words):
    for abbrev_key in sorted(ABBREV.keys(), key=len, reverse=True):
        if word.startswith(abbrev_key):
            abbrev_matches[word] = ABBREV[abbrev_key] + word[len(abbrev_key):]
            break

print(f"   Abbreviations matched: {len(abbrev_matches)}")
print()

# ============================================================================
# STAGE 2: CHARACTER FREQUENCY MAPPING (Enhanced)
# ============================================================================
print("[3/6] Building character frequency mapping...")

# Voynich frequencies
voynich_freq = Counter(all_chars)

# Known Latin letter frequencies (adjusted for pharmaceutical Latin)
# Medical/alchemical Latin has different frequencies than standard Latin
LATIN_FREQ_SORTED = [
    'e', 'a', 'r', 'i', 'o', 't',  # top 6
    'n', 's', 'h', 'd', 'l', 'c',  # next 6
    'u', 'm', 'g', 'f', 'p', 'b',  # next 6
    'v', 'k', 'x', 'w', 'y', 'z',  # bottom 6
]

# Build Voynich sorted by frequency
voynich_sorted = [char for char, count in voynich_freq.most_common()]

# Create mapping: Voynich char -> Latin char
cipher_map = {}
for i, voynich_char in enumerate(voynich_sorted):
    if i < len(LATIN_FREQ_SORTED):
        cipher_map[voynich_char] = LATIN_FREQ_SORTED[i]
    else:
        cipher_map[voynich_char] = voynich_char

print(f"   Character mapping created: {len(cipher_map)} characters")
print()

# ============================================================================
# STAGE 3: BIGRAM VALIDATION & REFINEMENT
# ============================================================================
print("[4/6] Analyzing bigrams for cipher refinement...")

# Known Latin bigrams (common in pharmaceutical/alchemical text)
KNOWN_LATIN_BIGRAMS = {
    'ch', 'ae', 'oe', 'ae', 're', 'er', 'ar', 'or', 'ir', 'us',
    'um', 'am', 'em', 'im', 'is', 'es', 'as', 'os', 'ia', 'io',
    'ium', 'ina', 'ina', 'orum', 'arum',
}

# Calculate bigrams in original text
voynich_bigrams = Counter()
for i in range(len(all_text) - 1):
    c1, c2 = all_text[i].lower(), all_text[i+1].lower()
    if c1.isalpha() and c2.isalpha():
        voynich_bigrams[(c1, c2)] += 1

# Decode bigrams using current mapping
decoded_bigrams = {}
for (c1, c2), count in voynich_bigrams.most_common(100):
    decoded = cipher_map.get(c1, '?') + cipher_map.get(c2, '?')
    if '?' not in decoded:
        decoded_bigrams[decoded] = count

# Count how many match known Latin bigrams
matching_latin = sum(count for bigram, count in decoded_bigrams.items()
                     if bigram in KNOWN_LATIN_BIGRAMS)
total_bigrams = sum(decoded_bigrams.values())

print(f"   Top 100 bigrams analyzed")
print(f"   Matching known Latin bigrams: {matching_latin}/{total_bigrams} ({100*matching_latin/total_bigrams:.1f}%)")
print()

# ============================================================================
# STAGE 4: KNOWN WORD MATCHING
# ============================================================================
print("[5/6] Testing against known pharmaceutical words...")

# Known Latin pharmaceutical words (partial list)
KNOWN_LATIN_WORDS = {
    'aqua', 'oleum', 'sal', 'herba', 'radix', 'folium', 'flos', 'semen',
    'cortex', 'resina', 'balsamum', 'unguentum', 'emplastrum', 'tinctura',
    'decoctum', 'infusio', 'extractum', 'pulvis', 'vinum', 'mel',
    'distilla', 'solve', 'coquere', 'miscere', 'frangere', 'tritum',
    'dare', 'recipe', 'fiat', 'fice', 'misce', 'coque', 'distille',
    'mercurius', 'sulphur', 'vitriol', 'alumen', 'arsenicum',
}

# Try to find known words in decoded text
known_word_matches = []
for word in KNOWN_LATIN_WORDS:
    if word in all_text.lower():
        known_word_matches.append(word)

print(f"   Known Latin words found directly: {len(known_word_matches)}")
if known_word_matches[:10]:
    print(f"   Examples: {', '.join(known_word_matches[:10])}")
print()

# ============================================================================
# STAGE 5: DECODE SAMPLE FOLIOS
# ============================================================================
print("[6/6] Decoding sample folios...")
print()

decoded_samples = []

for idx, folio in enumerate(integrated.get('folios', [])[:5]):  # First 5 folios with text
    if not folio.get('has_text'):
        continue

    folio_id = folio.get('folio_id', 'unknown')

    # Decode first 3 lines
    print(f"--- {folio_id} ---")

    for line_idx, line in enumerate(folio.get('text_lines', [])[:3]):
        text = line.get('text', '')
        words = line.get('words', [])

        # Remove markup
        clean_text = re.sub(r'[{<\]}\[\]!>@;:,.\-]', '', text)

        # Decode
        decoded_chars = []
        for char in clean_text:
            if char.isalpha():
                decoded_chars.append(cipher_map.get(char.lower(), '?'))
            elif char in ' \n':
                decoded_chars.append(char)
            else:
                decoded_chars.append(char)

        decoded_line = ''.join(decoded_chars)

        # Apply abbreviation expansion
        decoded_words = []
        for word in words:
            if word in abbrev_matches:
                decoded_words.append(f"[{abbrev_matches[word]}]")
            else:
                # Decode character by character
                decoded_word = ''.join([cipher_map.get(c.lower(), '?') for c in word])
                decoded_words.append(decoded_word)

        print(f"Original: {' '.join(words[:12])}")
        print(f"Decoded:  {' '.join(decoded_words[:12])}")
        print()

        decoded_samples.append({
            'folio': folio_id,
            'original': ' '.join(words),
            'decoded': ' '.join(decoded_words)
        })

# ============================================================================
# STAGE 6: ANALYSIS & SCORING
# ============================================================================
print("=" * 80)
print("ANALYSIS & SCORING")
print("=" * 80)
print()

# Score the decryption quality
print("Cipher Quality Indicators:")
print(f"  1. Character frequency mapping: {len(cipher_map)}/26 characters")
print(f"  2. Latin bigram matches: {100*matching_latin/total_bigrams:.1f}%")
print(f"  3. Known Latin words found: {len(known_word_matches)}")
print(f"  4. Abbreviation matches: {len(abbrev_matches)}/{{len(set(all_words))}}")
print()

print("Top decoded words (from first 20 folios):")
decoded_word_freq = Counter()
for folio in integrated.get('folios', [])[:20]:
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            for word in line.get('words', []):
                decoded_word = ''.join([cipher_map.get(c.lower(), '?') for c in word])
                if '?' not in decoded_word:
                    decoded_word_freq[decoded_word] += 1

print("  Top 15 decoded words:")
for word, count in decoded_word_freq.most_common(15):
    print(f"    {word:20} {count:5}")
print()

print("=" * 80)
print("NEXT STEPS")
print("=" * 80)
print()
print("[ ] Validate decoded words against pharmaceutical Latin dictionaries")
print("[ ] Refine cipher mapping using known pharmaceutical terminology")
print("[ ] Cross-reference @-codes with batch identifiers")
print("[ ] Extract complete recipes from multiple folios")
print("[ ] Have Juan validate ingredient patterns and abbreviations")
print()

print("Full sample decodings saved to decoded_samples.json")
with open('decoded_samples.json', 'w') as f:
    json.dump(decoded_samples, f, indent=2)

print()
print("DECODER COMPLETE")
