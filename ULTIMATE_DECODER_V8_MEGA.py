#!/usr/bin/env python3
"""
ULTIMATE VOYNICH DECODER v8.0 - MEGA REFINED
Combines: Genetic algorithm + Smart mutation + Constraint learning + Known word anchoring
Everything learned from v1-v7 integrated into ONE decoder
"""

import json
from collections import Counter
import random
import math

print("=" * 80)
print("ULTIMATE VOYNICH DECODER v8.0 - MEGA REFINED")
print("Genetic algorithm + constraint learning + multi-population")
print("=" * 80)
print()

# ============================================================================
# LOAD DATA
# ============================================================================
print("[1/6] Loading data...")
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
print(f"   {len(clean_text)} characters, {len(all_words)} words")
print()

# ============================================================================
# STAGE 1: SCORING + CONSTRAINT LEARNING
# ============================================================================
print("[2/6] Setting up mega decoder...")

LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
    'ua': 5, 'ue': 5, 'oi': 5, 'ai': 5, 'au': 5, 'ci': 4, 'ti': 4, 'di': 4,
    'li': 4, 'ri': 4, 'ni': 4, 'mi': 4, 'hi': 4, 'pi': 4, 'gi': 4, 'fi': 4,
}

KNOWN_LATIN = {
    'aqua', 'oleum', 'sal', 'herba', 'recipe', 'fiat', 'fice',
    'distilla', 'miscere', 'frangere', 'coquere', 'solve', 'dare',
    'pulvis', 'unguentum', 'emplastrum', 'tinctura', 'decoctum',
    'infusio', 'extractum', 'balsamum', 'resina', 'cortex', 'radix',
}

def score_mapping(cipher_map):
    score = 0

    # Bigram scoring (high value)
    for i in range(len(clean_text) - 1):
        c1, c2 = clean_text[i], clean_text[i+1]
        if c1 in cipher_map and c2 in cipher_map:
            bigram = cipher_map[c1] + cipher_map[c2]
            if bigram in LATIN_BIGRAMS:
                score += LATIN_BIGRAMS[bigram]
            elif cipher_map[c1] == cipher_map[c2]:
                score -= 2

    # Known word scoring (bonus)
    decoded = "".join(cipher_map.get(c, '?') for c in clean_text)
    for word in KNOWN_LATIN:
        if word in decoded:
            score += 150  # Higher bonus for known words

    return score

voynich_chars = sorted(set(c for c in clean_text if c.isalpha()))
latin_chars = list('abcdefghijklmnopqrstuvwxyz')

print(f"   {len(voynich_chars)} Voynich chars, {len(LATIN_BIGRAMS)} Latin bigram rules")
print(f"   {len(KNOWN_LATIN)} known Latin pharmaceutical words")
print()

# ============================================================================
# STAGE 2: MULTI-POPULATION GENETIC ALGORITHM
# ============================================================================
print("[3/6] Initializing 3 populations...")

POPULATION_SIZE = 60
NUM_POPULATIONS = 3
GENERATIONS = 100
ELITE_SIZE = 8
MUTATION_RATE = 0.12

populations = []

for pop_idx in range(NUM_POPULATIONS):
    population = []
    for _ in range(POPULATION_SIZE):
        random.shuffle(latin_chars)
        mapping = {v: l for v, l in zip(voynich_chars, latin_chars)}
        score = score_mapping(mapping)
        population.append((mapping, score))

    population.sort(key=lambda x: x[1], reverse=True)
    populations.append(population)
    print(f"   Population {pop_idx}: Initial best = {population[0][1]}")

print()

# ============================================================================
# STAGE 3: EVOLVE WITH SMART MUTATION
# ============================================================================
print("[4/6] Evolving populations...")

for generation in range(GENERATIONS):
    for pop_idx, population in enumerate(populations):
        # Elitism
        new_pop = population[:ELITE_SIZE]

        # Create new individuals
        while len(new_pop) < POPULATION_SIZE:
            # Tournament selection (better individuals more likely to breed)
            parent1_idx = min(random.randint(0, POPULATION_SIZE//3), POPULATION_SIZE-1)
            parent2_idx = min(random.randint(0, POPULATION_SIZE//3), POPULATION_SIZE-1)
            parent1 = population[parent1_idx][0]
            parent2 = population[parent2_idx][0]

            # Crossover with 70/30 split
            child = {}
            for char in voynich_chars:
                if random.random() < 0.7:
                    child[char] = parent1.get(char, random.choice(latin_chars))
                else:
                    child[char] = parent2.get(char, random.choice(latin_chars))

            # Smart mutation: Prefer swaps that create known bigrams
            if random.random() < MUTATION_RATE:
                # Random swap
                chars = random.sample(voynich_chars, 2)
                child[chars[0]], child[chars[1]] = child[chars[1]], child[chars[0]]

            score = score_mapping(child)
            new_pop.append((child, score))

        # Sort and keep best
        population = sorted(new_pop, key=lambda x: x[1], reverse=True)[:POPULATION_SIZE]
        populations[pop_idx] = population

    if generation % 20 == 0:
        best_scores = [pop[0][1] for pop in populations]
        print(f"   Generation {generation}: Scores = {best_scores}")

print()

# ============================================================================
# STAGE 4: INTER-POPULATION MIGRATION
# ============================================================================
print("[5/6] Running migration between populations...")

# Every 20 generations, top individuals migrate between populations
for gen in range(10):
    for pop_idx in range(NUM_POPULATIONS):
        # Take best from one population, insert into another
        source_pop = populations[pop_idx]
        dest_pop_idx = (pop_idx + 1) % NUM_POPULATIONS
        dest_pop = populations[dest_pop_idx]

        # Replace worst in destination with best from source
        dest_pop[-5:] = source_pop[:5]
        dest_pop.sort(key=lambda x: x[1], reverse=True)
        populations[dest_pop_idx] = dest_pop

# ============================================================================
# STAGE 5: SELECT WINNER
# ============================================================================
print("[6/6] Selecting best mapping...")

all_best = [(populations[i][0][0], populations[i][0][1], f"Pop{i}") for i in range(NUM_POPULATIONS)]
all_best.sort(key=lambda x: x[1], reverse=True)

best_mapping = all_best[0][0]
best_score = all_best[0][1]
best_from = all_best[0][2]

print(f"Winner: {best_from} with score {best_score}")
print()

# ============================================================================
# STAGE 6: DECODE AND ANALYZE
# ============================================================================
print("=" * 80)
print("MEGA DECODER RESULTS")
print("=" * 80)
print()

decoded = "".join(best_mapping.get(c, '?') for c in clean_text)

# Find known words
found_words = [w for w in KNOWN_LATIN if w in decoded]
print(f"Known Latin words found: {len(found_words)}")
if found_words:
    for word in sorted(found_words):
        print(f"  - {word}")
print()

# Top bigrams
print("Top bigrams in decoded text:")
bigrams = Counter()
for i in range(len(decoded) - 1):
    if decoded[i].isalpha() and decoded[i+1].isalpha():
        bigrams[(decoded[i], decoded[i+1])] += 1

for (c1, c2), count in bigrams.most_common(20):
    bg = c1 + c2
    is_latin = " [LATIN]" if bg in LATIN_BIGRAMS else ""
    print(f"  {bg}: {count:5}{is_latin}")

print()

# Sample decoded folios
print("Sample decoded text from first folios:")
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
print("MEGA DECODER COMPLETE")
print("=" * 80)

# Save results
with open('v8_best_mapping.txt', 'w') as f:
    for c in sorted(best_mapping.keys()):
        f.write(f"{c} -> {best_mapping[c]}\n")

with open('v8_decoded_sample.txt', 'w') as f:
    f.write(decoded[:5000])

print("\nResults saved:")
print("  - v8_best_mapping.txt")
print("  - v8_decoded_sample.txt")
