#!/usr/bin/env python3
"""
ULTIMATE VOYNICH DECODER v4.0 - UNCONSTRAINED OPTIMIZATION
Release all constraints. Let the optimizer find the true mapping.
No assumptions. Pure hill climbing on bigram quality.
"""

import json
from collections import Counter
import random
import math

print("=" * 80)
print("ULTIMATE VOYNICH DECODER v4.0 - UNCONSTRAINED OPTIMIZATION")
print("=" * 80)
print()

# ============================================================================
# LOAD DATA
# ============================================================================
print("[1/4] Loading data...")
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

clean_text = ""
for c in all_text:
    if c.isalpha():
        clean_text += c.lower()
    else:
        clean_text += " "

print(f"   {len(all_text)} characters, {len(all_words)} words")
print()

# ============================================================================
# STAGE 1: BIGRAM QUALITY SYSTEM
# ============================================================================
print("[2/4] Setting up pure bigram optimization...")

# Known Latin bigrams (high score)
LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
    'ua': 5, 'ue': 5, 'oi': 5, 'ai': 5, 'au': 5, 'ci': 4, 'ti': 4, 'di': 4,
    'li': 4, 'ri': 4, 'ni': 4, 'mi': 4, 'hi': 4, 'pi': 4, 'gi': 4, 'fi': 4,
    'bi': 4, 'vi': 4, 'si': 4, 'ca': 3, 'ta': 3, 'da': 3, 'la': 3, 'ra': 3,
    'ma': 3, 'pa': 3, 'ha': 3, 'ga': 3, 'fa': 3, 'ba': 3, 'va': 3, 'sa': 3,
}

def score_mapping(cipher_map):
    """Score mapping purely on Latin bigram matches"""
    score = 0
    for i in range(len(clean_text) - 1):
        c1_encrypted = clean_text[i]
        c2_encrypted = clean_text[i+1]

        if c1_encrypted in cipher_map and c2_encrypted in cipher_map:
            c1_decoded = cipher_map[c1_encrypted]
            c2_decoded = cipher_map[c2_encrypted]
            bigram = c1_decoded + c2_decoded

            if bigram in LATIN_BIGRAMS:
                score += LATIN_BIGRAMS[bigram]
            elif c1_decoded == c2_decoded:
                score -= 2  # Penalize double letters

    return score

# ============================================================================
# STAGE 2: RANDOM INITIALIZATION (NO CONSTRAINTS)
# ============================================================================
print("[3/4] Running unconstrained hill climbing...")

voynich_chars = sorted(set(c for c in clean_text if c.isalpha()))
latin_chars = list('abcdefghijklmnopqrstuvwxyz')

# Random shuffle - start completely fresh
random.shuffle(latin_chars)
initial_mapping = {v: l for v, l in zip(voynich_chars, latin_chars[:len(voynich_chars)])}

initial_score = score_mapping(initial_mapping)
print(f"   Initial random score: {initial_score}")
print()

current_mapping = initial_mapping.copy()
current_score = initial_score
best_mapping = current_mapping.copy()
best_score = current_score

temperature = 50.0
cooling_rate = 0.998
max_iterations = 10000
no_improve_count = 0
max_no_improve = 1000

for iteration in range(max_iterations):
    # Random swap
    chars = list(current_mapping.keys())
    if len(chars) >= 2:
        c1, c2 = random.sample(chars, 2)

        new_mapping = current_mapping.copy()
        new_mapping[c1], new_mapping[c2] = new_mapping[c2], new_mapping[c1]
        new_score = score_mapping(new_mapping)

        # Simulated annealing
        delta = new_score - current_score
        if delta > 0 or (temperature > 0 and random.random() < math.exp(delta / temperature)):
            current_mapping = new_mapping
            current_score = new_score

            if current_score > best_score:
                best_score = current_score
                best_mapping = current_mapping.copy()
                no_improve_count = 0
                if iteration % 100 == 0:
                    print(f"   Iteration {iteration}: New best = {best_score}")
            else:
                no_improve_count += 1
        else:
            no_improve_count += 1

    temperature *= cooling_rate

    # Early stopping if no improvement
    if no_improve_count > max_no_improve:
        print(f"   Converged at iteration {iteration}")
        break

    if iteration % 1000 == 0 and iteration > 0:
        print(f"   ...iteration {iteration}, temp={temperature:.4f}, best={best_score}")

print(f"   Final best score: {best_score}")
print()

# ============================================================================
# STAGE 3: DECODE AND SHOW RESULTS
# ============================================================================
print("=" * 80)
print("UNCONSTRAINED OPTIMIZATION RESULTS")
print("=" * 80)
print()

# Decode first folios
for idx, folio in enumerate(integrated.get('folios', [])[:3]):
    if not folio.get('has_text'):
        continue

    print(f"--- {folio.get('folio_id')} ---")

    for line_idx, line in enumerate(folio.get('text_lines', [])[:2]):
        words = line.get('words', [])

        decoded_words_line = []
        for word in words:
            decoded = ''.join([best_mapping.get(c.lower(), '?') for c in word])
            decoded_words_line.append(decoded)

        print(f"Original: {' '.join(words[:15])}")
        print(f"Decoded:  {' '.join(decoded_words_line[:15])}")
        print()

print("=" * 80)
print("Top bigrams in decoded text:")
print("=" * 80)

decoded_full = ""
for c in clean_text:
    if c in best_mapping:
        decoded_full += best_mapping[c]
    else:
        decoded_full += '?'

decoded_bigrams = Counter()
for i in range(len(decoded_full) - 1):
    if decoded_full[i].isalpha() and decoded_full[i+1].isalpha():
        decoded_bigrams[(decoded_full[i], decoded_full[i+1])] += 1

print("\nTop 20 bigrams in decoded text:")
for (c1, c2), count in decoded_bigrams.most_common(20):
    bigram = c1 + c2
    is_known = " [LATIN]" if bigram in LATIN_BIGRAMS else ""
    print(f"  {bigram}: {count:5}{is_known}")
print()

# Check known words
KNOWN_WORDS = ['aqua', 'oleum', 'sal', 'herba', 'recipe', 'fiat', 'distilla', 'miscere', 'dare', 'recipe']
found_words = [w for w in KNOWN_WORDS if w in decoded_full]

print(f"Known Latin words found: {len(found_words)}")
if found_words:
    for word in found_words:
        print(f"  - {word}")
print()

print("Sample decoded text (first 200 chars):")
print(decoded_full[:200])
print()

print("=" * 80)
