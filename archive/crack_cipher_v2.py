#!/usr/bin/env python3
"""
IMPROVED CIPHER CRACKING
Use frequency analysis + bigram constraints + hill climbing

The naive frequency mapping didn't work perfectly because:
1. Character mappings conflict at bigram level
2. Latin has constraint patterns (certain bigrams forbidden/common)
3. Need to solve iteratively using constraints

Approach:
1. Start with frequency-based initial mapping
2. Test against known Latin bigrams
3. Use hill climbing to swap characters for better score
4. Try known medical/Latin vocabulary
"""

import json
from collections import Counter
import random

print("=" * 80)
print("IMPROVED CIPHER CRACKING: CONSTRAINT SATISFACTION")
print("=" * 80)

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

# Extract EVA text
all_words = []
for folio in integrated['folios'][:50]:
    for line in folio.get('text_lines', []):
        if 'words' in line:
            all_words.extend(line['words'])

eva_text = ''.join(all_words)
eva_chars = list(eva_text)

print(f"\nWorking with: {len(all_words)} words, {len(eva_chars)} characters")

# ============================================================================
# PHASE 1: BUILD INITIAL MAPPING (frequency-based)
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 1: FREQUENCY-BASED INITIAL MAPPING")
print("=" * 80)

eva_freq = Counter(eva_chars)
expected_freq = {
    'e': 0.127, 'a': 0.082, 'r': 0.075, 'i': 0.070, 'o': 0.075, 't': 0.093,
    'n': 0.067, 's': 0.063, 'h': 0.061, 'd': 0.043, 'c': 0.028, 'u': 0.028,
    'l': 0.040, 'm': 0.024, 'g': 0.020, 'p': 0.019, 'b': 0.015, 'f': 0.013,
    'v': 0.010, 'w': 0.012, 'k': 0.008, 'x': 0.002, 'y': 0.020, 'z': 0.001
}

eva_sorted = sorted(eva_freq.items(), key=lambda x: x[1], reverse=True)
expected_sorted = sorted(expected_freq.items(), key=lambda x: x[1], reverse=True)

mapping = {}
reverse_mapping = {}
for i in range(min(len(eva_sorted), len(expected_sorted))):
    eva_char = eva_sorted[i][0]
    expected_char = expected_sorted[i][0]
    mapping[eva_char] = expected_char
    reverse_mapping[expected_char] = eva_char

print(f"Initial mapping built: {len(mapping)} character pairs")
print(f"Top 5 mappings:")
for eva, expected in list(mapping.items())[:5]:
    print(f"  {eva} → {expected}")

# ============================================================================
# PHASE 2: LATIN BIGRAM CONSTRAINTS
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 2: LATIN BIGRAM CONSTRAINT ANALYSIS")
print("=" * 80)

# Common Latin bigrams
common_latin_bigrams = [
    'ch', 'ae', 'qu', 'th', 'ae', 'us', 'em', 'in', 'is', 'es', 'ut', 'et',
    'que', 'ium', 'ion', 'ant', 'ent', 'ous', 'ity', 'ive'
]

# Extract EVA bigrams
eva_bigrams = []
for word in all_words:
    for i in range(len(word)-1):
        eva_bigrams.append(word[i:i+2])

eva_bigram_freq = Counter(eva_bigrams)

print(f"\nMost common EVA bigrams:")
for bigram, count in eva_bigram_freq.most_common(20):
    decoded = ''.join(mapping.get(c, '?') for c in bigram)
    print(f"  {bigram} ({count:4d}) → {decoded}")

# Score current mapping by how many EVA bigrams decode to valid Latin bigrams
def score_mapping(mapping, eva_bigram_freq, common_latin_bigrams):
    """Score how well the mapping produces common Latin bigrams"""
    score = 0
    for eva_bigram, count in eva_bigram_freq.most_common(100):
        decoded = ''.join(mapping.get(c, '?') for c in eva_bigram)
        if decoded in common_latin_bigrams or (len(decoded) == 2 and all(c in 'aeioulnrst' for c in decoded)):
            score += count
    return score

initial_score = score_mapping(mapping, eva_bigram_freq, common_latin_bigrams)
print(f"\nInitial mapping score: {initial_score}")

# ============================================================================
# PHASE 3: HILL CLIMBING OPTIMIZATION
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 3: HILL CLIMBING OPTIMIZATION")
print("=" * 80)

best_mapping = mapping.copy()
best_score = initial_score
iterations = 0
improvements = 0

print(f"\nStarting hill climb (max 1000 iterations)...")

for iteration in range(1000):
    iterations += 1

    # Try swapping two character mappings
    all_eva_chars = list(best_mapping.keys())
    if len(all_eva_chars) < 2:
        break

    # Random swap
    char1, char2 = random.sample(all_eva_chars, 2)

    # Create new mapping with swap
    test_mapping = best_mapping.copy()
    test_mapping[char1], test_mapping[char2] = test_mapping[char2], test_mapping[char1]

    # Score it
    test_score = score_mapping(test_mapping, eva_bigram_freq, common_latin_bigrams)

    # Accept if better
    if test_score > best_score:
        best_mapping = test_mapping
        best_score = test_score
        improvements += 1

        if improvements % 10 == 0:
            print(f"  Improvement {improvements}: score={best_score} (iteration {iteration})")

    if iteration % 100 == 0 and iteration > 0:
        print(f"  Iteration {iteration}: best score = {best_score}")

print(f"\n✓ Hill climb complete")
print(f"  Total iterations: {iterations}")
print(f"  Improvements found: {improvements}")
print(f"  Final score: {best_score} (initial: {initial_score})")
print(f"  Improvement: +{best_score - initial_score} ({100*(best_score-initial_score)/initial_score:.1f}%)")

# ============================================================================
# PHASE 4: DECODE WITH OPTIMIZED MAPPING
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 4: DECODE WITH OPTIMIZED MAPPING")
print("=" * 80)

# Full decode
decoded_text = ''.join(best_mapping.get(c, '?') for c in eva_text)

print(f"\nDecoded sample (first 300 chars):")
print(decoded_text[:300])

print(f"\n\nDecoded words (first 100):")
decoded_words = []
for word in all_words[:100]:
    decoded_word = ''.join(best_mapping.get(c, '?') for c in word)
    decoded_words.append(decoded_word)

print(' '.join(decoded_words))

# ============================================================================
# PHASE 5: ANALYZE DECODED TEXT
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 5: ANALYSIS OF DECODED TEXT")
print("=" * 80)

# Check for real Latin/English words
common_latin_words = {
    'aqua', 'herba', 'medicina', 'cura', 'dolor', 'febris', 'morbus',
    'remedium', 'sanguis', 'corpus', 'anima', 'vis', 'virtus', 'potentia',
    'homo', 'rex', 'deus', 'vita', 'mors', 'tempus', 'locus', 'modus',
    'via', 'modo', 'talis', 'qualis', 'dum', 'cum', 'sed', 'nam', 'enim',
    'est', 'sunt', 'erat', 'erant', 'est', 'esse', 'fuit', 'sum', 'sumus'
}

found_words = []
for word in decoded_words:
    if word.lower() in common_latin_words:
        found_words.append(word)

print(f"\nCommon Latin words found in decoded text:")
if found_words:
    for word in found_words[:20]:
        print(f"  - {word}")
else:
    print(f"  (none found in sample)")

# ============================================================================
# PHASE 6: BIGRAM ANALYSIS OF DECODED
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 6: BIGRAM ANALYSIS OF DECODED TEXT")
print("=" * 80)

decoded_bigrams = []
for word in decoded_words:
    for i in range(len(word)-1):
        decoded_bigrams.append(word[i:i+2])

decoded_bigram_freq = Counter(decoded_bigrams)

print(f"\nMost common bigrams in decoded text:")
for bigram, count in decoded_bigram_freq.most_common(20):
    print(f"  {bigram:5s}: {count:3d}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("HILL CLIMBING SUMMARY")
print("=" * 80)

print(f"""
METHOD: Frequency-based initial mapping + hill climbing optimization

PROCESS:
  1. Built frequency-based initial mapping
  2. Scored against known Latin bigrams
  3. Hill climbed for 1000 iterations
  4. Found {improvements} improvements to mapping score

RESULTS:
  Initial score: {initial_score}
  Final score: {best_score}
  Improvement: +{best_score - initial_score} ({100*(best_score-initial_score)/initial_score:.1f}%)

DECODED TEXT SAMPLE:
  {decoded_text[:100]}...

LATIN WORDS FOUND: {len(found_words)}
  {', '.join(found_words[:10]) if found_words else '(none in sample)'}

COMMON DECODED BIGRAMS:
  {', '.join(f"{bg}({decoded_bigram_freq[bg]})" for bg in list(decoded_bigram_freq.keys())[:5])}

NEXT STEP:
  - Refine with known plaintext matching
  - Try different initial seeds
  - Use constraint solver for entire alphabet
  - Cross-validate against medical Latin vocabulary
""")

print("=" * 80)

# Save the best mapping
print(f"\nBest mapping found:")
print(json.dumps(best_mapping, indent=2)[:500])
