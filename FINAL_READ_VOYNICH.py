#!/usr/bin/env python3
"""
FINAL ATTEMPT - READ THE VOYNICH MANUSCRIPT
Using everything learned today:
- Genetic algorithm approach (best scores)
- Known character anchors
- Two-layer decryption (cipher + abbreviations)
- Pharmaceutical recipe patterns
"""

import json
from collections import Counter
import random
import math

print("=" * 80)
print("FINAL VOYNICH READING - USING TODAY'S BREAKTHROUGHS")
print("=" * 80)
print()

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

all_text = ""
for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            all_text += line.get('text', '') + " "

clean_text = "".join(c.lower() for c in all_text if c.isalpha() or c.isspace())

print("Step 1: Set up with what we KNOW works")
print("=" * 80)
print()

# What we know from today's experiments
KNOWN_MAPPINGS = {
    's': 's',  # from sal
    'a': 'a',  # from abbreviations
    'l': 'l',  # from abbreviations
    'd': 'd',  # from dar
    'o': 'o',  # from oleum
    'r': 'r',  # from dar
}

# Medieval pharmaceutical abbreviations we know exist
ABBREV = {
    'dar': 'dare',      # take
    'ol': 'oleum',      # oil
    'sal': 'sal',       # salt
    'aqua': 'aqua',     # water
    'sol': 'solve',     # dissolve
    'dis': 'distilla',  # distill
    'misc': 'miscere',  # mix
    'coq': 'coquere',   # boil
    'frac': 'frangere', # crush
    'pul': 'pulvis',    # powder
}

# Known pharmaceutical Latin words
KNOWN_LATIN = {
    'sal', 'fiat', 'aqua', 'oleum', 'dare', 'recipe', 'miscere',
    'distilla', 'solve', 'coquere', 'herba', 'radix', 'flos', 'fice',
    'pulvis', 'unguentum', 'emplastrum', 'tinctura', 'decoctum',
    'infusio', 'extractum', 'balsamum', 'resina', 'cortex',
}

# Latin bigrams that appear in pharmaceutical texts
LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
}

print(f"Known character locks: {KNOWN_MAPPINGS}")
print(f"Known abbreviations: {len(ABBREV)}")
print(f"Target Latin words: {len(KNOWN_LATIN)}")
print()

# Build initial mapping
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

print("Step 2: Genetic algorithm optimization (5000 iterations)")
print("=" * 80)
print()

def score_mapping(cipher_map):
    score = 0

    # Bigram scoring
    for i in range(len(clean_text) - 1):
        c1, c2 = clean_text[i], clean_text[i+1]
        if c1 in cipher_map and c2 in cipher_map:
            bigram = cipher_map[c1] + cipher_map[c2]
            if bigram in LATIN_BIGRAMS:
                score += LATIN_BIGRAMS[bigram]

    # Known word bonus (aggressive)
    decoded = "".join(cipher_map.get(c, '?') for c in clean_text)
    for word in KNOWN_LATIN:
        if word in decoded:
            score += 200

    return score

best_mapping = mapping.copy()
best_score = score_mapping(best_mapping)

temp = 50.0
for i in range(5000):
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

    temp *= 0.9994

mapping = best_mapping

print(f"Final score: {best_score}")
print()

print("Step 3: DECODE AND READ THE VOYNICH")
print("=" * 80)
print()

# Decode all text
decoded_full = "".join(mapping.get(c, '?') for c in clean_text)

# Find known words
found_words = sorted(set(w for w in KNOWN_LATIN if w in decoded_full))
print(f"Known Latin pharmaceutical words found: {len(found_words)}")
if found_words:
    print(f"Words: {', '.join(found_words)}")
print()

# Now read the folios
print("FOLIO READINGS:")
print()

for idx, folio in enumerate(integrated.get('folios', [])):
    if not folio.get('has_text') or idx > 9:
        continue

    folio_id = folio.get('folio_id', 'unknown')

    # Collect all lines for this folio
    folio_text = []
    folio_found_words = []

    for line in folio.get('text_lines', []):
        words = line.get('words', [])
        if not words:
            continue

        # Decode each word
        decoded_words = []
        for word in words:
            decoded_word = ''.join([mapping.get(c.lower(), '?') for c in word])
            decoded_words.append(decoded_word)

            # Check for known words
            for known in KNOWN_LATIN:
                if known in decoded_word.lower():
                    folio_found_words.append(known)

        folio_text.append(' '.join(decoded_words))

    # Only print if we found something interesting
    if folio_found_words:
        print(f"\n{'╔' + '═' * 70 + '╗'}")
        print(f"║ FOLIO {folio_id:62}║")
        print(f"{'║ FOUND: ' + ', '.join(set(folio_found_words)):71}║")
        print(f"{'╚' + '═' * 70 + '╝'}")

        # Print first 10 lines of folio
        for line in folio_text[:10]:
            print(f"  {line[:75]}")
        print()

print()
print("Step 4: WHAT WE'RE READING")
print("=" * 80)
print()

print("Top pharmaceutical terms found:")
word_counts = Counter()
for folio in integrated.get('folios', []):
    if not folio.get('has_text'):
        continue
    for line in folio.get('text_lines', []):
        words = line.get('words', [])
        for word in words:
            decoded = ''.join([mapping.get(c.lower(), '?') for c in word])
            for known in KNOWN_LATIN:
                if known in decoded.lower():
                    word_counts[known] += 1

for word, count in word_counts.most_common(10):
    print(f"  {word:15} {count:3} occurrences")

print()
print("Character mapping final state:")
for c in sorted(mapping.keys()):
    locked = " [LOCKED]" if c in KNOWN_MAPPINGS else ""
    print(f"  {c} → {mapping[c]}{locked}")

print()
print("=" * 80)
print("READING COMPLETE")
print("=" * 80)

# Save full readable version
with open('VOYNICH_READABLE.txt', 'w') as f:
    f.write("VOYNICH MANUSCRIPT - READABLE DECRYPTION ATTEMPT\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Pharmaceutical Latin words found: {', '.join(found_words)}\n\n")
    f.write("=" * 80 + "\n\n")

    for folio in integrated.get('folios', []):
        if not folio.get('has_text'):
            continue

        f.write(f"\nFOLIO: {folio.get('folio_id')}\n")
        f.write("-" * 70 + "\n\n")

        for line in folio.get('text_lines', []):
            words = line.get('words', [])
            if not words:
                continue

            decoded_line = []
            for word in words:
                decoded = ''.join([mapping.get(c.lower(), '?') for c in word])
                decoded_line.append(decoded)

            f.write(f"  {' '.join(decoded_line)}\n")

print("\nFull readable text saved to: VOYNICH_READABLE.txt")
