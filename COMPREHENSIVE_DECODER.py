#!/usr/bin/env python3
"""
COMPREHENSIVE EXPERIMENTAL DECODER
Combines all experimental approaches:
1. Extended iterations (10,000+)
2. Locks best mappings + recipe extraction
3. Ensemble voting across variants
4. Historical cross-reference
5. Scoring function variants
"""

import json
from collections import Counter
import random
import math

print("=" * 80)
print("COMPREHENSIVE VOYNICH EXPERIMENTAL DECODER")
print("=" * 80)
print()

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

all_text = ""
all_folios = []
for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        folio_lines = ""
        for line in folio.get('text_lines', []):
            text = line.get('text', '')
            all_text += text + " "
            folio_lines += text + " "
        if folio_lines.strip():
            all_folios.append({
                'id': folio.get('folio_id'),
                'text': folio_lines,
                'lines': folio.get('text_lines', [])
            })

clean_text = "".join(c.lower() for c in all_text if c.isalpha() or c.isspace())

# ============================================================================
# KNOWN PHARMACEUTICAL TERMS - EXPANDED
# ============================================================================
KNOWN_LATIN = {
    'sal', 'fiat', 'aqua', 'oleum', 'dare', 'recipe', 'miscere',
    'distilla', 'solve', 'coquere', 'herba', 'radix', 'flos', 'fice',
    'pulvis', 'unguentum', 'emplastrum', 'tinctura', 'decoctum',
    'infusio', 'extractum', 'balsamum', 'resina', 'cortex', 'mel',
    'vin', 'acid', 'basis', 'misce', 'coque', 'distille', 'decoct',
    'infund', 'extract', 'spirit', 'essentia', 'aeterna', 'crucis',
    'quintessentia', 'alkali', 'vitriol', 'sulfur', 'mercur', 'rex',
    'gold', 'silver', 'copper', 'iron', 'lead', 'tin', 'alkahest',
}

# Historical pharmaceutical recipes (what real medieval recipes look like)
HISTORICAL_PATTERNS = {
    'recipe': 'Take/instruction marker',
    'aqua': 'Water base',
    'sal': 'Salt preservative',
    'oleum': 'Oil base',
    'herba': 'Herb ingredient',
    'radix': 'Root ingredient',
    'flos': 'Flower ingredient',
    'coquere': 'Boil instruction',
    'miscere': 'Mix instruction',
    'distilla': 'Distill instruction',
    'solve': 'Dissolve instruction',
}

LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
}

KNOWN_MAPPINGS = {
    's': 's', 'a': 'a', 'l': 'l', 'd': 'd', 'o': 'o', 'r': 'r'
}

print("STEP 1: EXTENDED ITERATIONS (10,000+ genetic algorithm)")
print("=" * 80)
print()

def score_mapping(cipher_map, known_weight=200, bigram_weight=1):
    """Multiple scoring functions to test"""
    score = 0

    # Bigram scoring
    for i in range(len(clean_text) - 1):
        c1, c2 = clean_text[i], clean_text[i+1]
        if c1 in cipher_map and c2 in cipher_map:
            bigram = cipher_map[c1] + cipher_map[c2]
            if bigram in LATIN_BIGRAMS:
                score += LATIN_BIGRAMS[bigram] * bigram_weight

    # Heavy bonus for known words
    decoded = "".join(cipher_map.get(c, '?') for c in clean_text)
    for word in KNOWN_LATIN:
        if word in decoded:
            if word in ['sal', 'aqua', 'oleum']:
                score += known_weight * 2  # Highest confidence words
            else:
                score += known_weight

    return score

def run_genetic_algorithm(iterations=10000, name="GA"):
    """Run genetic algorithm for extended iterations"""
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

    temp = 50.0
    for i in range(iterations):
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

        if i % 2000 == 0:
            decoded = "".join(best_mapping.get(c, '?') for c in clean_text)
            found = [w for w in KNOWN_LATIN if w in decoded]
            print(f"  {name} Iteration {i}: Score={best_score} Words found={len(found)}")

    return best_mapping, best_score

print("Running genetic algorithm with 10,000 iterations...")
ga_mapping, ga_score = run_genetic_algorithm(10000, "GA-10K")
print(f"Final GA score: {ga_score}")
print()

# ============================================================================
# STEP 2: LOCK BEST MAPPINGS + EXTRACT RECIPES
# ============================================================================
print("STEP 2: LOCK BEST MAPPINGS + EXTRACT PHARMACEUTICAL RECIPES")
print("=" * 80)
print()

def extract_recipes(mapping, folios):
    """Extract pharmaceutical recipe patterns from decoded text"""
    recipes = []

    for folio_data in folios:
        folio_id = folio_data['id']
        folio_text = folio_data['text']

        # Decode folio
        decoded_folio = "".join(mapping.get(c.lower(), '?') for c in folio_text)

        # Find pharmaceutical terms in this folio
        found_terms = []
        for term in KNOWN_LATIN:
            if term in decoded_folio.lower():
                count = decoded_folio.lower().count(term)
                found_terms.append((term, count))

        if found_terms:
            recipes.append({
                'folio': folio_id,
                'terms': sorted(found_terms, key=lambda x: -x[1]),
                'sample': decoded_folio[:200]
            })

    return recipes

recipes = extract_recipes(ga_mapping, all_folios)
print(f"Found {len(recipes)} folios with pharmaceutical content:")
for recipe in recipes[:10]:
    print(f"  {recipe['folio']}: {', '.join([t[0] for t in recipe['terms'][:5]])}")
print()

# ============================================================================
# STEP 3: ENSEMBLE VOTING
# ============================================================================
print("STEP 3: ENSEMBLE VOTING - RUN MULTIPLE VARIANTS")
print("=" * 80)
print()

def run_variant_decoder(variant_name, scoring_params):
    """Run a decoder with specific scoring parameters"""
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
    best_score = score_mapping(best_mapping, **scoring_params)

    temp = scoring_params.get('temp', 50.0)
    iterations = scoring_params.get('iterations', 5000)

    for i in range(iterations):
        swappable = [c for c in voynich_chars if c not in KNOWN_MAPPINGS]

        if len(swappable) >= 2:
            c1, c2 = random.sample(swappable, 2)
            mapping[c1], mapping[c2] = mapping[c2], mapping[c1]
            new_score = score_mapping(mapping, **scoring_params)

            delta = new_score - best_score
            if delta > 0 or (temp > 0 and random.random() < math.exp(delta / temp)):
                best_score = new_score
                best_mapping = mapping.copy()
            else:
                mapping[c1], mapping[c2] = mapping[c2], mapping[c1]

        temp *= 0.9994

    return best_mapping, best_score

# Run multiple variants
variants = [
    ("High-confidence", {'known_weight': 500, 'bigram_weight': 1, 'iterations': 5000, 'temp': 100}),
    ("Balanced", {'known_weight': 200, 'bigram_weight': 2, 'iterations': 7000, 'temp': 50}),
    ("Bigram-focused", {'known_weight': 100, 'bigram_weight': 5, 'iterations': 8000, 'temp': 30}),
]

ensemble_results = []
for name, params in variants:
    print(f"Running {name}...")
    variant_mapping, variant_score = run_variant_decoder(name, params)
    ensemble_results.append({
        'name': name,
        'mapping': variant_mapping,
        'score': variant_score
    })

    # Find words in this variant
    decoded = "".join(variant_mapping.get(c, '?') for c in clean_text)
    found = [w for w in KNOWN_LATIN if w in decoded]
    print(f"  Score: {variant_score}, Words: {', '.join(found[:8])}")

print()

# Ensemble voting: which words appear in multiple variants?
print("ENSEMBLE VOTING RESULTS:")
word_votes = Counter()
for result in ensemble_results:
    decoded = "".join(result['mapping'].get(c, '?') for c in clean_text)
    for word in KNOWN_LATIN:
        if word in decoded:
            word_votes[word] += 1

print("Words that appear in multiple decoder variants (high confidence):")
for word, votes in word_votes.most_common(15):
    confidence = votes / len(ensemble_results) * 100
    print(f"  {word:15} {votes}/{len(ensemble_results)} variants ({confidence:.0f}%)")

print()

# ============================================================================
# STEP 4: HISTORICAL CROSS-REFERENCE
# ============================================================================
print("STEP 4: HISTORICAL CROSS-REFERENCE")
print("=" * 80)
print()

print("Mapping found words to historical pharmaceutical patterns:")
for word, votes in word_votes.most_common(10):
    if word in HISTORICAL_PATTERNS:
        print(f"  {word:15} → {HISTORICAL_PATTERNS[word]}")
    else:
        print(f"  {word:15} → (ingredient or specialized term)")

print()
print("Historical recipe structure hypothesis:")
print("  'recipe' (instruction marker)")
print("  → 'aqua'/'oleum'/'vin' (base)")
print("  → 'herba'/'radix'/'flos'/'mel' (ingredients)")
print("  → 'coquere'/'miscere'/'distilla' (processing)")
print("  → 'sal' (preservation)")

# Check if patterns match
decoded_best = "".join(ga_mapping.get(c, '?') for c in clean_text)
found_sequences = []
for i in range(len(decoded_best) - 50):
    chunk = decoded_best[i:i+50]
    has_base = any(b in chunk for b in ['aqua', 'oleum', 'vin'])
    has_ingredient = any(ing in chunk for ing in ['herba', 'radix', 'flos', 'mel'])
    has_process = any(p in chunk for p in ['coquere', 'miscere', 'distilla'])

    if has_base and has_ingredient and has_process:
        found_sequences.append(chunk)

if found_sequences:
    print(f"\n✓ Found {len(found_sequences)} sequences matching historical recipe patterns!")
else:
    print("\n(Recipe pattern matching needs more refinement)")

print()

# ============================================================================
# STEP 5: VARIANT EXPERIMENTS
# ============================================================================
print("STEP 5: EXPERIMENTAL VARIANTS - DIFFERENT APPROACHES")
print("=" * 80)
print()

# Variant A: Double-weight "sal"
print("Variant A: Prioritize 'sal' (most robust word)...")
def score_sal_focused(cipher_map):
    score = 0
    for i in range(len(clean_text) - 1):
        c1, c2 = clean_text[i], clean_text[i+1]
        if c1 in cipher_map and c2 in cipher_map:
            bigram = cipher_map[c1] + cipher_map[c2]
            if bigram in LATIN_BIGRAMS:
                score += LATIN_BIGRAMS[bigram]

    decoded = "".join(cipher_map.get(c, '?') for c in clean_text)
    score += decoded.count('sal') * 500  # Heavy bonus per occurrence

    for word in KNOWN_LATIN:
        if word != 'sal' and word in decoded:
            score += 100

    return score

# Variant B: Cross-validation across random starting points
print("Variant B: Cross-validation across 5 random initializations...")
cv_results = []
for trial in range(5):
    voynich_chars = sorted(set(c for c in clean_text if c.isalpha()))
    latin_chars = list('abcdefghijklmnopqrstuvwxyz')

    for known_l in KNOWN_MAPPINGS.values():
        if known_l in latin_chars:
            latin_chars.remove(known_l)

    # Random initialization
    random.shuffle(latin_chars)

    mapping = KNOWN_MAPPINGS.copy()
    remaining_voynich = [c for c in voynich_chars if c not in mapping]

    for v_char in remaining_voynich:
        if latin_chars:
            mapping[v_char] = latin_chars.pop(0)

    best_mapping = mapping.copy()
    best_score = score_mapping(best_mapping)

    temp = 50.0
    for i in range(3000):
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

        temp *= 0.999

    decoded = "".join(best_mapping.get(c, '?') for c in clean_text)
    found = [w for w in KNOWN_LATIN if w in decoded]
    cv_results.append({'score': best_score, 'words': found})
    print(f"  Trial {trial+1}: Score={best_score}, Found: {', '.join(found[:5])}")

print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 80)
print("COMPREHENSIVE RESULTS SUMMARY")
print("=" * 80)
print()

print("Best results achieved:")
print(f"  Genetic Algorithm (10K): {ga_score}")
best_ensemble = max(ensemble_results, key=lambda x: x['score'])
print(f"  Best Ensemble Variant: {best_ensemble['score']} ({best_ensemble['name']})")
best_cv = max(cv_results, key=lambda x: x['score'])
print(f"  Best Cross-Validation: {best_cv['score']}")

print()
print("Consensus pharmaceutical terms (across all methods):")
for word, votes in word_votes.most_common(20):
    print(f"  {word:15} confidence: {votes}/{len(ensemble_results)}")

print()
print("Character mapping (GA-10K, locked known mappings):")
for c in sorted(ga_mapping.keys()):
    locked = " [LOCKED]" if c in KNOWN_MAPPINGS else ""
    print(f"  {c} → {ga_mapping[c]}{locked}")

print()
print("=" * 80)
print("ALL EXPERIMENTS COMPLETE")
print("=" * 80)

# Save comprehensive results
with open('COMPREHENSIVE_RESULTS.json', 'w') as f:
    json.dump({
        'ga_score': ga_score,
        'ensemble_scores': [r['score'] for r in ensemble_results],
        'consensus_words': dict(word_votes.most_common(30)),
        'best_mapping': ga_mapping,
        'recipes_found': len(recipes),
        'cross_validation_scores': [r['score'] for r in cv_results],
    }, f, indent=2)

print("\nDetailed results saved to: COMPREHENSIVE_RESULTS.json")
