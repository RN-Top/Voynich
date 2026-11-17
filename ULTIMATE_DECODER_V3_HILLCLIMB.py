#!/usr/bin/env python3
"""
ULTIMATE VOYNICH DECODER v3.0 - HILL CLIMBING OPTIMIZER
Uses: Simulated annealing + bigram scoring to optimize cipher mapping
Push it further. Optimize the shit out of this.
"""

import json
from collections import Counter
import random
import math

print("=" * 80)
print("ULTIMATE VOYNICH DECODER v3.0 - HILL CLIMBING OPTIMIZER")
print("=" * 80)
print()

# ============================================================================
# LOAD DATA
# ============================================================================
print("[1/5] Loading data...")
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

# Clean text for bigram analysis
clean_text = ""
for c in all_text:
    if c.isalpha():
        clean_text += c.lower()
    else:
        clean_text += " "

print(f"   Loaded {len(all_text)} characters, {len(all_words)} words")
print()

# ============================================================================
# STAGE 1: BUILD BIGRAM SCORING SYSTEM
# ============================================================================
print("[2/5] Building bigram scoring system...")

# Known Latin bigrams (high score = very common in Latin)
LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
    'ua': 5, 'ue': 5, 'oi': 5, 'ai': 5, 'au': 5, 'ci': 4, 'ti': 4, 'di': 4,
    'li': 4, 'ri': 4, 'ni': 4, 'mi': 4, 'hi': 4, 'pi': 4, 'gi': 4, 'fi': 4,
    'bi': 4, 'vi': 4, 'si': 4, 'ca': 3, 'ta': 3, 'da': 3, 'la': 3, 'ra': 3,
    'ma': 3, 'pa': 3, 'ha': 3, 'ga': 3, 'fa': 3, 'ba': 3, 'va': 3, 'sa': 3,
}

# Forbidden bigrams (never in Latin)
FORBIDDEN_BIGRAMS = {
    'qq', 'xx', 'zz', 'jj', 'ww', 'kk',
}

def score_bigram_quality(cipher_map):
    """Score how many bigrams in decoded text match known Latin bigrams"""
    score = 0
    count = 0

    for i in range(len(clean_text) - 1):
        c1_encrypted = clean_text[i]
        c2_encrypted = clean_text[i+1]

        if c1_encrypted in cipher_map and c2_encrypted in cipher_map:
            c1_decoded = cipher_map[c1_encrypted]
            c2_decoded = cipher_map[c2_encrypted]
            bigram = c1_decoded + c2_decoded

            count += 1

            if bigram in LATIN_BIGRAMS:
                score += LATIN_BIGRAMS[bigram]
            elif bigram in FORBIDDEN_BIGRAMS:
                score -= 5
            elif bigram[0] == bigram[1]:  # Double letters
                score -= 1

    return score if count > 0 else 0

print(f"   {len(LATIN_BIGRAMS)} known Latin bigrams")
print(f"   {len(FORBIDDEN_BIGRAMS)} forbidden bigrams")
print()

# ============================================================================
# STAGE 2: INITIALIZE WITH CONSTRAINTS
# ============================================================================
print("[3/5] Initializing with constraint-based mapping...")

# Start with what we know from abbreviations
initial_mapping = {
    'a': 'a', 'd': 'd', 'o': 'o', 'l': 'l', 'r': 'r',
}

# Fill in remaining characters by frequency
voynich_chars = sorted(set(c for c in clean_text if c.isalpha()))
latin_chars = 'etarinoshducmgfpbvkwxyjzq'
used_latin = set(initial_mapping.values())

for v_char in voynich_chars:
    if v_char not in initial_mapping:
        for l_char in latin_chars:
            if l_char not in used_latin:
                initial_mapping[v_char] = l_char
                used_latin.add(l_char)
                break

initial_score = score_bigram_quality(initial_mapping)
print(f"   Initial mapping score: {initial_score}")
print()

# ============================================================================
# STAGE 3: HILL CLIMBING WITH SIMULATED ANNEALING
# ============================================================================
print("[4/5] Running hill climbing optimization (this may take a moment)...")

current_mapping = initial_mapping.copy()
current_score = initial_score
best_mapping = current_mapping.copy()
best_score = current_score

temperature = 100.0
cooling_rate = 0.995
iterations = 0
max_iterations = 5000

for iteration in range(max_iterations):
    iterations += 1

    # Random swap of two characters
    chars = list(current_mapping.keys())
    if len(chars) >= 2:
        c1, c2 = random.sample(chars, 2)

        # Don't swap the constrained ones (from abbreviations)
        if c1 not in initial_mapping or c2 not in initial_mapping:
            # Try swap
            new_mapping = current_mapping.copy()
            new_mapping[c1], new_mapping[c2] = new_mapping[c2], new_mapping[c1]
            new_score = score_bigram_quality(new_mapping)

            # Accept or reject (simulated annealing)
            delta = new_score - current_score
            if delta > 0 or (temperature > 0 and random.random() < math.exp(delta / temperature)):
                current_mapping = new_mapping
                current_score = new_score

                # Track best
                if current_score > best_score:
                    best_score = current_score
                    best_mapping = current_mapping.copy()
                    print(f"   Iteration {iteration}: New best score = {best_score}")

    # Cool down
    temperature *= cooling_rate

    # Progress indicator
    if iteration % 500 == 0 and iteration > 0:
        print(f"   ...iteration {iteration}/{max_iterations}, temp={temperature:.2f}, score={current_score}")

print(f"   Optimization complete: {iterations} iterations")
print(f"   Final best score: {best_score}")
print()

# ============================================================================
# STAGE 4: DECODE WITH OPTIMIZED MAPPING
# ============================================================================
print("[5/5] Decoding with optimized mapping...")
print()

# Decode first few folios
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
# STAGE 5: ANALYSIS
# ============================================================================
print("=" * 80)
print("OPTIMIZATION RESULTS")
print("=" * 80)
print()

print("Final optimized mapping:")
for c in sorted(best_mapping.keys()):
    print(f"  {c} -> {best_mapping[c]}")
print()

# Check for known words
decoded_full = ""
for c in clean_text:
    if c in best_mapping:
        decoded_full += best_mapping[c]
    else:
        decoded_full += '?'

KNOWN_WORDS = ['aqua', 'oleum', 'sal', 'herba', 'recipe', 'fiat', 'distilla', 'miscere']
found_words = [w for w in KNOWN_WORDS if w in decoded_full]

print(f"Known Latin words found: {len(found_words)}")
if found_words:
    print(f"  {', '.join(found_words)}")
print()

# Bigram quality
print("Bigram quality after optimization:")
quality_score = 0
total_bigrams = 0
for i in range(len(decoded_full) - 1):
    c1, c2 = decoded_full[i], decoded_full[i+1]
    if c1.isalpha() and c2.isalpha():
        bigram = c1 + c2
        total_bigrams += 1
        if bigram in LATIN_BIGRAMS:
            quality_score += LATIN_BIGRAMS[bigram]

print(f"  Latin bigram matches: {quality_score}/{total_bigrams} quality points")
print(f"  Average quality per bigram: {quality_score/total_bigrams if total_bigrams > 0 else 0:.2f}")
print()

print("=" * 80)
print("HILL CLIMBING DECODER COMPLETE")
print("=" * 80)
