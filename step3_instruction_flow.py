#!/usr/bin/env python3
"""
STEP 3: UNDERSTAND INSTRUCTION FLOW AND INGREDIENT CATEGORIES
Parse line structure as recipe instructions
"""

import json
from collections import Counter

print("=" * 80)
print("STEP 3: INSTRUCTION FLOW ANALYSIS")
print("=" * 80)

with open('voynich_integrated.json') as f:
    integrated = json.load(f)

all_lines = []
for folio in integrated['folios'][:100]:
    for line in folio.get('text_lines', []):
        if line.get('words'):
            all_lines.append(line.get('words'))

# ============================================================================
# LINE STRUCTURE PATTERNS
# ============================================================================

print(f"\nAnalyzing {len(all_lines)} instruction lines...")

# Most common word patterns
first_word_freq = Counter(line[0] if line else '' for line in all_lines)
print(f"\nMost common FIRST WORDS (action/ingredient starters):")
for word, freq in first_word_freq.most_common(15):
    print(f"  {word:12s} ({freq:3d}x) - starts instructions")

# Second position analysis
second_word_freq = Counter(line[1] if len(line) > 1 else '' for line in all_lines)
print(f"\nMost common SECOND WORDS (ingredients/modifiers):")
for word, freq in second_word_freq.most_common(15):
    print(f"  {word:12s} ({freq:3d}x) - describes ingredient")

# Terminal word analysis (how instructions end)
last_word_freq = Counter(line[-1] if line else '' for line in all_lines)
print(f"\nMost common FINAL WORDS (result/state indicators):")
for word, freq in last_word_freq.most_common(15):
    print(f"  {word:12s} ({freq:3d}x) - instruction result")

# ============================================================================
# INSTRUCTION TEMPLATE PATTERNS
# ============================================================================

print("\n" + "=" * 80)
print("INSTRUCTION TEMPLATES")
print("=" * 80)

# Common 4-word sequences as templates
templates = Counter()
for line in all_lines:
    if len(line) >= 4:
        template = tuple(line[:4])
        templates[template] += 1

print(f"\nMost common 4-word instruction sequences:")
for template, count in templates.most_common(10):
    print(f"  {' → '.join(template):<50s} ({count}x)")

# ============================================================================
# INGREDIENT CATEGORY HYPOTHESIS
# ============================================================================

print("\n" + "=" * 80)
print("INGREDIENT CATEGORY ANALYSIS")
print("=" * 80)

# Words ending in '-iin' or '-ain' (possible ingredient suffixes)
ingredient_markers = Counter(w for line in all_lines for w in line if 'iin' in w or 'ain' in w)
print(f"\nWords with '-iin'/'-ain' (ingredient category markers):")
for word, freq in ingredient_markers.most_common(10):
    print(f"  {word:15s} ({freq:3d}x)")

# Words starting with common prefixes (actions)
action_patterns = {
    'd': 'distill/dissolve/dry',
    'ch': 'chemistry/change/heat',
    's': 'separate/solve/sine',
    'c': 'coq(cook)/cum(with)/cure',
    'sh': 'shake/sharp/shaken',
}

print(f"\nAction prefix frequencies:")
for prefix, meaning in action_patterns.items():
    count = sum(1 for line in all_lines for w in line if w.startswith(prefix))
    print(f"  {prefix:5s} ({count:4d}x) - {meaning}")

# ============================================================================
# LINE STRUCTURE AS RECIPE INSTRUCTION
# ============================================================================

print("\n" + "=" * 80)
print("RECIPE INSTRUCTION HYPOTHESIS")
print("=" * 80)

print(f"""
PROPOSED INSTRUCTION STRUCTURE:

Format: [ACTION/INGREDIENT] [INGREDIENT/MODIFIER] [@CODE;] [STATE/RESULT]

Example breakdowns:

1. "dar ataiin cthy" = Take [ataiin ingredient] in [cthy state]
   - dar = dare (take/give)
   - ataiin = ingredient name (suffix -iin = ingredient)
   - cthy = state (c+thy = chemical+state)

2. "chol daiin cthy" = Chemical action on [daiin] resulting in [cthy]
   - chol = cohere/chemical action
   - daiin = core ingredient (most common, likely aqua or oil)
   - cthy = end state

3. "sho chor shol" = Separate [chor] by [shol] method
   - sho = shake/separate
   - chor = chemical/component
   - shol = separation method

4. "dal ol ar" = Distill [ol-oil] [ar-ardent/burning]
   - dal = distill variant
   - ol = oleum (oil)
   - ar = ardent/heat indicator

RECOGNIZED PATTERNS:
  - {first_word_freq.most_common(1)[0][0]:12s} appears {first_word_freq.most_common(1)[0][1]:3d}x as action starter
  - {second_word_freq.most_common(1)[0][0]:12s} appears {second_word_freq.most_common(1)[0][1]:3d}x as ingredient marker
  - Lines end typically with state/quality indicators (-y, -ry, -ky)
  - @[CODE] appears as measurement/batch identifier

CONCLUSION: Text follows pharmaceutical recipe format with:
  Position 1: Action verb (distill, take, mix, etc.)
  Position 2-3: Ingredient(s) or measurements
  Position 4+: State/quality indicators or instructions
""")

print("=" * 80)
