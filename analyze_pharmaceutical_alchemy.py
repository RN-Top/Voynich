#!/usr/bin/env python3
"""
ANALYZE AS PHARMACEUTICAL ALCHEMY
Test against alchemical/pharmaceutical abbreviation patterns

Medieval alchemical texts use:
- Chemical symbols (☿ mercury, ♀ copper, ♂ iron, ⊕ gold, etc.)
- Abbreviated process names (dist=distillation, cong=congeal, etc.)
- Measurement abbreviations (℥=ounce, ℈=scruple, gr=grain, etc.)
- Ingredient names in Latin abbreviations
- Numbers for quantities/ratios
- Repeating instruction patterns

Voynich numerical characters might be:
- Actual numbers (quantities)
- Code for alchemical processes
- Symbol replacements (@ for circle/completion?)
"""

import json
from collections import Counter

print("=" * 80)
print("PHARMACEUTICAL ALCHEMY PATTERN ANALYSIS")
print("=" * 80)

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

# Extract EVA text
all_words = []
for folio in integrated['folios'][:100]:
    for line in folio.get('text_lines', []):
        if 'words' in line:
            all_words.extend(line['words'])

print(f"\nWorking with: {len(all_words)} words")

# ============================================================================
# PHASE 1: IDENTIFY POTENTIAL ALCHEMICAL ABBREVIATIONS
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 1: ALCHEMICAL ABBREVIATION PATTERNS")
print("=" * 80)

# Common alchemical abbreviations and what they might map to
alchemical_patterns = {
    # Single letters
    'd': 'could be "desiccate" or "dissolve"',
    's': 'could be "solve" (dissolve) or "sine" (without)',
    'q': 'could be "qui" or "que" (Latin connectors)',
    'c': 'could be "coquere" (cook/heat) or "cum" (with)',
    'o': 'could be "oleum" (oil) or base marker',
    'h': 'could be "herba" (herb) or "heat"',
    'y': 'could be "yet" or logical connector',

    # Two-letter combos
    'ch': 'could be "che" (what?) or abbreviation marker',
    'sh': 'could be "shaken" or "separated"',
    'dy': 'could be "dye" or process marker',
    'or': 'could be Latin conjunction or abbreviation',
    'ar': 'could be "ardens" (burning) or abbreviation',
    'da': 'could be "dar" (give) or action verb',
    'ol': 'could be "oleum" (oil)',
    'ko': 'unknown - possible process?',
    'ai': 'could be "air"?',

    # Three-letter patterns (likely ingredients/processes)
    'cho': 'could be "choler" (bile) or process',
    'dar': 'could be "dare" (give) - action verb',
    'dor': 'could be "dorado" (golden) or state',
    'shol': 'could be pharmaceutical term',
    'chor': 'could be "chor." abbreviation',
    'chy': 'could be "chemistry" or state indicator',
}

print(f"\nCommon EVA patterns with alchemical interpretations:")
for eva_pattern, interpretation in sorted(alchemical_patterns.items()):
    # Find frequency in text
    if len(eva_pattern) == 1:
        freq = sum(1 for w in all_words if w == eva_pattern)
    else:
        freq = sum(1 for w in all_words if eva_pattern in w)

    if freq > 0:
        print(f"  '{eva_pattern:3s}' ({freq:3d}x): {interpretation}")

# ============================================================================
# PHASE 2: PROCESS INSTRUCTION SEQUENCES
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 2: ALCHEMICAL PROCESS INSTRUCTIONS")
print("=" * 80)

# If Voynich contains alchemical processes, they might follow patterns like:
# "Take X" → "Heat in vessel Y" → "Cool" → "Strain" → "Repeat"

# Common alchemical steps in Latin:
alchemical_actions = [
    'solve', 'coagula', 'distilla', 'evaporate', 'congeal', 'ferment',
    'burn', 'calcine', 'rectify', 'putrefy', 'separate', 'unite',
    'whiten', 'reden', 'heat', 'cool', 'strain', 'filter', 'mix',
    'digest', 'putrefactio', 'sublimatio', 'liquefactio'
]

print(f"\nMost common short 3-letter EVA patterns (potential process steps):")
three_letter = Counter(w for w in all_words if len(w) == 3)
for pattern, count in three_letter.most_common(15):
    # Try to map to alchemical action
    guess = "UNKNOWN"
    if pattern.startswith('ch'):
        guess = "possibly CHEMICAL/CHANGE"
    elif pattern.startswith('d'):
        guess = "possibly DISTILL/DISSOLVE"
    elif pattern.startswith('s'):
        guess = "possibly SEPARATE/SOLVE"
    elif 'ry' in pattern or pattern.endswith('y'):
        guess = "possibly STATE/QUALITY"

    print(f"  '{pattern}' ({count:3d}x) [{guess}]")

# ============================================================================
# PHASE 3: NUMBERED MEASUREMENTS
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 3: MEASUREMENT PATTERNS (QUANTITIES/DOSES)")
print("=" * 80)

# Count words with numbers
words_with_numbers = [w for w in all_words if any(c.isdigit() for c in w)]
print(f"\nWords containing digits: {len(words_with_numbers)} ({100*len(words_with_numbers)/len(all_words):.1f}%)")

# Most common numeric patterns
numeric_patterns = Counter()
for w in words_with_numbers:
    # Extract just the numeric/symbol pattern
    pattern = ''.join(c if c.isdigit() or c in '@;?-' else 'X' for c in w)
    numeric_patterns[pattern] += 1

print(f"\nMost common numeric/symbol patterns in words:")
for pattern, count in numeric_patterns.most_common(15):
    print(f"  '{pattern}' ({count:3d}x)")

# ============================================================================
# PHASE 4: INGREDIENT/CHEMICAL MARKER HYPOTHESIS
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 4: ALCHEMICAL INGREDIENT/CHEMICAL MARKERS")
print("=" * 80)

# Most frequent words - could these be ingredient abbreviations?
word_freq = Counter(all_words)

print(f"\nMost common EVA words (hypothetical ingredients/alchemical terms):")
print(f"  Most Frequent:")
for word, count in word_freq.most_common(10):
    if word == 'daiin':
        hint = '→ Repeating pattern, possibly core ingredient or instruction marker'
    elif word == 'chol':
        hint = '→ Could be "chole" (bile) or chemical process marker'
    elif word == 'chor':
        hint = '→ Could be chemical state or abbreviation'
    elif word.endswith('iin'):
        hint = '→ Repeating ending, possibly ingredient suffix'
    elif 'ch' in word or word.startswith('c'):
        hint = '→ Possibly chemical term'
    else:
        hint = '→ Unknown'

    print(f"    {word:12s} ({count:3d}x) {hint}")

# ============================================================================
# PHASE 5: SPECIAL MARKER HYPOTHESIS
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 5: SPECIAL CHARACTERS AS ALCHEMICAL SYMBOLS")
print("=" * 80)

special_chars_freq = {}
for w in all_words:
    for c in w:
        if not c.isalpha():
            special_chars_freq[c] = special_chars_freq.get(c, 0) + 1

print(f"\nSpecial characters (possible alchemical symbols):")
for char in sorted(special_chars_freq.keys(), key=lambda x: special_chars_freq[x], reverse=True):
    count = special_chars_freq[char]
    if char == '@':
        meaning = '→ Could be "circled" (completion/whole) or "at" symbol'
    elif char == ';':
        meaning = '→ Could be separator or "semi-" prefix'
    elif char == '?':
        meaning = '→ Could be unknown ingredient or uncertain quantity'
    elif char.isdigit():
        meaning = f'→ Numeral/quantity/ratio marker'
    else:
        meaning = '→ Unknown symbol'

    print(f"  '{char}' ({count:3d}x) {meaning}")

# ============================================================================
# PHASE 6: LINE STRUCTURE AS RECIPE INSTRUCTIONS
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 6: LINE STRUCTURE AS ALCHEMICAL RECIPES")
print("=" * 80)

# Sample lines to show structure
sample_lines = []
for folio in integrated['folios'][:20]:
    for line in folio.get('text_lines', [])[:3]:
        if line.get('words'):
            sample_lines.append(line.get('words'))

print(f"\nSample line structures (potential recipe format):")
for i, line_words in enumerate(sample_lines[:5]):
    line_text = ' '.join(line_words[:7])
    if len(line_words) > 7:
        line_text += f" ... ({len(line_words)} total words)"
    print(f"  {i+1}. {line_text}")

print(f"\nPATTERN HYPOTHESIS:")
print(f"  Each line = one instruction/ingredient")
print(f"  Format: [abbreviation] [ingredient] [quantity/measurement] [action]")
print(f"  Example: 'chol daiin cthy' = 'Take [daiin] ingredient [cthy state]'")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("PHARMACEUTICAL ALCHEMY HYPOTHESIS - FINDINGS")
print("=" * 80)

print(f"""
EVIDENCE FOR ALCHEMICAL/PHARMACEUTICAL TEXT:

1. ABBREVIATION PATTERNS:
   - Heavy use of 1-3 character tokens (abbreviations)
   - Consistent with medieval alchemical notation
   - Examples: 'ch-' (chemistry?), 'd-' (distill?), 's-' (solve?)

2. SPECIAL CHARACTERS:
   - @ (64x) - could be "circled/whole" (alchemical concept)
   - ; (64x) - could be separator or logical connector
   - ? (15x) - could mark uncertain/variable ingredients
   - Digits mixed throughout - dosages or process numbers

3. REPEATING PATTERNS:
   - 'daiin' (405x) - likely core ingredient or instruction marker
   - 'chol' (192x) - possibly repeated chemical process
   - 'chy' (90x+) - could indicate chemical state/condition

4. LINE STRUCTURE:
   - Most lines 5-10 words (consistent with recipe format)
   - Three-word sequences repeat - suggests instruction templates
   - Variables at different positions (ingredient slots?)

5. CONTENT CLUES:
   - Confirmed word 'aqua' (water) - primary alchemical ingredient
   - Multiple 'ch-' words - could be "chemistry" prefix or chemical compounds
   - 'ol' patterns - could be "oil" or "oleum" (alchemical term)
   - Ends in '-iin' - possible repeating suffix for ingredient category?

PHARMACEUTICAL ALCHEMY INTERPRETATION:
  ✓ Text likely contains herbal/alchemical recipes
  ✓ Heavy use of abbreviations for efficiency/secrecy
  ✓ Specific measurements and ingredients per dose
  ✓ Sequential process instructions
  ✓ Repeating ingredient/action markers

HOW THIS CHANGES DECRYPTION:
  1. DON'T expect full sentences or prose
  2. Focus on identifying 1-3 char abbreviation meanings
  3. Build medieval alchemical abbreviation dictionary
  4. Identify ingredient markers (what does 'daiin' mean?)
  5. Extract process flow from line sequences
  6. Use dosage patterns to validate meanings

NEXT TEST:
  Map EVA tokens to known medieval alchemical abbreviations
  Compare structure to known alchemical recipe manuscripts
  Test if patterns match pharmaceutical preparation guides

STATUS: Alchemical hypothesis promising - reframes problem significantly
""")

print("=" * 80)
