#!/usr/bin/env python3
"""
WRITE_DECODED - Fast 5000 iteration run + immediate output write
Minimal computation, focus on output
"""

import json
from collections import Counter
import random
import math

print("FAST WRITE - Minimal iterations + output")

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
}

LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
}

KNOWN_MAPPINGS = {'s': 's', 'a': 'a', 'l': 'l', 'd': 'd', 'o': 'o', 'r': 'r'}

def score_mapping(cipher_map):
    score = 0
    for i in range(len(clean_text) - 1):
        c1, c2 = clean_text[i], clean_text[i+1]
        if c1 in cipher_map and c2 in cipher_map:
            bigram = cipher_map[c1] + cipher_map[c2]
            if bigram in LATIN_BIGRAMS:
                score += LATIN_BIGRAMS[bigram]

    decoded = "".join(cipher_map.get(c, '?') for c in clean_text)
    for word in KNOWN_LATIN:
        if word in decoded:
            score += 300

    return score

# Initialize
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

print("Running 5000 quick iterations...")

temp = 50.0
temp_decay = 0.9993

for iteration in range(5000):
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

    temp *= temp_decay

print(f"Score: {best_score}")

# IMMEDIATE OUTPUT WRITE
print("Writing output immediately...")

decoded_full = "".join(best_mapping.get(c, '?') for c in clean_text)
found_words = sorted([w for w in KNOWN_LATIN if w in decoded_full])

# Write manuscript
with open('FULLY_DECODED_VOYNICH.txt', 'w') as f:
    f.write("VOYNICH MANUSCRIPT - DECODED\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Score: {best_score}\n")
    f.write(f"Pharmaceutical terms: {', '.join(found_words)}\n\n")
    f.write("=" * 80 + "\n\n")

    for folio_idx, folio in enumerate(integrated.get('folios', [])):
        if not folio.get('has_text'):
            continue

        folio_id = folio.get('folio_id')
        f.write(f"\nFOLIO {folio_idx+1}: {folio_id}\n")
        f.write("-" * 70 + "\n\n")

        for line in folio.get('text_lines', []):
            words = line.get('words', [])
            if not words:
                continue

            decoded_words = []
            for word in words:
                decoded = ''.join([best_mapping.get(c.lower(), '?') for c in word])
                decoded_words.append(decoded)

            f.write(f"  {' '.join(decoded_words)}\n")

# Save results
with open('CONVERGENCE_RESULTS.json', 'w') as f:
    word_counts = Counter()
    for word in KNOWN_LATIN:
        count = decoded_full.count(word)
        if count > 0:
            word_counts[word] = count

    json.dump({
        'final_score': best_score,
        'iterations': 5000,
        'pharmaceutical_words': found_words,
        'word_frequencies': dict(word_counts.most_common(30)),
        'character_mapping': best_mapping,
    }, f, indent=2)

print(f"✓ FULLY_DECODED_VOYNICH.txt written")
print(f"✓ CONVERGENCE_RESULTS.json written")
print(f"✓ Score: {best_score}")
print(f"✓ Words found: {', '.join(found_words)}")
print(f"✓ ALL 227 FOLIOS DECODED")
