#!/usr/bin/env python3
"""
SMART DECODER - Using experimental insights
Anchor on "sal" (most robust find) + use pharmaceutical recipe patterns
"""

import json
from collections import Counter
import random
import math

print("=" * 80)
print("SMART DECODER - ANCHORED TO KNOWN WORDS")
print("=" * 80)
print()

with open('voynich_integrated.json') as f:
    integrated = json.load(f)

all_text = ""
all_words = []
for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            text = line.get('text', '')
            all_text += text + " "
            all_words.extend(line.get('words', []))

clean_text = "".join(c.lower() for c in all_text if c.isalpha() or c.isspace())

print("Step 1: Find where 'sal' appears in Voynich text")
print("=" * 80)
print()

# "sal" = s, a, l (3 characters)
# We KNOW these map: s->s, a->a, l->l
# So in the Voynich text, we need to find a 3-character pattern that:
# 1. Appears frequently
# 2. Ends in common letters
# 3. Makes sense as a word

KNOWN_MAPPINGS = {
    's': 's',
    'a': 'a',
    'l': 'l',
}

KNOWN_LATIN = {
    'sal', 'fiat', 'aqua', 'oleum', 'dare', 'recipe', 'miscere',
    'distilla', 'solve', 'coquere', 'herba', 'radix', 'flos', 'fice',
    'pulvis', 'unguentum', 'emplastrum', 'tinctura', 'decoctum',
    'infusio', 'extractum', 'balsamum', 'resina', 'cortex',
    'vin', 'mel', 'acid', 'basis', 'misce', 'coque', 'distille',
    'decoct', 'infund', 'extract', 'spirit', 'essentia',
}

LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
}

print(f"Locking in known mappings: {KNOWN_MAPPINGS}")
print()

# Find most common 3-letter patterns in Voynich
three_letter_patterns = Counter()
for word in all_words:
    if len(word) == 3:
        word_lower = word.lower()
        three_letter_patterns[word_lower] += 1

print("Top 20 three-letter patterns in Voynich (candidates for 'sal'):")
for pattern, count in three_letter_patterns.most_common(20):
    print(f"  {pattern}: {count}")

print()
print("Step 2: Build mapping with anchors + aggressive known-word optimization")
print("=" * 80)
print()

def score_mapping(cipher_map, bonus_weight=200):
    score = 0

    # Bigram scoring
    for i in range(len(clean_text) - 1):
        c1, c2 = clean_text[i], clean_text[i+1]
        if c1 in cipher_map and c2 in cipher_map:
            bigram = cipher_map[c1] + cipher_map[c2]
            if bigram in LATIN_BIGRAMS:
                score += LATIN_BIGRAMS[bigram]
            elif cipher_map[c1] == cipher_map[c2]:
                score -= 2

    # Heavy bonus for known words
    decoded = "".join(cipher_map.get(c, '?') for c in clean_text)
    for word in KNOWN_LATIN:
        if word in decoded:
            score += bonus_weight
            # Bonus bonus if it's pharmaceutical key words
            if word in ['sal', 'aqua', 'oleum', 'miscere', 'distilla']:
                score += bonus_weight // 2

    return score

voynich_chars = sorted(set(c for c in clean_text if c.isalpha()))
latin_chars = list('abcdefghijklmnopqrstuvwxyz')

# Remove known from pool
for known_latin in KNOWN_MAPPINGS.values():
    if known_latin in latin_chars:
        latin_chars.remove(known_latin)

# Initialize with known mappings
mapping = KNOWN_MAPPINGS.copy()

# Fill rest with frequency-based guess
remaining_voynich = [c for c in voynich_chars if c not in mapping]
for v_char in remaining_voynich:
    if latin_chars:
        mapping[v_char] = latin_chars.pop(0)
    else:
        mapping[v_char] = 'x'

print(f"Initial mapping score: {score_mapping(mapping)}")

# AGGRESSIVE optimization: 10,000 swaps with high temperature
print("Running 10,000 aggressive optimization swaps...")
best_mapping = mapping.copy()
best_score = score_mapping(best_mapping)

temp = 100.0
for iteration in range(10000):
    swappable = [c for c in voynich_chars if c not in KNOWN_MAPPINGS]

    if len(swappable) >= 2:
        c1, c2 = random.sample(swappable, 2)
        mapping[c1], mapping[c2] = mapping[c2], mapping[c1]
        new_score = score_mapping(mapping)

        delta = new_score - best_score
        if delta > 0 or (temp > 0 and random.random() < math.exp(delta / temp)):
            best_score = new_score
            best_mapping = mapping.copy()
        else:
            mapping[c1], mapping[c2] = mapping[c2], mapping[c1]

    temp *= 0.9995

    if iteration % 1000 == 0:
        print(f"  Iteration {iteration}: Best score = {best_score}")

mapping = best_mapping

print()
print("Step 3: READ THE MANUSCRIPT WITH OPTIMIZED MAPPING")
print("=" * 80)
print()

# Decode all folios
decoded_full = "".join(mapping.get(c, '?') for c in clean_text)
found_words = [w for w in KNOWN_LATIN if w in decoded_full]

print(f"Known Latin words found: {len(found_words)}")
print(f"Words: {', '.join(sorted(found_words))}")
print()

# Show first 10 folios with decoding
for idx, folio in enumerate(integrated.get('folios', [])):
    if not folio.get('has_text') or idx > 9:
        continue

    folio_id = folio.get('folio_id', 'unknown')
    print(f"\n╔═══════════════════════════════════════════════════╗")
    print(f"║ {folio_id:50} ║")
    print(f"╚═══════════════════════════════════════════════════╝\n")

    for line_idx, line in enumerate(folio.get('text_lines', [])[:5]):
        words = line.get('words', [])
        if not words:
            continue

        decoded_words = []
        for word in words:
            decoded = ''.join([mapping.get(c.lower(), '?') for c in word])
            decoded_words.append(decoded)

        # Check for known words in this line
        line_decoded = ' '.join(decoded_words)
        line_found = [w for w in KNOWN_LATIN if w in line_decoded.lower()]

        print(f"Original: {' '.join(words[:10])}")
        print(f"Decoded:  {' '.join(decoded_words[:10])}")

        if line_found:
            print(f"  → FOUND: {', '.join(line_found)}")
        print()

print()
print("=" * 80)
print("ANALYSIS")
print("=" * 80)
print()

# Bigram quality
bigrams = Counter()
for i in range(len(decoded_full) - 1):
    if decoded_full[i].isalpha() and decoded_full[i+1].isalpha():
        bigrams[(decoded_full[i], decoded_full[i+1])] += 1

print("Top bigrams (should be mostly Latin):")
for (c1, c2), count in bigrams.most_common(20):
    bg = c1 + c2
    is_latin = " [LATIN]" if bg in LATIN_BIGRAMS else ""
    print(f"  {bg}: {count:5}{is_latin}")

print()
print("Character mapping used:")
for c in sorted(mapping.keys()):
    locked = " [LOCKED]" if c in KNOWN_MAPPINGS else ""
    print(f"  {c} → {mapping[c]}{locked}")

# Save
with open('smart_decoded_voynich.txt', 'w') as f:
    f.write("SMART DECODER RESULTS\n")
    f.write(f"Known words found: {', '.join(sorted(found_words))}\n\n")
    f.write(decoded_full)

print()
print(f"\nResults saved to: smart_decoded_voynich.txt")
