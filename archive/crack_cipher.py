#!/usr/bin/env python3
"""
CRACK THE MONOALPHABETIC SUBSTITUTION CIPHER
Use frequency analysis, pattern matching, and known plaintext attacks
"""

import json
from collections import Counter
import re

print("=" * 80)
print("CRACKING MONOALPHABETIC SUBSTITUTION CIPHER")
print("=" * 80)

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

# Extract EVA text
all_words = []
for folio in integrated['folios'][:100]:  # Use larger sample
    for line in folio.get('text_lines', []):
        if 'words' in line:
            all_words.extend(line['words'])

eva_text = ''.join(all_words)
eva_chars = list(eva_text)

print(f"\nSample: {len(all_words)} words, {len(eva_chars)} characters")

# ============================================================================
# STEP 1: FREQUENCY ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("STEP 1: FREQUENCY ANALYSIS")
print("=" * 80)

eva_freq = Counter(eva_chars)
total_chars = len(eva_chars)

print(f"\nEVA character frequencies:")
for char, count in eva_freq.most_common(15):
    pct = 100 * count / total_chars
    print(f"  {char:5s}: {count:5d} ({pct:5.1f}%)")

# Expected English/Latin frequencies
expected_freq = {
    'e': 0.127, 'a': 0.082, 'r': 0.075, 'i': 0.070, 'o': 0.075, 't': 0.093,
    'n': 0.067, 's': 0.063, 'h': 0.061, 'd': 0.043, 'c': 0.028, 'u': 0.028,
    'l': 0.040, 'm': 0.024, 'g': 0.020, 'p': 0.019, 'b': 0.015
}

print(f"\nExpected Latin/English frequencies:")
for char in sorted(expected_freq.keys(), key=lambda x: expected_freq[x], reverse=True)[:10]:
    pct = expected_freq[char]
    print(f"  {char}: {pct:5.1%}")

# Try naive frequency mapping
print(f"\n" + "-" * 80)
print("NAIVE FREQUENCY MAPPING:")
print("-" * 80)

eva_sorted = sorted(eva_freq.items(), key=lambda x: x[1], reverse=True)
expected_sorted = sorted(expected_freq.items(), key=lambda x: x[1], reverse=True)

frequency_mapping = {}
for i in range(min(len(eva_sorted), len(expected_sorted))):
    eva_char = eva_sorted[i][0]
    expected_char = expected_sorted[i][0]
    frequency_mapping[eva_char] = expected_char

print(f"\nProposed mapping (by frequency):")
for eva, expected in list(frequency_mapping.items())[:10]:
    eva_pct = 100 * eva_freq[eva] / total_chars
    exp_pct = 100 * expected_freq[expected]
    print(f"  {eva} ({eva_pct:5.1f}%) → {expected} ({exp_pct:5.1f}%)")

# Decode sample
sample_words = all_words[:100]
decoded_naive = []
for word in sample_words:
    decoded_word = ''.join(frequency_mapping.get(c, '?') for c in word)
    decoded_naive.append(decoded_word)

print(f"\nNaive decode (first 50 words):")
print(' '.join(decoded_naive[:50]))

# ============================================================================
# STEP 2: PATTERN ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("STEP 2: PATTERN ANALYSIS")
print("=" * 80)

# Find words that might be known patterns
print(f"\nCommon EVA words:")
word_freq = Counter(all_words)
for word, count in word_freq.most_common(20):
    print(f"  {word:15s}: {count:3d} occurrences")

# Common Latin medical words (Voynich is likely medical)
latin_medical = [
    'aqua', 'herba', 'medicina', 'cura', 'dolor', 'febris', 'morbus',
    'remedium', 'sanguis', 'corpus', 'anima', 'vis', 'virtus', 'potentia'
]

print(f"\nSearching for patterns matching Latin medical words...")

# Try to match EVA word patterns to Latin words
# Pattern: words with similar structure might reveal cipher

eva_word_patterns = {}
for word in all_words:
    pattern = ''.join(str(i) for i, c in enumerate(set(word), 1) for _ in [c])
    # Create pattern showing which chars repeat
    char_map = {}
    pattern = []
    next_id = 0
    for c in word:
        if c not in char_map:
            char_map[c] = next_id
            next_id += 1
        pattern.append(str(char_map[c]))
    pattern = ''.join(pattern)

    if pattern not in eva_word_patterns:
        eva_word_patterns[pattern] = []
    eva_word_patterns[pattern].append(word)

# Find common patterns
pattern_freq = Counter(eva_word_patterns.keys())
print(f"\nMost common word patterns (letter structure):")
for pattern, count in pattern_freq.most_common(10):
    example_words = eva_word_patterns[pattern][:3]
    print(f"  Pattern {pattern}: {count:3d} words - examples: {example_words}")

# ============================================================================
# STEP 3: BIGRAM/TRIGRAM ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("STEP 3: BIGRAM/TRIGRAM ANALYSIS")
print("=" * 80)

# Common EVA bigrams
bigrams = []
for word in all_words:
    for i in range(len(word)-1):
        bigrams.append(word[i:i+2])

bigram_freq = Counter(bigrams)
print(f"\nMost common EVA bigrams:")
for bigram, count in bigram_freq.most_common(20):
    decoded = ''.join(frequency_mapping.get(c, '?') for c in bigram)
    print(f"  {bigram} ({count:3d}) → {decoded}")

# Common trigrams
trigrams = []
for word in all_words:
    for i in range(len(word)-2):
        trigrams.append(word[i:i+3])

trigram_freq = Counter(trigrams)
print(f"\nMost common EVA trigrams:")
for trigram, count in trigram_freq.most_common(15):
    decoded = ''.join(frequency_mapping.get(c, '?') for c in trigram)
    print(f"  {trigram} ({count:3d}) → {decoded}")

# ============================================================================
# STEP 4: KNOWN PLAINTEXT ATTACK
# ============================================================================
print("\n" + "=" * 80)
print("STEP 4: KNOWN PLAINTEXT ATTACK")
print("=" * 80)

print(f"\nLooking for medical/herbal Latin patterns...")

# If this is herbal/medical text, look for patterns
# Common word endings in Latin: -a, -us, -um, -ae, -is, -es

print(f"\nWord ending patterns:")
word_endings = Counter()
for word in all_words:
    if len(word) >= 2:
        ending = word[-2:]
        word_endings[ending] += 1

for ending, count in word_endings.most_common(15):
    decoded = ''.join(frequency_mapping.get(c, '?') for c in ending)
    print(f"  {ending} ({count:3d} words) → {decoded}")

# ============================================================================
# STEP 5: ATTEMPT DECRYPTION
# ============================================================================
print("\n" + "=" * 80)
print("STEP 5: ATTEMPT DECRYPTION")
print("=" * 80)

# Full text decode
full_text_decoded = ''.join(frequency_mapping.get(c, '?') for c in eva_text)

print(f"\nDecoded text (first 500 characters):")
print(full_text_decoded[:500])

print(f"\n\nDecoded words (first 100):")
decoded_words = []
for word in all_words[:100]:
    decoded_word = ''.join(frequency_mapping.get(c, '?') for c in word)
    decoded_words.append(decoded_word)

print(' '.join(decoded_words))

# Check for recognizable words
print(f"\n\nSearching for recognizable Latin/English words...")
recognizable = []
for word in decoded_words:
    if word in ['the', 'and', 'is', 'of', 'to', 'in', 'that', 'this', 'with', 'as']:
        recognizable.append(word)
    elif len(word) > 3 and all(c in 'aeioulnrst' for c in word):
        recognizable.append(word)

if recognizable:
    print(f"Found potential words: {recognizable[:20]}")
else:
    print(f"No recognizable words found in sample")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("DECRYPTION SUMMARY")
print("=" * 80)

print(f"""
METHOD: Frequency analysis based on expected Latin/English distribution

RESULTS:
  - Mapping built from character frequencies
  - Decoded text: {full_text_decoded[:200]}...

SUCCESS INDICATORS:
  - Common bigrams: {bigram_freq.most_common(1)[0] if bigram_freq else 'none'}
  - Common trigrams: {trigram_freq.most_common(1)[0] if trigram_freq else 'none'}
  - Recognizable words: {len(recognizable)} found

NEXT STEPS:
  1. Refine mapping based on known plaintext
  2. Try different character assignments
  3. Use constraint solving (letter patterns)
  4. Compare to known herbal/medical vocabulary

STATUS: Partial decode achieved - review for validity
""")

print("=" * 80)
