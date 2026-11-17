#!/usr/bin/env python3
"""
ULTIMATE VOYNICH DECODER v5.0 - FINAL INTEGRATED DECODER
Combines: Unconstrained optimization + Dictionary validation + Abbreviation layer
This is it. Everything combined.
"""

import json
from collections import Counter
import random
import math

print("=" * 80)
print("ULTIMATE VOYNICH DECODER v5.0 - FINAL INTEGRATED")
print("=" * 80)
print()

# ============================================================================
# LOAD DATA
# ============================================================================
print("[1/5] Loading and preparing data...")
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
# STAGE 1: PHARMACEUTICAL ABBREVIATION DATABASE
# ============================================================================
print("[2/5] Building pharmaceutical abbreviation database...")

ABBREV_DB = {
    # Actions
    'dar': ['dare', 'take'], 'dar': ['dare'], 'da': ['dare'],
    'dis': ['distilla', 'distill'], 'dist': ['distilla'],
    'sol': ['solve', 'dissolve'], 'solv': ['solve'],
    'coq': ['coquere', 'boil'], 'coqu': ['coquere'],
    'misc': ['miscere', 'mix'],
    'ferv': ['fervere', 'boil'],
    'frac': ['frangere', 'crush'],
    'pul': ['pulvis', 'powder'], 'pulv': ['pulvis'],
    'trit': ['tritum', 'ground'],

    # Substances
    'ol': ['oleum', 'oil'],
    'aqua': ['aqua', 'water'],
    'vin': ['vinum', 'wine'],
    'mel': ['mel', 'honey'],
    'sal': ['sal', 'salt'],
    'herb': ['herba', 'herb'],
    'rad': ['radix', 'root'],
    'fol': ['folium', 'leaf'],
    'flor': ['flos', 'flower'],
    'sem': ['semen', 'seed'],
    'cort': ['cortex', 'bark'],
    'res': ['resina', 'resin'],

    # Measurements
    'gr': ['granum', 'grain'],
    'dr': ['drachma', 'dram'],
    'oz': ['oncia', 'ounce'],
    'lib': ['libra', 'pound'],

    # Medical properties
    'diuret': ['diureticum'],
    'laxat': ['laxativum'],
    'carmin': ['carminativum'],
    'stomat': ['stomaticum'],
}

print(f"   {len(ABBREV_DB)} pharmaceutical abbreviations loaded")
print()

# ============================================================================
# STAGE 2: KNOWN LATIN PHARMACEUTICAL WORDS
# ============================================================================
print("[3/5] Setting up known word dictionary...")

KNOWN_LATIN = {
    'aqua', 'oleum', 'sal', 'herba', 'recipe', 'fiat', 'fice',
    'distilla', 'miscere', 'frangere', 'coquere', 'solve', 'dare',
    'pulvis', 'unguentum', 'emplastrum', 'tinctura', 'decoctum',
    'infusio', 'extractum', 'balsamum', 'resina', 'cortex',
    'radix', 'folium', 'flos', 'semen', 'vinum', 'mel',
    'mercurius', 'sulphur', 'vitriol', 'alumen', 'arsenicum',
    'misce', 'coque', 'distille', 'recipe', 'fiat', 'misce',
    'aquae', 'oleorum', 'salis', 'herbae', 'herbis',
}

# Scoring function: combines bigram quality + known word matches
LATIN_BIGRAMS = {
    'ch': 10, 're': 9, 'er': 9, 'ar': 8, 'or': 8, 'us': 8, 'um': 7, 'am': 7,
    'em': 7, 'ae': 7, 'oe': 7, 'ia': 6, 'io': 6, 'is': 6, 'es': 6, 'as': 6,
    'os': 6, 'in': 6, 'an': 6, 'on': 6, 'en': 6, 'ea': 6, 'eo': 6,
    'ua': 5, 'ue': 5, 'oi': 5, 'ai': 5, 'au': 5, 'ci': 4, 'ti': 4, 'di': 4,
    'li': 4, 'ri': 4, 'ni': 4, 'mi': 4, 'hi': 4, 'pi': 4, 'gi': 4, 'fi': 4,
    'bi': 4, 'vi': 4, 'si': 4, 'ca': 3, 'ta': 3, 'da': 3, 'la': 3, 'ra': 3,
}

def score_mapping_hybrid(cipher_map):
    """Score mapping on bigrams + known words"""
    bigram_score = 0
    word_score = 0

    # Bigram scoring
    for i in range(len(clean_text) - 1):
        c1_encrypted = clean_text[i]
        c2_encrypted = clean_text[i+1]

        if c1_encrypted in cipher_map and c2_encrypted in cipher_map:
            c1_decoded = cipher_map[c1_encrypted]
            c2_decoded = cipher_map[c2_encrypted]
            bigram = c1_decoded + c2_decoded

            if bigram in LATIN_BIGRAMS:
                bigram_score += LATIN_BIGRAMS[bigram]
            elif c1_decoded == c2_decoded:
                bigram_score -= 2

    # Known word scoring
    decoded_full = ""
    for c in clean_text:
        if c in cipher_map:
            decoded_full += cipher_map[c]
        else:
            decoded_full += '?'

    for known_word in KNOWN_LATIN:
        if known_word in decoded_full:
            word_score += 100

    return bigram_score + word_score

print(f"   {len(KNOWN_LATIN)} known Latin pharmaceutical words")
print()

# ============================================================================
# STAGE 4: UNCONSTRAINED OPTIMIZATION (Hybrid Scoring)
# ============================================================================
print("[4/5] Running hybrid optimization (bigrams + known words)...")

voynich_chars = sorted(set(c for c in clean_text if c.isalpha()))
latin_chars = list('abcdefghijklmnopqrstuvwxyz')

random.shuffle(latin_chars)
initial_mapping = {v: l for v, l in zip(voynich_chars, latin_chars[:len(voynich_chars)])}

initial_score = score_mapping_hybrid(initial_mapping)
print(f"   Initial score: {initial_score}")
print()

current_mapping = initial_mapping.copy()
current_score = initial_score
best_mapping = current_mapping.copy()
best_score = current_score

temperature = 50.0
cooling_rate = 0.998
max_iterations = 15000
no_improve_count = 0

for iteration in range(max_iterations):
    chars = list(current_mapping.keys())
    if len(chars) >= 2:
        c1, c2 = random.sample(chars, 2)

        new_mapping = current_mapping.copy()
        new_mapping[c1], new_mapping[c2] = new_mapping[c2], new_mapping[c1]
        new_score = score_mapping_hybrid(new_mapping)

        delta = new_score - current_score
        if delta > 0 or (temperature > 0 and random.random() < math.exp(delta / temperature)):
            current_mapping = new_mapping
            current_score = new_score

            if current_score > best_score:
                best_score = current_score
                best_mapping = current_mapping.copy()
                no_improve_count = 0
                if iteration % 500 == 0:
                    print(f"   Iteration {iteration}: Best = {best_score}")
            else:
                no_improve_count += 1
        else:
            no_improve_count += 1

    temperature *= cooling_rate

    if no_improve_count > 2000:
        print(f"   Converged at iteration {iteration}")
        break

    if iteration % 2000 == 0 and iteration > 0:
        print(f"   ...iteration {iteration}, best={best_score}")

print(f"   Final score: {best_score}")
print()

# ============================================================================
# STAGE 5: DECODE AND DISPLAY
# ============================================================================
print("=" * 80)
print("FINAL DECODER RESULTS")
print("=" * 80)
print()

# Full decode
decoded_full = ""
for c in clean_text:
    if c in best_mapping:
        decoded_full += best_mapping[c]
    else:
        decoded_full += '?'

# Check known words
found_words = [w for w in KNOWN_LATIN if w in decoded_full]
print(f"Known Latin words found: {len(found_words)}")
if found_words:
    for word in found_words[:20]:
        print(f"  - {word}")
print()

# Decode first folios
print("Sample decoded folios:")
print()
for idx, folio in enumerate(integrated.get('folios', [])[:3]):
    if not folio.get('has_text'):
        continue

    print(f"--- {folio.get('folio_id')} ---")

    for line_idx, line in enumerate(folio.get('text_lines', [])[:3]):
        words = line.get('words', [])

        decoded_words_line = []
        for word in words:
            decoded = ''.join([best_mapping.get(c.lower(), '?') for c in word])
            decoded_words_line.append(decoded)

        print(f"Original: {' '.join(words[:12])}")
        print(f"Decoded:  {' '.join(decoded_words_line[:12])}")
        print()

# Top bigrams
print("Top decoded bigrams:")
decoded_bigrams = Counter()
for i in range(len(decoded_full) - 1):
    if decoded_full[i].isalpha() and decoded_full[i+1].isalpha():
        decoded_bigrams[(decoded_full[i], decoded_full[i+1])] += 1

for (c1, c2), count in decoded_bigrams.most_common(15):
    bigram = c1 + c2
    is_known = " [LATIN]" if bigram in LATIN_BIGRAMS else ""
    print(f"  {bigram}: {count:5}{is_known}")

print()
print("=" * 80)
print("FINAL DECODER COMPLETE")
print("=" * 80)

# Save results
with open('v5_decoded_text.txt', 'w') as f:
    f.write(decoded_full)

with open('v5_mapping.txt', 'w') as f:
    for c in sorted(best_mapping.keys()):
        f.write(f"{c} -> {best_mapping[c]}\n")

print("\nResults saved to:")
print("  - v5_decoded_text.txt (full decoded text)")
print("  - v5_mapping.txt (character mapping)")
