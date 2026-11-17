#!/usr/bin/env python3
"""
EXPERIMENTAL: Substitution Cipher Frequency Mapping
Hypothesis: Voynich is monoalphabetic substitution + pharmaceutical abbreviations
"""

import json
from collections import Counter
import string

# Load data
with open('voynich_integrated.json', 'r') as f:
    integrated = json.load(f)

# Collect characters
all_chars = []
for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            text = line.get('text', '')
            # Remove markup and special chars
            for char in text:
                if char.isalpha():
                    all_chars.append(char.lower())

# Voynich character frequency
voynich_freq = Counter(all_chars)
total_voynich = sum(voynich_freq.values())

# Expected English frequency (what Latin/pharmaceutical shorthand would likely be)
ENGLISH_FREQ = {
    'e': 0.127, 'a': 0.082, 'r': 0.075, 'i': 0.070, 'o': 0.075, 't': 0.093,
    'n': 0.067, 's': 0.063, 'h': 0.061, 'd': 0.043, 'l': 0.040, 'c': 0.028,
    'u': 0.028, 'm': 0.024, 'w': 0.024, 'f': 0.022, 'g': 0.020, 'y': 0.020,
    'p': 0.019, 'b': 0.015, 'v': 0.010, 'k': 0.008, 'x': 0.002, 'j': 0.002,
    'q': 0.001, 'z': 0.001
}

print("=== CHARACTER FREQUENCY ANALYSIS ===")
print("Voynich characters (top 15):")
voynich_chars = []
for char, count in voynich_freq.most_common(15):
    pct = count / total_voynich
    expected = ENGLISH_FREQ.get(char, 0)
    print(f"  {char}: {count:6} ({pct:5.1%}) | Expected in English: {expected:5.1%}")
    voynich_chars.append(char)

print()

# Build a frequency-based mapping (most common Voynich char -> most common English char)
print("=== FREQUENCY-BASED CIPHER MAPPING ===")
english_sorted = sorted(ENGLISH_FREQ.items(), key=lambda x: x[1], reverse=True)
voynich_sorted = voynich_freq.most_common()

# Create mapping
cipher_map = {}
for i, (voynich_char, v_count) in enumerate(voynich_sorted[:26]):
    if i < len(english_sorted):
        english_char, e_freq = english_sorted[i]
        cipher_map[voynich_char] = english_char

print("Voynich -> English mapping (by frequency):")
for voynich_char in sorted(cipher_map.keys(), key=lambda c: cipher_map[c]):
    english_char = cipher_map[voynich_char]
    v_count = voynich_freq[voynich_char]
    print(f"  {voynich_char} ({v_count:5}) -> {english_char} ({ENGLISH_FREQ.get(english_char, 0):5.1%})")

print()

# Test decryption on sample words
print("=== SAMPLE DECRYPTIONS ===")
sample_words = ['daiin', 'ol', 'chedy', 'shedy', 'qokeey', 'dar', 'chol', 'ar', 'aiin', 'shey']

for word in sample_words:
    decoded = ''.join([cipher_map.get(c, '?') for c in word])
    print(f"  {word:15} -> {decoded}")

print()

# Decode a full sample text
print("=== FULL SAMPLE DECRYPTION (First 3 lines of f1r) ===")
sample_lines = []
for folio in integrated.get('folios', []):
    if folio.get('folio_id') == 'f1r' and folio.get('has_text'):
        for line in folio.get('text_lines', [])[:3]:
            text = line.get('text', '')
            sample_lines.append(text)
        break

for text in sample_lines:
    # Remove markup
    import re
    clean_text = re.sub(r'[{<\]}\[\]!>@;:,.]', '', text)

    # Decode each character
    decoded = ''
    for char in clean_text:
        if char.isalpha():
            decoded += cipher_map.get(char.lower(), char)
        else:
            decoded += char

    print(f"Original: {text[:70]}")
    print(f"Decoded:  {decoded[:70]}")
    print()

# Bigram analysis
print("=== BIGRAM ANALYSIS (Character level) ===")
char_bigrams = Counter()
for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            text = line.get('text', '')
            for i in range(len(text) - 1):
                if text[i].isalpha() and text[i+1].isalpha():
                    pair = (text[i].lower(), text[i+1].lower())
                    char_bigrams[pair] += 1

print("Top 20 character bigrams in Voynich:")
for (c1, c2), count in char_bigrams.most_common(20):
    decoded = cipher_map.get(c1, c1) + cipher_map.get(c2, c2)
    print(f"  {c1}{c2}: {count:5} -> {decoded}")

print()
print("=== OBSERVATIONS ===")
print("- 'ch' bigram is very common (expected in Latin/alchemical text)")
print("- 'o' and 'e' frequencies are off from English (might be Latin/abbreviations)")
print("- Mapping shows partial structure but not readable Latin yet")
print("- Next: Need to refine mapping with known Latin/pharmaceutical words")
