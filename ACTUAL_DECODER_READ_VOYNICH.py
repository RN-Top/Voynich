#!/usr/bin/env python3
"""
ACTUAL VOYNICH DECODER - READ THE MANUSCRIPT
Use everything we learned to actually decode and read Voynich text
"""

import json
from collections import Counter
import random

print("=" * 80)
print("ACTUAL VOYNICH DECODER - LET'S READ IT")
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

print("Step 1: Building best possible cipher mapping from what we learned")
print("=" * 80)
print()

# What we KNOW from abbreviations (reliable):
KNOWN_MAPPINGS = {
    'a': 'a',  # from dar->dare, sal->sal, aqua->aqua
    'd': 'd',  # from dar->dare
    'o': 'o',  # from oleum
    'l': 'l',  # from oleum
    'r': 'r',  # from dar
    's': 's',  # from sal
}

# V6 discovered that these work well:
# Start with frequency-based but keep the known ones locked
LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
}

KNOWN_LATIN = {
    'sal', 'fiat', 'aqua', 'oleum', 'dare', 'recipe', 'miscere',
    'distilla', 'solve', 'coquere', 'herba', 'radix', 'flos',
}

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
            score += 100

    return score

# Build mapping with constraints locked
voynich_chars = sorted(set(c for c in clean_text if c.isalpha()))
latin_chars = list('abcdefghijklmnopqrstuvwxyz')

# Remove known mappings from available pool
for known_v, known_l in KNOWN_MAPPINGS.items():
    if known_l in latin_chars:
        latin_chars.remove(known_l)

# Start with known mappings
mapping = KNOWN_MAPPINGS.copy()

# Fill in the rest randomly
for v_char in voynich_chars:
    if v_char not in mapping:
        l_char = latin_chars.pop(0) if latin_chars else 'x'
        mapping[v_char] = l_char

print(f"Initial mapping (known + random): {len(mapping)} characters")
print(f"Known locked: {list(KNOWN_MAPPINGS.keys())}")
print()

# Quick optimization: 2000 swaps to improve
print("Quick optimization: 2000 swaps...")
best_mapping = mapping.copy()
best_score = score_mapping(best_mapping)

for i in range(2000):
    # Only swap non-locked characters
    swappable = [c for c in voynich_chars if c not in KNOWN_MAPPINGS]

    if len(swappable) >= 2:
        c1, c2 = random.sample(swappable, 2)
        mapping[c1], mapping[c2] = mapping[c2], mapping[c1]
        score = score_mapping(mapping)

        if score > best_score:
            best_score = score
            best_mapping = mapping.copy()

mapping = best_mapping
print(f"Optimized score: {best_score}")
print()

print("Step 2: Decode and READ Voynich folios")
print("=" * 80)
print()

# Now let's actually READ some folios
for idx, folio in enumerate(integrated.get('folios', [])):
    if not folio.get('has_text') or idx > 4:  # First 5 folios
        continue

    folio_id = folio.get('folio_id', 'unknown')
    print()
    print(f"╔═══════════════════════════════════════════════════════════════╗")
    print(f"║ FOLIO: {folio_id:50} ║")
    print(f"╚═══════════════════════════════════════════════════════════════╝")
    print()

    # Decode each line
    for line_idx, line in enumerate(folio.get('text_lines', [])):
        words = line.get('words', [])

        if not words:
            continue

        # Decode words
        decoded_words = []
        for word in words:
            decoded = ''.join([mapping.get(c.lower(), '?') for c in word])
            decoded_words.append(decoded)

        # Print original and decoded
        orig_text = ' '.join(words)
        decod_text = ' '.join(decoded_words)

        print(f"Original: {orig_text[:70]}")
        print(f"Decoded:  {decod_text[:70]}")
        print()

        # Look for known words
        found_words = [w for w in KNOWN_LATIN if w in ' '.join(decoded_words).lower()]
        if found_words:
            print(f"  → FOUND: {', '.join(found_words)}")
            print()

print()
print("Step 3: Character mapping we're using")
print("=" * 80)
print()

print("Voynich → Latin Mapping:")
for c in sorted(mapping.keys()):
    locked = " [LOCKED]" if c in KNOWN_MAPPINGS else ""
    print(f"  {c} → {mapping[c]}{locked}")

print()
print("Step 4: Statistics")
print("=" * 80)
print()

decoded_full = "".join(mapping.get(c, '?') for c in clean_text)

# Count bigrams
bigrams = Counter()
for i in range(len(decoded_full) - 1):
    if decoded_full[i].isalpha() and decoded_full[i+1].isalpha():
        bigrams[(decoded_full[i], decoded_full[i+1])] += 1

print("Top bigrams in decoded text:")
for (c1, c2), count in bigrams.most_common(20):
    bg = c1 + c2
    is_latin = " [LATIN]" if bg in LATIN_BIGRAMS else ""
    print(f"  {bg}: {count:5}{is_latin}")

print()

# Find all known words
found_all = [w for w in KNOWN_LATIN if w in decoded_full]
print(f"Known Latin words found in full text: {len(found_all)}")
if found_all:
    print(f"  {', '.join(sorted(found_all))}")

print()
print("=" * 80)
print("DECODING COMPLETE")
print("=" * 80)

# Save full decoded text
with open('actual_decoded_voynich.txt', 'w') as f:
    # Write header
    f.write("VOYNICH MANUSCRIPT - ACTUAL DECODING ATTEMPT\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Mapping used: {len(mapping)} character substitutions\n")
    f.write(f"Known words found: {', '.join(sorted(found_all)) if found_all else 'None yet'}\n\n")
    f.write("=" * 80 + "\n\n")

    # Write all folios decoded
    for folio in integrated.get('folios', []):
        if not folio.get('has_text'):
            continue

        f.write(f"\n{'─' * 80}\n")
        f.write(f"FOLIO: {folio.get('folio_id')}\n")
        f.write(f"{'─' * 80}\n\n")

        for line in folio.get('text_lines', []):
            words = line.get('words', [])
            if not words:
                continue

            decoded_line = []
            for word in words:
                decoded_word = ''.join([mapping.get(c.lower(), '?') for c in word])
                decoded_line.append(decoded_word)

            f.write(f"  {' '.join(decoded_line)}\n")

print("\nFull decoded text saved to: actual_decoded_voynich.txt")
