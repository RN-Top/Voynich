#!/usr/bin/env python3
"""
ULTIMATE VOYNICH DECODER v6.0 - GENETIC ALGORITHM
Population-based: Crossover + Mutation + Selection
Different approach - evolve populations of mappings
"""

import json
from collections import Counter
import random

print("=" * 80)
print("ULTIMATE VOYNICH DECODER v6.0 - GENETIC ALGORITHM")
print("=" * 80)
print()

# ============================================================================
# LOAD DATA
# ============================================================================
print("[1/5] Loading data...")
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

all_text = ""
for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            all_text += line.get('text', '') + " "

clean_text = "".join(c.lower() for c in all_text if c.isalpha() or c.isspace())
print(f"   {len(all_text)} characters")
print()

# ============================================================================
# STAGE 1: SCORING SYSTEM
# ============================================================================
print("[2/5] Setting up genetic algorithm...")

LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
    'ua': 5, 'ue': 5, 'oi': 5, 'ai': 5, 'au': 5,
}

KNOWN_LATIN = {'aqua', 'oleum', 'sal', 'herba', 'recipe', 'fiat', 'distilla', 'miscere', 'dare', 'solve'}

def score_mapping(cipher_map):
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

    # Known word scoring
    decoded = "".join(cipher_map.get(c, '?') for c in clean_text)
    for word in KNOWN_LATIN:
        if word in decoded:
            score += 100

    return score

# ============================================================================
# STAGE 2: CREATE INITIAL POPULATION
# ============================================================================
print("[3/5] Creating population and evolving...")

voynich_chars = sorted(set(c for c in clean_text if c.isalpha()))
latin_chars = list('abcdefghijklmnopqrstuvwxyz')

POPULATION_SIZE = 50
population = []

for _ in range(POPULATION_SIZE):
    random.shuffle(latin_chars)
    mapping = {v: l for v, l in zip(voynich_chars, latin_chars)}
    score = score_mapping(mapping)
    population.append((mapping, score))

population.sort(key=lambda x: x[1], reverse=True)
print(f"   Initial best score: {population[0][1]}")
print()

# ============================================================================
# STAGE 3: GENETIC EVOLUTION
# ============================================================================
GENERATIONS = 100
MUTATION_RATE = 0.1
ELITE_SIZE = 5

for generation in range(GENERATIONS):
    # Elitism: Keep best mappings
    new_population = population[:ELITE_SIZE]

    # Create new individuals through crossover + mutation
    while len(new_population) < POPULATION_SIZE:
        # Tournament selection
        parent1 = population[random.randint(0, min(POPULATION_SIZE//2, len(population)-1))][0]
        parent2 = population[random.randint(0, min(POPULATION_SIZE//2, len(population)-1))][0]

        # Crossover: Mix parent mappings
        child = {}
        for char in voynich_chars:
            if random.random() < 0.5:
                child[char] = parent1.get(char, random.choice(latin_chars))
            else:
                child[char] = parent2.get(char, random.choice(latin_chars))

        # Mutation: Random swaps
        if random.random() < MUTATION_RATE:
            chars = random.sample(voynich_chars, 2)
            child[chars[0]], child[chars[1]] = child[chars[1]], child[chars[0]]

        score = score_mapping(child)
        new_population.append((child, score))

    # Sort by fitness
    population = sorted(new_population, key=lambda x: x[1], reverse=True)[:POPULATION_SIZE]

    best_score = population[0][1]
    if generation % 10 == 0:
        print(f"   Generation {generation}: Best = {best_score}")

print(f"\n   Final best score: {population[0][1]}")
print()

# ============================================================================
# STAGE 4: DECODE WITH BEST MAPPING
# ============================================================================
print("[4/5] Decoding with evolved best mapping...")

best_mapping = population[0][0]

decoded = "".join(best_mapping.get(c, '?') for c in clean_text)
found = [w for w in KNOWN_LATIN if w in decoded]

print(f"Known Latin words found: {', '.join(found) if found else 'None'}")
print()

# Show sample
print("Sample decoded text (first 400 chars):")
print(decoded[:400])
print()

# Top bigrams
bigrams = Counter()
for i in range(len(decoded) - 1):
    if decoded[i].isalpha() and decoded[i+1].isalpha():
        bigrams[(decoded[i], decoded[i+1])] += 1

print("Top bigrams:")
for (c1, c2), count in bigrams.most_common(15):
    bg = c1 + c2
    is_latin = " [LATIN]" if bg in LATIN_BIGRAMS else ""
    print(f"  {bg}: {count:5}{is_latin}")

print()

# Decode first folios
print("[5/5] Sample decoded folios:")
print()

for idx, folio in enumerate(integrated.get('folios', [])[:2]):
    if not folio.get('has_text'):
        continue

    print(f"--- {folio.get('folio_id')} ---")

    for line_idx, line in enumerate(folio.get('text_lines', [])[:2]):
        words = line.get('words', [])

        decoded_words = []
        for word in words:
            decoded_word = ''.join([best_mapping.get(c.lower(), '?') for c in word])
            decoded_words.append(decoded_word)

        print(f"Original: {' '.join(words[:12])}")
        print(f"Decoded:  {' '.join(decoded_words[:12])}")
        print()

print("=" * 80)
print("GENETIC ALGORITHM DECODER COMPLETE")
print("=" * 80)
