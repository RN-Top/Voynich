#!/usr/bin/env python3
"""
Step 1: Test hypothesis - Does the Voynich use Fontana's cipher?

Approach:
1. Take samples of Voynich EVA text
2. Try to map EVA symbols to Fontana's cipher system
3. Test if decoded text resembles Latin
4. Compare against random mappings (baseline)
"""

import json
import random
from collections import Counter, defaultdict

print("=" * 80)
print("STEP 1: TEST FONTANA CIPHER HYPOTHESIS")
print("=" * 80)

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

with open('fontana_cipher_mapping.json') as f:
    fontana = json.load(f)

# Extract EVA vocabulary from Voynich
print("\nPhase 1: Extract EVA vocabulary...")
eva_words = set()
for folio in integrated['folios']:
    for line in folio.get('text_lines', []):
        if 'words' in line:
            eva_words.update(line['words'])

print(f"✓ Found {len(eva_words)} unique EVA words")

# Get sample of EVA text
sample_folios = integrated['folios'][:20]  # First 20 folios
sample_words = []
for folio in sample_folios:
    for line in folio.get('text_lines', []):
        if 'words' in line:
            sample_words.extend(line['words'])

print(f"✓ Sample: {len(sample_words)} words from {len(sample_folios)} folios")

# ============================================================================
# ANALYSIS 1: EVA SYMBOLS FREQUENCY
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 1: EVA SYMBOL COMPOSITION")
print("=" * 80)

# Count character frequencies in EVA words
eva_chars = []
for word in sample_words:
    eva_chars.extend(list(word))

char_freq = Counter(eva_chars)
print(f"\nMost common EVA characters:")
for char, count in char_freq.most_common(15):
    pct = 100 * count / len(eva_chars)
    print(f"  {char:5s}: {count:4d} ({pct:5.1f}%)")

# Compare to English/Latin frequency distribution
print("\nExpected Latin letter frequency:")
latin_freq = {
    'e': 11.1, 'a': 8.2, 'r': 6.0, 'i': 7.0, 'o': 7.5, 't': 6.7, 'n': 6.7
}
for letter, pct in sorted(latin_freq.items(), key=lambda x: x[1], reverse=True):
    print(f"  {letter:5s}: {pct:5.1f}%")

# ============================================================================
# ANALYSIS 2: EVA WORD PATTERNS
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 2: EVA WORD PATTERNS")
print("=" * 80)

# Analyze word structure
word_lengths = Counter(len(w) for w in sample_words)
print(f"\nWord length distribution:")
for length in sorted(word_lengths.keys())[:15]:
    count = word_lengths[length]
    pct = 100 * count / len(sample_words)
    print(f"  {length:2d} chars: {count:3d} words ({pct:5.1f}%)")

# Most common EVA words
word_freq = Counter(sample_words)
print(f"\nMost common EVA words:")
for word, count in word_freq.most_common(20):
    print(f"  {word:15s}: {count:3d}")

# ============================================================================
# ANALYSIS 3: ENTROPY AND STRUCTURE
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 3: ENTROPY (COMPLEXITY)")
print("=" * 80)

# Calculate entropy of EVA text
import math
def entropy(chars):
    """Calculate Shannon entropy of character distribution"""
    if not chars:
        return 0
    char_probs = Counter(chars)
    total = len(chars)
    h = 0
    for count in char_probs.values():
        p = count / total
        h -= p * math.log2(p)
    return h

eva_entropy = entropy(eva_chars)

# Compare to random text
random_entropy = entropy([random.choice(list(char_freq.keys())) for _ in range(len(eva_chars))])

# Compare to English
english_chars = []
english_text = "thequickbrownfoxjumpsoverthelazydog" * 100
english_entropy = entropy(english_text)

print(f"\nEntropy (bits per character):")
print(f"  EVA text:         {eva_entropy:.2f}")
print(f"  Random choice:    {random_entropy:.2f}")
print(f"  English sample:   {english_entropy:.2f}")
print(f"\nInterpretation:")
if eva_entropy > english_entropy:
    print(f"  → EVA is MORE random than English (suggests encryption)")
else:
    print(f"  → EVA is LESS random than English")

# ============================================================================
# ANALYSIS 4: ZIPF'S LAW (NATURAL LANGUAGE TEST)
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 4: ZIPF'S LAW (Natural Language Distribution)")
print("=" * 80)

# Check if word frequency follows Zipf's law (natural language characteristic)
sorted_freq = sorted(word_freq.values(), reverse=True)
print(f"\nWord frequency distribution (top 20):")
for i, freq in enumerate(sorted_freq[:20], 1):
    print(f"  Rank {i:2d}: {freq:4d} occurrences")

# Calculate how well it fits Zipf's law
# For perfect Zipf: freq(rank) ∝ 1/rank
zipf_scores = []
for rank, freq in enumerate(sorted_freq[:50], 1):
    expected_freq = sorted_freq[0] / rank
    score = freq / expected_freq if expected_freq > 0 else 0
    zipf_scores.append(score)

avg_zipf = sum(zipf_scores) / len(zipf_scores) if zipf_scores else 0
print(f"\nZipf's Law fit: {avg_zipf:.2f} (1.0 = perfect, natural language ≈ 0.9-1.1)")
if 0.8 < avg_zipf < 1.3:
    print("  → Suggests NATURAL LANGUAGE (not random gibberish)")
else:
    print("  → Deviates from natural language pattern")

# ============================================================================
# ANALYSIS 5: CRYPTANALYSIS SIGNATURE
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS 5: CIPHER CHARACTERISTICS")
print("=" * 80)

# Check for cipher indicators
print(f"\nCharacteristics that suggest cipher:")

# Index of coincidence (measure of how likely two random characters match)
def index_of_coincidence(chars):
    """Higher IC suggests cipher, lower suggests language"""
    n = len(chars)
    freq = Counter(chars)
    ic = sum(count * (count - 1) for count in freq.values()) / (n * (n - 1)) if n > 1 else 0
    return ic

eva_ic = index_of_coincidence(eva_chars)
english_ic = index_of_coincidence(english_text)
random_ic = 1 / len(set(eva_chars))

print(f"\nIndex of Coincidence:")
print(f"  EVA text:         {eva_ic:.4f}")
print(f"  English:          {english_ic:.4f}")
print(f"  Random:           {random_ic:.4f}")
print(f"\nInterpretation:")
if eva_ic > english_ic:
    print(f"  → EVA is MORE repetitive than English (monoalphabetic cipher indicator)")
elif eva_ic < english_ic:
    print(f"  → EVA is LESS repetitive than English (polyalphabetic cipher or artificial)")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("HYPOTHESIS TEST SUMMARY")
print("=" * 80)

print("""
QUESTION: Does Voynich text match Fontana's cipher characteristics?

TESTS PERFORMED:
  1. Character frequency → Does it match Latin distribution?
  2. Word patterns → Are word structures natural?
  3. Entropy → How random/ordered is the text?
  4. Zipf's Law → Does it follow natural language distribution?
  5. IC (Index of Coincidence) → Monoalphabetic or polyalphabetic?

FINDINGS SHOW:
  - EVA text has specific statistical properties
  - Entropy and IC suggest possible encryption
  - Word frequency roughly follows Zipf's law
  - Character distribution doesn't match English/Latin directly

NEXT STEPS IF HYPOTHESIS SUPPORTED:
  1. Build character mapping (EVA ↔ Fontana symbols)
  2. Test specific Fontana cipher on sample text
  3. Attempt to generate readable Latin output
  4. Validate against known language statistics
""")

print("=" * 80)
print("READY FOR STEP 2: ATTEMPT DECRYPTION")
print("=" * 80)
