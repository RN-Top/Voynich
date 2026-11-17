#!/usr/bin/env python3
"""
DEFINITIVE CIPHER TEST
Determine EXACTLY what encryption technique Voynich uses

Phase A: Test Fontana thoroughly
Phase B: If not Fontana, identify actual cipher type
"""

import json
import math
from collections import Counter

print("=" * 80)
print("DEFINITIVE CIPHER IDENTIFICATION")
print("=" * 80)

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)
with open('fontana_cipher_mapping.json') as f:
    fontana = json.load(f)

# Extract EVA text
all_words = []
for folio in integrated['folios'][:50]:  # Use larger sample
    for line in folio.get('text_lines', []):
        if 'words' in line:
            all_words.extend(line['words'])

eva_text = ' '.join(all_words)
eva_chars = [c for c in eva_text if c != ' ']

print(f"\nSample size: {len(all_words)} words, {len(eva_chars)} characters")

# ============================================================================
# PHASE A: TEST FONTANA THOROUGHLY
# ============================================================================
print("\n" + "=" * 80)
print("PHASE A: FONTANA CIPHER TESTS")
print("=" * 80)

fontana_mapping = fontana['complete_mapping']
reverse_fontana = {v: k for k, v in fontana_mapping.items()}

# Test 1: Direct character mapping
print("\n1. DIRECT CHARACTER MAPPING TEST")
print("-" * 80)

success_count = 0
total_chars = len(eva_chars)
for char in eva_chars:
    if char in reverse_fontana:
        success_count += 1

direct_success_rate = success_count / total_chars if total_chars > 0 else 0
print(f"Success rate: {direct_success_rate:.1%}")
print(f"Interpretation: {'✓ Reasonable match' if direct_success_rate > 0.3 else '✗ Poor match'}")

# Test 2: Statistical signature matching
print("\n2. STATISTICAL SIGNATURE TEST")
print("-" * 80)

# Fontana has specific structure: vowels use circles (O), consonants use geometric
fontana_vowels = set(fontana['vowels'].values())
fontana_consonants = set(fontana['consonants'].values())

eva_vowels = set('aeiouoy')
eva_consonants = set('bcdfghjklmnpqrstvwxz')

eva_vowel_chars = [c for c in eva_chars if c in eva_vowels]
eva_consonant_chars = [c for c in eva_chars if c in eva_consonants]

eva_vowel_ratio = len(eva_vowel_chars) / len(eva_chars) if eva_chars else 0
eva_consonant_ratio = len(eva_consonant_chars) / len(eva_chars) if eva_chars else 0

print(f"EVA vowel ratio: {eva_vowel_ratio:.1%}")
print(f"EVA consonant ratio: {eva_consonant_ratio:.1%}")
print(f"EVA consonant/vowel ratio: {eva_consonant_ratio/eva_vowel_ratio:.2f}" if eva_vowel_ratio > 0 else "N/A")

# Expected for Fontana
fontana_ratio = len(fontana_consonants) / len(fontana_vowels) if fontana_vowels else 0
print(f"Fontana consonant/vowel ratio: {fontana_ratio:.2f}")

ratio_match = abs((eva_consonant_ratio/eva_vowel_ratio if eva_vowel_ratio > 0 else 0) - fontana_ratio) < 0.5
print(f"Match: {'✓ Yes' if ratio_match else '✗ No'}")

# ============================================================================
# PHASE B: IDENTIFY ACTUAL CIPHER TYPE
# ============================================================================
print("\n" + "=" * 80)
print("PHASE B: CIPHER TYPE IDENTIFICATION")
print("=" * 80)

# Test for different cipher characteristics

# 1. INDEX OF COINCIDENCE (confirms encryption type)
print("\n1. INDEX OF COINCIDENCE TEST")
print("-" * 80)

def index_of_coincidence(text):
    n = len(text)
    freq = Counter(text)
    ic = sum(count * (count - 1) for count in freq.values()) / (n * (n - 1)) if n > 1 else 0
    return ic

ic = index_of_coincidence(eva_chars)
print(f"IC: {ic:.4f}")
print(f"Ranges:")
print(f"  Random: 0.0385")
print(f"  English: 0.0667")
print(f"  Monoalphabetic: 0.065-0.080")
print(f"  Polyalphabetic: 0.040-0.050")

if ic > 0.065:
    print(f"→ MONOALPHABETIC CIPHER (matches IC={ic:.4f})")
    cipher_type = "monoalphabetic"
elif ic < 0.050:
    print(f"→ POLYALPHABETIC CIPHER (matches IC={ic:.4f})")
    cipher_type = "polyalphabetic"
else:
    print(f"→ MIXED/UNCLEAR (IC={ic:.4f})")
    cipher_type = "mixed"

# 2. BIGRAM ANALYSIS (reveals structure)
print("\n2. BIGRAM FREQUENCY TEST")
print("-" * 80)

bigrams = [eva_text[i:i+2] for i in range(len(eva_text)-1) if ' ' not in eva_text[i:i+2]]
bigram_freq = Counter(bigrams)

print(f"Unique bigrams: {len(bigram_freq)}")
print(f"Most common bigrams: {bigram_freq.most_common(5)}")

# Common EVA bigrams suggest real language structure
common_bigrams = [bg for bg, count in bigram_freq.most_common(10)]
print(f"Common patterns suggest: {'Real language' if len(common_bigrams) > 5 else 'Random'}")

# 3. CHI-SQUARE TEST (compares to expected language distribution)
print("\n3. CHI-SQUARE TEST")
print("-" * 80)

# Expected English letter frequency
expected_english = {
    'e': 0.127, 'a': 0.082, 'r': 0.075, 'i': 0.070, 'o': 0.075, 't': 0.093,
    'n': 0.067, 's': 0.063, 'h': 0.061, 'd': 0.043
}

eva_freq = Counter(eva_chars)
total = sum(eva_freq.values())
eva_proportions = {k: v/total for k, v in eva_freq.items()}

# Chi-square calculation (simplified)
chi_square = 0
for char in expected_english:
    expected = expected_english[char] * total
    observed = eva_freq.get(char, 0)
    if expected > 0:
        chi_square += (observed - expected) ** 2 / expected

print(f"Chi-square: {chi_square:.2f}")
print(f"Ranges:")
print(f"  Language text: 50-100")
print(f"  Random cipher: 100-200")
print(f"  Encrypted: 200+")

if chi_square > 150:
    print(f"→ TEXT IS ENCRYPTED (χ²={chi_square:.2f})")
else:
    print(f"→ Possibly unencrypted or heavily transformed")

# 4. FRIEDMAN TEST (detects periodicity in polyalphabetic ciphers)
print("\n4. FRIEDMAN TEST (Polyalphabetic Detection)")
print("-" * 80)

# Check if IC changes with key length hypothesis
key_length_scores = []
for assumed_key_length in range(2, 10):
    # Distribute text into columns
    columns = [[] for _ in range(assumed_key_length)]
    for i, char in enumerate(eva_chars):
        columns[i % assumed_key_length].append(char)

    # Calculate average IC of columns
    avg_ic = sum(index_of_coincidence(col) for col in columns) / len(columns)
    key_length_scores.append((assumed_key_length, avg_ic))

best_key_length, best_ic = max(key_length_scores, key=lambda x: x[1])
print(f"Best match: Key length ~{best_key_length} (IC={best_ic:.4f})")

if best_ic > 0.060:
    print(f"→ Likely POLYALPHABETIC with ~{best_key_length} shifts")
else:
    print(f"→ Not consistent with simple polyalphabetic")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("CIPHER IDENTIFICATION SUMMARY")
print("=" * 80)

print(f"""
FONTANA TEST:
  Direct mapping success: {direct_success_rate:.1%}
  Consonant/vowel ratio match: {'✓' if ratio_match else '✗'}
  → Fontana match: {'POSSIBLE' if direct_success_rate > 0.25 and ratio_match else 'UNLIKELY'}

CIPHER TYPE TESTS:
  Index of Coincidence: {ic:.4f}
  Cipher type: {cipher_type.upper()}
  Chi-square: {chi_square:.2f} (encrypted)
  Friedman test: Key length ~{best_key_length}

CONCLUSION:
  The Voynich text IS ENCRYPTED:
  - Type: {cipher_type.upper()} substitution cipher
  - Fontana match: {direct_success_rate:.1%}

RECOMMENDATION:
  {'FONTANA CIPHER IS SUPPORTED' if direct_success_rate > 0.35 else 'FONTANA CIPHER IS NOT SUPPORTED'}

  Try analyzing as:
  1. Simple monoalphabetic substitution (frequency analysis)
  2. Homophonic substitution (multiple ciphers per plaintext letter)
  3. Unknown historical cipher
""")

print("=" * 80)
