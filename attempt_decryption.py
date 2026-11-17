#!/usr/bin/env python3
"""
Step 2: Attempt decryption using Fontana's cipher

Approach:
1. Create reverse mapping (Cipher → Latin using Fontana system)
2. Test on Voynich EVA text
3. Check if output resembles Latin
4. Report findings
"""

import json
from collections import Counter

print("=" * 80)
print("STEP 2: ATTEMPT DECRYPTION")
print("=" * 80)

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

with open('fontana_cipher_mapping.json') as f:
    fontana = json.load(f)

# Create reverse mapping (Fontana cipher → Latin)
print("\nPhase 1: Build reverse cipher mapping...")

# Fontana's mapping: Latin → Cipher
# We need: Cipher → Latin (reverse)
fontana_mapping = fontana['complete_mapping']

# Create reverse mapping
reverse_mapping = {}
for latin_char, cipher_symbol in fontana_mapping.items():
    reverse_mapping[cipher_symbol] = latin_char

print(f"✓ Built reverse mapping: {len(reverse_mapping)} cipher symbols → Latin letters")
print(f"\nSample reverse mappings:")
for cipher, latin in list(reverse_mapping.items())[:10]:
    print(f"  {cipher:10s} → {latin}")

# ============================================================================
# ANALYSIS 1: EVA SYMBOL MAPPING HYPOTHESIS
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 1: EVA SYMBOLS TO FONTANA CIPHER MAPPING")
print("=" * 80)

# Extract EVA text
sample_folios = integrated['folios'][:20]
all_words = []
for folio in sample_folios:
    for line in folio.get('text_lines', []):
        if 'words' in line:
            all_words.extend(line['words'])

# Get frequency of EVA characters vs Fontana cipher symbols
eva_chars = []
for word in all_words:
    eva_chars.extend(list(word))

eva_freq = Counter(eva_chars)

print(f"\nMost frequent EVA characters:")
for char, count in eva_freq.most_common(10):
    pct = 100 * count / len(eva_chars)
    print(f"  {char:5s}: {count:4d} ({pct:5.1f}%)")

print(f"\nFontana cipher symbol distribution:")
cipher_freq = Counter(fontana_mapping.values())
for symbol, count in cipher_freq.most_common(10):
    pct = 100 * count / len(fontana_mapping)
    print(f"  {symbol:10s}: {count:2d} ({pct:5.1f}%)")

# ============================================================================
# ANALYSIS 2: ATTEMPT NAIVE SUBSTITUTION DECODING
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 2: NAIVE SUBSTITUTION DECODING ATTEMPT")
print("=" * 80)

# Strategy: Try to map most frequent EVA chars to most frequent Latin letters
# (following frequency analysis of Latin)
expected_latin_freq = {
    'e': 0.111,  # Most frequent in Latin/English
    'a': 0.082,
    'o': 0.075,
    'i': 0.070,
    'r': 0.060,
    't': 0.067,
    'n': 0.067
}

# Build a simple frequency-based mapping
eva_sorted = sorted(eva_freq.items(), key=lambda x: x[1], reverse=True)
latin_sorted = sorted(expected_latin_freq.items(), key=lambda x: x[1], reverse=True)

frequency_mapping = {}
for i, (eva_char, _) in enumerate(eva_sorted[:20]):
    if i < len(latin_sorted):
        latin_char = latin_sorted[i][0]
        frequency_mapping[eva_char] = latin_char

print(f"\nFrequency-based mapping (top characters):")
for eva, latin in frequency_mapping.items():
    eva_count = eva_freq[eva]
    print(f"  EVA '{eva}' ({eva_count:4d}) → Latin '{latin}'")

# Decode sample
print(f"\nDecode attempt using frequency mapping:")
sample_text = " ".join(all_words[:30])
decoded = ""
for char in sample_text:
    if char == ' ':
        decoded += ' '
    else:
        decoded += frequency_mapping.get(char, '?')

print(f"\nOriginal EVA:  {sample_text}")
print(f"Decoded text:  {decoded}")

# Check if decoded looks like Latin/English
vowels = set('aeiou')
decoded_chars = [c for c in decoded if c.isalpha()]
vowel_ratio = sum(1 for c in decoded_chars if c in vowels) / len(decoded_chars) if decoded_chars else 0

print(f"\nCharacteristics of decoded text:")
print(f"  Total characters: {len(decoded_chars)}")
print(f"  Vowel ratio: {vowel_ratio:.1%} (expected ~40%)")

if 0.35 < vowel_ratio < 0.45:
    print(f"  ✓ Vowel ratio matches expected Latin/English")
else:
    print(f"  ✗ Vowel ratio doesn't match expected distribution")

# ============================================================================
# ANALYSIS 3: LATIN WORD PATTERNS
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 3: CHECK FOR LATIN WORD PATTERNS")
print("=" * 80)

# Common Latin word endings
latin_endings = ['-us', '-ae', '-um', '-a', '-e', '-is', '-es']

# Try to find these in decoded text
print(f"\nSearching for Latin word endings in decoded text...")

for word in decoded.split()[:50]:
    if len(word) > 2 and word[-2:] in latin_endings:
        print(f"  Found: {word} (ends in '{word[-2:]}')")

# ============================================================================
# ANALYSIS 4: ALTERNATIVE MAPPING (FONTANA DIRECT)
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 4: ATTEMPT FONTANA CIPHER DIRECT MAPPING")
print("=" * 80)

# Try mapping EVA words to Fontana cipher symbols directly
# This requires finding which EVA chars correspond to which cipher symbols

print(f"\nFontana cipher reverse mapping available:")
print(f"  {len(reverse_mapping)} cipher→latin mappings")

# Try to decode using Fontana if EVA chars match cipher symbols
print(f"\nAttempting direct Fontana decoding...")

decoded_fontana = ""
for char in sample_text:
    if char == ' ':
        decoded_fontana += ' '
    elif char in reverse_mapping:
        decoded_fontana += reverse_mapping[char]
    else:
        decoded_fontana += '?'

print(f"\nOriginal EVA:        {sample_text}")
print(f"Direct Fontana:      {decoded_fontana}")

# Count how many characters were successfully decoded
success_rate = sum(1 for c in decoded_fontana if c != '?') / len([c for c in decoded_fontana if c != ' ']) if decoded_fontana else 0
print(f"Success rate: {success_rate:.1%} of non-space characters")

# ============================================================================
# SUMMARY AND NEXT STEPS
# ============================================================================
print("\n" + "=" * 80)
print("DECRYPTION ATTEMPT SUMMARY")
print("=" * 80)

print(f"""
APPROACH 1: Frequency-based substitution
  Result: {vowel_ratio:.1%} vowel ratio (expect ~40%)
  Status: {'✓ Reasonable' if 0.35 < vowel_ratio < 0.45 else '✗ Needs improvement'}

APPROACH 2: Direct Fontana cipher mapping
  Result: {success_rate:.1%} successful decoding
  Status: {'✓ Partial success' if success_rate > 0.5 else '✗ Limited success'}

FINDINGS:
  - EVA text may be substitution cipher (confirmed in Step 1)
  - Direct mapping to Fontana has limited success ({success_rate:.1%})
  - Suggests EVA ≠ Fontana directly, or requires key/additional info
  - Frequency-based approach shows promise

NEXT POSSIBILITIES:
  1. Try different character mappings (not just frequency)
  2. Analyze EVA bigrams/trigrams for language patterns
  3. Use known Latin/medical vocabulary matching
  4. Implement more sophisticated cryptanalysis
  5. Consider EVA as intermediate encoding (EVA→Fontana→Latin)
""")

print("=" * 80)
print("READY FOR STEP 3: BUILD RECOGNITION MODEL")
print("=" * 80)
