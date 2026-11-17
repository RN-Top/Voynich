#!/usr/bin/env python3
"""
EXPERIMENTAL: Frequency Analysis + Ingredient Validation
Testing: Can we build a substitution cipher key from word patterns?
"""

import json
from collections import Counter

# Load data
with open('voynich_integrated.json', 'r') as f:
    integrated = json.load(f)

# Collect all words with context
all_words = []
word_bigrams = []
word_lines = []

for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            words = line.get('words', [])
            if words:
                all_words.extend(words)
                word_lines.append(words)
                # Build bigrams
                for i in range(len(words) - 1):
                    word_bigrams.append((words[i], words[i+1]))

print(f"Total words: {len(all_words)}")
print(f"Unique words: {len(set(all_words))}")
print(f"Total lines: {len(word_lines)}")
print()

# === FREQUENCY ANALYSIS ===
print("=== FREQUENCY ANALYSIS ===")
word_freq = Counter(all_words)

# Analyze character frequencies
char_freq = Counter()
for word in all_words:
    for char in word:
        char_freq[char] += 1

print("Top 15 Characters by frequency:")
for char, count in char_freq.most_common(15):
    pct = 100 * count / sum(char_freq.values())
    print(f"  {char}: {count} ({pct:.1f}%)")
print()

# Expected Latin letter frequencies (for comparison)
LATIN_FREQ = {
    'e': 11.1, 'a': 8.2, 'r': 7.5, 'i': 6.9, 'o': 6.9, 't': 5.6,
    'n': 5.6, 's': 4.3, 'h': 3.1, 'd': 3.0, 'l': 2.8, 'c': 2.8,
    'u': 2.8, 'm': 2.4, 'g': 2.0, 'f': 1.8, 'b': 1.5, 'p': 1.5,
}

print("Character frequency comparison (Voynich vs Latin):")
total_chars = sum(char_freq.values())
for char in sorted(char_freq.keys(), key=lambda c: char_freq[c], reverse=True)[:10]:
    voynich_pct = 100 * char_freq[char] / total_chars
    latin_pct = LATIN_FREQ.get(char, 0)
    print(f"  {char}: Voynich {voynich_pct:.1f}%, Latin avg {latin_pct:.1f}%")
print()

# === BIGRAM ANALYSIS ===
print("=== BIGRAM ANALYSIS ===")
bigram_freq = Counter(word_bigrams)

print("Top 20 word bigrams:")
for (w1, w2), count in bigram_freq.most_common(20):
    print(f"  {w1} -> {w2}: {count}")
print()

# === STARTING CHARACTERS ===
print("=== STARTING CHARACTER PATTERNS ===")
start_chars = Counter(w[0] for w in all_words)
print("Top 15 starting characters:")
for char, count in start_chars.most_common(15):
    pct = 100 * count / len(all_words)
    print(f"  {char}: {count} words ({pct:.1f}%)")
print()

# === ENDING PATTERNS ===
print("=== ENDING PATTERNS ===")
# Words ending in -y
y_words = [w for w in all_words if w.endswith('y')]
print(f"Words ending in -y: {len(set(y_words))} unique, {len(y_words)} total")
print(f"  Hypothesis: Quality/state markers")

# Words ending in -iin
iin_words = [w for w in all_words if w.endswith('iin')]
print(f"Words ending in -iin: {len(set(iin_words))} unique, {len(iin_words)} total")
print(f"  Hypothesis: Ingredient categories")

# Words ending in -dy
dy_words = [w for w in all_words if w.endswith('dy')]
print(f"Words ending in -dy: {len(set(dy_words))} unique, {len(dy_words)} total")
print(f"  Hypothesis: Medical/alchemical actions")

# Words containing 'ch'
ch_words = [w for w in all_words if 'ch' in w]
print(f"Words containing 'ch': {len(set(ch_words))} unique, {len(ch_words)} total")
print(f"  Hypothesis: Chemistry/change actions (from medieval Latin)")
print()

# === KNOWN INGREDIENT HYPOTHESIS ===
print("=== INGREDIENT COMBINATION HYPOTHESIS ===")
# Most common unmatched words - could these be base ingredients?
top_unmatched = word_freq.most_common(50)
print("Top 20 most frequent words (potential ingredient bases):")
for i, (word, count) in enumerate(top_unmatched[:20], 1):
    # Simple heuristic: how "ingredient-like" is this word?
    has_ingredient_ending = word.endswith(('iin', 'ain', 'in', 'ol', 'ar', 'al', 'or'))
    print(f"  {i:2}. {word:20} {count:5} {'[ingredient-like]' if has_ingredient_ending else ''}")
print()

# === LINE STRUCTURE ANALYSIS ===
print("=== LINE STRUCTURE ANALYSIS ===")
line_lengths = [len(line) for line in word_lines]
line_len_dist = Counter(line_lengths)

print("Words per line distribution:")
for length in sorted(line_len_dist.keys())[:20]:
    count = line_len_dist[length]
    pct = 100 * count / len(word_lines)
    print(f"  {length:2} words: {count:5} lines ({pct:5.1f}%)")

print(f"\nAverage line length: {sum(line_lengths) / len(line_lengths):.1f} words")
print("Hypothesis: 5-10 word lines = standardized recipe format")
print()

# === RECIPE STRUCTURE PATTERN ===
print("=== RECIPE STRUCTURE PATTERNS ===")
# Are certain words more common at line start/end?
start_words = Counter(line[0] if line else None for line in word_lines)
end_words = Counter(line[-1] if line else None for line in word_lines)

print("Top words at line START:")
for word, count in start_words.most_common(10):
    if word:
        print(f"  {word}: {count}")

print("\nTop words at line END:")
for word, count in end_words.most_common(10):
    if word:
        print(f"  {word}: {count}")
print()

print("=== EXPERIMENTS COMPLETED ===")
print("[ ] Next: Test decryption with letter frequency mapping")
print("[ ] Next: Cross-reference ingredient words with historical texts")
print("[ ] Next: Analyze @-code positions in ingredient patterns")
