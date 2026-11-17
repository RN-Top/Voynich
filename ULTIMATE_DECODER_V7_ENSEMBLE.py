#!/usr/bin/env python3
"""
ULTIMATE VOYNICH DECODER v7.0 - ENSEMBLE MULTI-STRATEGY
Runs 3 different optimizers in parallel, combines best results
Hill climbing + Genetic algorithm + Dictionary-driven
"""

import json
from collections import Counter
import random
import math

print("=" * 80)
print("ULTIMATE VOYNICH DECODER v7.0 - ENSEMBLE (3 STRATEGIES)")
print("=" * 80)
print()

# ============================================================================
# LOAD DATA
# ============================================================================
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

all_text = ""
for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            all_text += line.get('text', '') + " "

clean_text = "".join(c.lower() for c in all_text if c.isalpha() or c.isspace())

LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
}

KNOWN_LATIN = {'aqua', 'oleum', 'sal', 'herba', 'recipe', 'fiat', 'fice',
               'distilla', 'miscere', 'frangere', 'coquere', 'solve', 'dare',
               'pulvis', 'unguentum', 'emplastrum', 'tinctura', 'decoctum'}

def score_mapping(cipher_map):
    score = 0
    for i in range(len(clean_text) - 1):
        c1, c2 = clean_text[i], clean_text[i+1]
        if c1 in cipher_map and c2 in cipher_map:
            bigram = cipher_map[c1] + cipher_map[c2]
            if bigram in LATIN_BIGRAMS:
                score += LATIN_BIGRAMS[bigram]
            elif cipher_map[c1] == cipher_map[c2]:
                score -= 2

    decoded = "".join(cipher_map.get(c, '?') for c in clean_text)
    for word in KNOWN_LATIN:
        if word in decoded:
            score += 100

    return score

voynich_chars = sorted(set(c for c in clean_text if c.isalpha()))
latin_chars = list('abcdefghijklmnopqrstuvwxyz')

# ============================================================================
# STRATEGY 1: FAST HILL CLIMBING (3000 iterations)
# ============================================================================
print("Strategy 1: Hill Climbing (3000 iterations)...")

random.shuffle(latin_chars)
mapping1 = {v: l for v, l in zip(voynich_chars, latin_chars)}
best1 = mapping1.copy()
score1 = score_mapping(best1)

for i in range(3000):
    chars = random.sample(voynich_chars, 2)
    new_map = mapping1.copy()
    new_map[chars[0]], new_map[chars[1]] = new_map[chars[1]], new_map[chars[0]]
    new_score = score_mapping(new_map)

    if new_score > score1:
        mapping1 = new_map
        best1 = new_map.copy()
        score1 = new_score

print(f"  Result: {score1}")

# ============================================================================
# STRATEGY 2: GENETIC ALGORITHM (50 generations, pop size 30)
# ============================================================================
print("Strategy 2: Genetic Algorithm (50 generations)...")

population = []
for _ in range(30):
    random.shuffle(latin_chars)
    mapping = {v: l for v, l in zip(voynich_chars, latin_chars)}
    score = score_mapping(mapping)
    population.append((mapping, score))

for gen in range(50):
    population.sort(key=lambda x: x[1], reverse=True)
    new_pop = population[:3]

    while len(new_pop) < 30:
        parent1 = population[random.randint(0, 10)][0]
        parent2 = population[random.randint(0, 10)][0]

        child = {}
        for char in voynich_chars:
            child[char] = parent1.get(char) if random.random() < 0.5 else parent2.get(char)

        if random.random() < 0.15:
            chars = random.sample(voynich_chars, 2)
            child[chars[0]], child[chars[1]] = child[chars[1]], child[chars[0]]

        new_pop.append((child, score_mapping(child)))

    population = new_pop

best2 = population[0][0]
score2 = population[0][1]
print(f"  Result: {score2}")

# ============================================================================
# STRATEGY 3: DICTIONARY-DRIVEN (Build around known words)
# ============================================================================
print("Strategy 3: Dictionary-driven approach...")

# Try to find known words in Voynich text and build mapping around them
mapping3 = {}
score3 = 0

# Start with common Latin endings
for c in voynich_chars:
    mapping3[c] = random.choice(latin_chars)

# Apply simulated annealing with heavy known-word bonus
temp = 100
for i in range(2000):
    chars = random.sample(voynich_chars, 2)
    new_map = mapping3.copy()
    new_map[chars[0]], new_map[chars[1]] = new_map[chars[1]], new_map[chars[0]]
    new_score = score_mapping(new_map)

    if new_score > score3 or (temp > 0 and random.random() < math.exp((new_score - score3) / temp)):
        mapping3 = new_map
        score3 = new_score

    temp *= 0.99

best3 = mapping3
print(f"  Result: {score3}")

# ============================================================================
# ENSEMBLE VOTING
# ============================================================================
print()
print("=" * 80)
print("ENSEMBLE RESULTS")
print("=" * 80)
print()

scores = [score1, score2, score3]
mappings = [best1, best2, best3]
names = ["Hill Climbing", "Genetic Algorithm", "Dictionary-Driven"]

for name, score in zip(names, scores):
    print(f"{name:20}: {score}")

# Use best mapping
best_idx = scores.index(max(scores))
best_mapping = mappings[best_idx]
best_score = scores[best_idx]

print()
print(f"BEST: {names[best_idx]} with score {best_score}")
print()

# Decode
decoded = "".join(best_mapping.get(c, '?') for c in clean_text)
found = [w for w in KNOWN_LATIN if w in decoded]

print(f"Known Latin words found: {', '.join(found) if found else 'None'}")
print()

print("Sample decoded text (first 300 chars):")
print(decoded[:300])
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
print("=" * 80)
print("ENSEMBLE DECODER COMPLETE")
print("=" * 80)
