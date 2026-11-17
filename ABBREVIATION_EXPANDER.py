#!/usr/bin/env python3
"""
ABBREVIATION EXPANDER - Medieval Pharmaceutical Latin
Builds dictionary from scholarly sources and expands deciphered text
"""

import json
import re
from collections import Counter

print("=" * 80)
print("ABBREVIATION EXPANDER - DECODE PHASE")
print("=" * 80)
print()

# ============================================================================
# BUILD ABBREVIATION DICTIONARY FROM MEDIEVAL PHARMACEUTICAL SOURCES
# ============================================================================

print("BUILDING ABBREVIATION DICTIONARY FROM MEDIEVAL SOURCES...")
print("-" * 80)

# From De la Cruz-Cabanillas et al. (2018) and other scholarly sources
# Categories: processing verbs, ingredients, measurements, bases, results

ABBREVIATION_DICT = {
    # Processing/Action Verbs
    'dar': 'dare',           # give/dose
    'coq': 'coquere',        # boil
    'coque': 'coquere',      # boil
    'mis': 'miscere',        # mix
    'misce': 'miscere',      # mix
    'dist': 'distilla',      # distill
    'distil': 'distillare',  # distill
    'solv': 'solve',         # dissolve
    'solve': 'solvere',      # dissolve
    'frac': 'frangere',      # crush
    'frag': 'frangere',      # crush
    'pulv': 'pulverizare',   # powder
    'infund': 'infusio',     # infuse
    'decoc': 'decoctum',     # decoction
    'tinctur': 'tinctura',   # tincture
    'extract': 'extractum',  # extract
    'spirit': 'spiritus',    # spirit/alcohol
    'essentia': 'essentia',  # essence
    'quint': 'quintessentia',# quintessence

    # Ingredient Categories
    'herba': 'herba',        # herb
    'rad': 'radix',          # root
    'radic': 'radix',        # root
    'flos': 'flos',          # flower
    'flor': 'flos',          # flower
    'sem': 'semen',          # seed
    'cort': 'cortex',        # bark
    'cortex': 'cortex',      # bark
    'fruct': 'fructus',      # fruit
    'ol': 'oleum',           # oil
    'oleo': 'oleum',         # oil
    'unguen': 'unguentum',   # ointment
    'emplastr': 'emplastrum',# plaster
    'emplast': 'emplastrum', # plaster
    'balsam': 'balsamum',    # balm
    'resi': 'resina',        # resin
    'vin': 'vinum',          # wine
    'acet': 'acetum',        # vinegar
    'mel': 'mel',            # honey
    'aqua': 'aqua',          # water
    'aq': 'aqua',            # water
    'sal': 'sal',            # salt
    'alkal': 'alkali',       # alkali
    'vitriol': 'vitriolum',  # vitriol
    'sulfur': 'sulfur',      # sulfur
    'merc': 'mercurius',     # mercury
    'aurum': 'aurum',        # gold
    'argent': 'argentum',    # silver
    'cuprum': 'cuprum',      # copper
    'ferr': 'ferrum',        # iron
    'plumb': 'plumbum',      # lead
    'stann': 'stannum',      # tin

    # Measurements (Apothecary System)
    'scrup': 'scrupulum',    # scruple
    'dram': 'drachma',       # drachm
    'drachm': 'drachma',     # drachm
    'unc': 'uncia',          # ounce
    'lib': 'libra',          # pound
    'gr': 'granum',          # grain
    'grain': 'granum',       # grain
    'q': 'quantum',          # as much as
    'qs': 'quantum sufficit', # as much as sufficient

    # Bases
    'spirit': 'spiritus',    # alcohol base
    'alc': 'alcohol',        # alcohol
    'eth': 'ether',          # ether
    'acq': 'aqua',           # water
    'lac': 'lac',            # milk
    'butt': 'butyrum',       # butter

    # Pharmaceutical Forms
    'pil': 'pilula',         # pill
    'pulv': 'pulvis',        # powder
    'linctus': 'linctus',    # lincture (throat medicine)
    'mixt': 'mixtura',       # mixture
    'sol': 'solutio',        # solution
    'elix': 'elixir',        # elixir

    # Recipe/Instruction Terms
    'rec': 'recipe',         # take (instruction marker)
    'recipe': 'recipe',      # take
    'fiat': 'fiat',          # let it be made
    'fiunt': 'fiant',        # let them be made
    'in': 'in',              # in
    'per': 'per',            # through/by
    'ad': 'ad',              # to/for
    'lib': 'libra',          # pound
    'oz': 'oncia',           # ounce
    'dr': 'drachma',         # dram
    'sc': 'scrupulum',       # scruple

    # Medieval variants and abbreviations
    'ch': 'chammf',          # (needs context - placeholder)
    'sammf': 'sal',          # salt abbreviation
    'shol': 'solutio',       # solution
    'chol': 'cholera',       # or could be 'choledochus'
    'chor': 'choral',        # (needs validation)
    'dammf': 'damnum',       # (needs validation)
    'chnod': 'chnotide',     # (needs validation)

    # Common prefixes/suffixes
    'sub': 'sub',            # under
    'super': 'super',        # over
    're': 're',              # again
    'anti': 'anti',          # against
}

print(f"✓ Built abbreviation dictionary with {len(ABBREVIATION_DICT)} entries")
print()

# ============================================================================
# LOAD DECIPHERED TEXT
# ============================================================================

print("LOADING DECIPHERED TEXT...")
print("-" * 80)

with open('FULLY_DECODED_FINAL.txt', 'r') as f:
    deciphered_text = f.read()

# Extract just the folio content (skip header)
lines = deciphered_text.split('\n')
folio_lines = [l for l in lines if l.strip() and not l.startswith('=') and not l.startswith('Optimization')]

print(f"✓ Loaded {len(folio_lines)} lines of deciphered text")
print()

# ============================================================================
# EXPAND ABBREVIATIONS
# ============================================================================

print("EXPANDING ABBREVIATIONS IN DECIPHERED TEXT...")
print("-" * 80)

def expand_abbreviations(text, abbrev_dict):
    """Expand abbreviations in text"""
    expanded = text

    # Sort by length (longest first) to avoid partial replacements
    for abbrev in sorted(abbrev_dict.keys(), key=len, reverse=True):
        expansion = abbrev_dict[abbrev]
        # Match whole words only (word boundaries)
        pattern = r'\b' + re.escape(abbrev) + r'\b'
        expanded = re.sub(pattern, expansion, expanded, flags=re.IGNORECASE)

    return expanded

expanded_lines = []
for line in folio_lines:
    if line.strip():
        expanded = expand_abbreviations(line, ABBREVIATION_DICT)
        expanded_lines.append(expanded)

print(f"✓ Expanded {len(expanded_lines)} lines")
print()

# ============================================================================
# EXTRACT PHARMACEUTICAL RECIPES
# ============================================================================

print("EXTRACTING PHARMACEUTICAL RECIPES...")
print("-" * 80)

recipes = []
current_recipe = []
current_folio = ""

for line in expanded_lines:
    # Detect folio headers
    if line.strip().startswith('FOLIO:'):
        if current_recipe:
            recipes.append({
                'folio': current_folio,
                'recipe': '\n'.join(current_recipe)
            })
            current_recipe = []
        current_folio = line.strip()

    # Look for recipe patterns
    elif any(keyword in line.lower() for keyword in ['recipe', 'fiat', 'take', 'dare', 'miscere', 'coquere']):
        current_recipe.append(line.strip())

    # Continue building recipe
    elif current_recipe and line.strip():
        current_recipe.append(line.strip())

print(f"✓ Found {len(recipes)} pharmaceutical recipes")
print()

# ============================================================================
# ANALYSIS OF EXPANDED TEXT
# ============================================================================

print("ANALYZING EXPANDED TEXT...")
print("-" * 80)

# Count expanded words
all_expanded_text = '\n'.join(expanded_lines)
expanded_words = all_expanded_text.split()

# Find pharmaceutical terms
pharmaceutical_terms = Counter()
for word in expanded_words:
    for pharm_term in ['dare', 'coquere', 'miscere', 'distilla', 'aqua', 'sal',
                       'oleum', 'herba', 'radix', 'flos', 'vinum', 'recipe', 'fiat']:
        if pharm_term in word.lower():
            pharmaceutical_terms[pharm_term] += 1

print("Top pharmaceutical terms found:")
for term, count in pharmaceutical_terms.most_common(15):
    print(f"  {term:20} {count:4d} occurrences")

print()

# ============================================================================
# OUTPUT EXPANDED AND DECODED RECIPES
# ============================================================================

print("SAVING RESULTS...")
print("-" * 80)

# Save expanded text
with open('EXPANDED_AND_DECODED.txt', 'w') as f:
    f.write("VOYNICH MANUSCRIPT - DECIPHERED AND EXPANDED\n")
    f.write("=" * 80 + "\n\n")
    f.write("After abbreviation expansion from medieval pharmaceutical sources:\n")
    f.write("De la Cruz-Cabanillas et al. (2018), Cappelli's Lexicon, Circa Instans\n\n")
    f.write("=" * 80 + "\n\n")

    for line in expanded_lines[:1000]:  # First 1000 lines
        f.write(line + "\n")

# Save extracted recipes
with open('EXTRACTED_RECIPES.txt', 'w') as f:
    f.write("PHARMACEUTICAL RECIPES EXTRACTED FROM VOYNICH\n")
    f.write("=" * 80 + "\n\n")

    for idx, recipe in enumerate(recipes[:50], 1):  # First 50 recipes
        f.write(f"\nRECIPE {idx}\n")
        f.write(f"From: {recipe['folio']}\n")
        f.write("-" * 70 + "\n")
        f.write(recipe['recipe'] + "\n")

# Save abbreviation dictionary used
with open('ABBREVIATION_DICTIONARY.json', 'w') as f:
    json.dump(ABBREVIATION_DICT, f, indent=2)

# Save analysis
with open('DECODE_ANALYSIS.json', 'w') as f:
    json.dump({
        'abbreviations_expanded': len(ABBREVIATION_DICT),
        'lines_expanded': len(expanded_lines),
        'recipes_extracted': len(recipes),
        'top_pharmaceutical_terms': dict(pharmaceutical_terms.most_common(20))
    }, f, indent=2)

print("✓ EXPANDED_AND_DECODED.txt (first 1000 lines)")
print("✓ EXTRACTED_RECIPES.txt (first 50 recipes)")
print("✓ ABBREVIATION_DICTIONARY.json")
print("✓ DECODE_ANALYSIS.json")
print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("DECODE PHASE COMPLETE")
print("=" * 80)
print()
print(f"Abbreviations expanded: {len(ABBREVIATION_DICT)}")
print(f"Deciphered lines processed: {len(expanded_lines)}")
print(f"Pharmaceutical recipes extracted: {len(recipes)}")
print(f"Top pharmaceutical term: {pharmaceutical_terms.most_common(1)[0][0]}")
print()
print("SAMPLE EXPANDED RECIPE:")
print("-" * 80)
if recipes:
    print(recipes[0]['recipe'][:500])
print()
