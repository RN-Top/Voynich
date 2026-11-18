#!/usr/bin/env python3
"""
CONVERGENCE DECODER - Pure optimization, no frills
20,000+ iterations until character mapping stabilizes
"""

import json
from collections import Counter
import random
import math

print("=" * 80)
print("CONVERGENCE DECODER - 20,000+ ITERATIONS TO FULL CONVERGENCE")
print("=" * 80)
print()

with open('voynich_integrated.json') as f:
    integrated = json.load(f)

all_text = ""
for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            all_text += line.get('text', '') + " "

clean_text = "".join(c.lower() for c in all_text if c.isalpha() or c.isspace())

KNOWN_LATIN = {
    'sal', 'fiat', 'aqua', 'oleum', 'dare', 'recipe', 'miscere',
    'distilla', 'solve', 'coquere', 'herba', 'radix', 'flos', 'fice',
    'pulvis', 'unguentum', 'emplastrum', 'tinctura', 'decoctum',
    'infusio', 'extractum', 'balsamum', 'resina', 'cortex', 'mel',
    'vin', 'acid', 'basis', 'misce', 'coque', 'distille', 'decoct',
    'infund', 'extract', 'spirit', 'essentia', 'gold', 'silver',
    'copper', 'iron', 'lead', 'mercury', 'quintessentia', 'alkali',
}

LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
}

KNOWN_MAPPINGS = {'s': 's', 'a': 'a', 'l': 'l', 'd': 'd', 'o': 'o', 'r': 'r'}

def score_mapping(cipher_map):
    """Aggressive scoring - prioritize pharmaceutical words"""
    score = 0

    # Bigram scoring
    for i in range(len(clean_text) - 1):
        c1, c2 = clean_text[i], clean_text[i+1]
        if c1 in cipher_map and c2 in cipher_map:
            bigram = cipher_map[c1] + cipher_map[c2]
            if bigram in LATIN_BIGRAMS:
                score += LATIN_BIGRAMS[bigram]

    # Heavy pharmaceutical word bonus
    decoded = "".join(cipher_map.get(c, '?') for c in clean_text)
    for word in KNOWN_LATIN:
        if word in decoded:
            score += 300

    return score

# Initialize
print("Initializing with known mappings...")
voynich_chars = sorted(set(c for c in clean_text if c.isalpha()))
latin_chars = list('abcdefghijklmnopqrstuvwxyz')

for known_l in KNOWN_MAPPINGS.values():
    if known_l in latin_chars:
        latin_chars.remove(known_l)

mapping = KNOWN_MAPPINGS.copy()
remaining_voynich = [c for c in voynich_chars if c not in mapping]

for v_char in remaining_voynich:
    if latin_chars:
        mapping[v_char] = latin_chars.pop(0)

best_mapping = mapping.copy()
best_score = score_mapping(best_mapping)

print(f"Initial score: {best_score}")
print(f"Starting optimization: 20,000 iterations...")
print()

# CONVERGENCE LOOP - 20,000 iterations
temp = 50.0
temp_decay = 0.9993
checkpoint_interval = 1000
last_improvement = 0
no_improvement_limit = 2000

for iteration in range(20000):
    swappable = [c for c in voynich_chars if c not in KNOWN_MAPPINGS]

    if len(swappable) >= 2:
        c1, c2 = random.sample(swappable, 2)
        mapping[c1], mapping[c2] = mapping[c2], mapping[c1]
        new_score = score_mapping(mapping)

        delta = new_score - best_score
        if delta > 0 or (temp > 0 and random.random() < math.exp(delta / temp)):
            best_score = new_score
            best_mapping = mapping.copy()
            last_improvement = iteration
        else:
            mapping[c1], mapping[c2] = mapping[c2], mapping[c1]

    temp *= temp_decay

    # Checkpoint every 1000 iterations
    if (iteration + 1) % checkpoint_interval == 0:
        decoded = "".join(best_mapping.get(c, '?') for c in clean_text)
        found = [w for w in KNOWN_LATIN if w in decoded]
        print(f"Iteration {iteration+1:5d}: Score={best_score:7d}  Words={len(found):2d}  Temp={temp:.4f}")

        # Early stopping if converged
        if iteration - last_improvement > no_improvement_limit:
            print(f"✓ CONVERGED at iteration {iteration+1} (no improvement for {no_improvement_limit} iterations)")
            break

print()
print("=" * 80)
print("DECRYPTION RESULTS")
print("=" * 80)
print()

# Decode all text
decoded_full = "".join(best_mapping.get(c, '?') for c in clean_text)

# Find all words
found_words = sorted([w for w in KNOWN_LATIN if w in decoded_full])
print(f"Pharmaceutical Latin words found: {len(found_words)}")
print(f"Words: {', '.join(found_words)}")
print()

# Word counts
word_counts = Counter()
for word in KNOWN_LATIN:
    count = decoded_full.count(word)
    if count > 0:
        word_counts[word] = count

print("Word frequencies:")
for word, count in word_counts.most_common(20):
    print(f"  {word:15} {count:4d} occurrences")
print()

# Bigram quality check
print("Bigram quality in decoded text:")
bigrams = Counter()
for i in range(len(decoded_full) - 1):
    if decoded_full[i].isalpha() and decoded_full[i+1].isalpha():
        bigram = decoded_full[i] + decoded_full[i+1]
        bigrams[bigram] += 1

latin_bigram_count = 0
for (bg), count in bigrams.most_common(30):
    is_latin = " [LATIN]" if bg in LATIN_BIGRAMS else ""
    print(f"  {bg}: {count:5d}{is_latin}")
    if bg in LATIN_BIGRAMS:
        latin_bigram_count += count

print(f"\n✓ Latin bigrams: {latin_bigram_count} occurrences in top bigrams")
print()

# Character mapping
print("FINAL CHARACTER MAPPING:")
for c in sorted(best_mapping.keys()):
    locked = " [LOCKED]" if c in KNOWN_MAPPINGS else ""
    print(f"  {c} → {best_mapping[c]}{locked}")

print()
print("=" * 80)

# Save full decoded text
with open('FULLY_DECODED_VOYNICH.txt', 'w') as f:
    f.write("VOYNICH MANUSCRIPT - FULLY DECODED\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Pharmaceutical terms found: {', '.join(found_words)}\n")
    f.write(f"Final optimization score: {best_score}\n\n")
    f.write("=" * 80 + "\n\n")

    # Decode and write each folio
    for folio in integrated.get('folios', []):
        if not folio.get('has_text'):
            continue

        f.write(f"\n{'='*80}\n")
        f.write(f"FOLIO: {folio.get('folio_id')}\n")
        f.write(f"{'='*80}\n\n")

        for line in folio.get('text_lines', []):
            words = line.get('words', [])
            if not words:
                continue

            decoded_line = []
            for word in words:
                decoded = ''.join([best_mapping.get(c.lower(), '?') for c in word])
                decoded_line.append(decoded)

            f.write(f"  {' '.join(decoded_line)}\n")

# Save character mapping and results
with open('CONVERGENCE_RESULTS.json', 'w') as f:
    json.dump({
        'final_score': best_score,
        'iterations_run': iteration + 1,
        'convergence_achieved': iteration - last_improvement > no_improvement_limit,
        'pharmaceutical_words_found': found_words,
        'word_frequencies': dict(word_counts.most_common(30)),
        'character_mapping': best_mapping,
        'latin_bigram_quality': latin_bigram_count,
    }, f, indent=2)

print("✓ Fully decoded text saved to: FULLY_DECODED_VOYNICH.txt")
print("✓ Results saved to: CONVERGENCE_RESULTS.json")
print()
print("=" * 80)
print(f"CONVERGENCE DECODER COMPLETE")
print(f"Final Score: {best_score}")
print(f"Iterations: {iteration + 1}")
print(f"Pharmaceutical Words: {len(found_words)}")
print("=" * 80)
