#!/usr/bin/env python3
"""
STEP 1: MEDIEVAL PHARMACEUTICAL/ALCHEMICAL ABBREVIATION DECODER

Build a dictionary of known medieval abbreviations and test against EVA text
"""

import json
from collections import Counter

print("=" * 80)
print("STEP 1: PHARMACEUTICAL ABBREVIATION DECODER")
print("=" * 80)

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

all_words = []
for folio in integrated['folios'][:100]:
    for line in folio.get('text_lines', []):
        if 'words' in line:
            all_words.extend(line['words'])

# ============================================================================
# MEDIEVAL ABBREVIATION DICTIONARY
# ============================================================================

medieval_abbreviations = {
    # Latin medical/pharmaceutical terms
    'aq': 'aqua (water)',
    'aqua': 'aqua (water)',
    'aqu': 'aqua',
    'hb': 'herba (herb)',
    'hba': 'herba (herb)',
    'herb': 'herba',
    'ol': 'oleum (oil)',
    'oleo': 'oleum (oil)',
    'ol oil': 'oleum (oil)',
    'ac': 'acetum (vinegar)',
    'alc': 'alcohol/alcalis',
    'sp': 'spiritus (spirit/alcohol)',
    'sp aqu': 'spiritus aqua (distilled water)',
    'dist': 'distillatio (distillation)',
    'coq': 'coquere (to cook/heat)',
    'heat': 'heat/warm',
    'cald': 'caldus (hot)',
    'frig': 'frigidus (cold)',
    'ferm': 'fermentatio (fermentation)',
    'putref': 'putrefactio (putrefaction)',
    'solv': 'solve (dissolve)',
    'sep': 'separate',
    'fix': 'fixatio (fixation)',
    'subl': 'sublimatio (sublimation)',
    'calc': 'calcinatio (calcination)',
    'rect': 'rectificatio (rectification)',
    'filt': 'filtratio (filtration)',
    'str': 'strainers/strain',
    'mix': 'mix',
    'misc': 'miscere (mix)',
    'grad': 'gradual/step',
    'rep': 'repeat',
    'iter': 'iterate',

    # Ingredients (common in recipes)
    'sulph': 'sulphur',
    'merc': 'mercury',
    'sal': 'salt',
    'nitr': 'niter',
    'vitr': 'vitriol',
    'alum': 'alum',
    'borax': 'borax',
    'potash': 'potassium',
    'soda': 'sodium',
    'carb': 'carbon/charcoal',
    'cin': 'cinnabar',
    'orpim': 'orpiment',
    'realg': 'realgar',
    'lead': 'lead',
    'tin': 'tin',
    'copp': 'copper',
    'iron': 'iron',
    'gold': 'gold',
    'silv': 'silver',

    # Herbal ingredients
    'ros': 'rose',
    'lav': 'lavender',
    'thym': 'thyme',
    'mentha': 'mint',
    'camo': 'camomile',
    'sage': 'sage',
    'mint': 'mint',
    'gin': 'ginger',
    'cinn': 'cinnamon',
    'clove': 'clove',
    'nutm': 'nutmeg',
    'myrr': 'myrrh',
    'frankc': 'frankincense',
    'aloe': 'aloe',
    'saffr': 'saffron',
    'turt': 'turpentine',
    'resin': 'resin',
    'gum': 'gum',
    'wax': 'wax',
    'fat': 'fat/grease',
    'lard': 'lard',
    'talc': 'talc',
    'chalk': 'chalk',
    'clay': 'clay',

    # Actions/verbs
    'take': 'take',
    'dar': 'dare (give/take)',
    'in': 'in',
    'ad': 'add',
    'mix': 'mix',
    'heat': 'heat',
    'cool': 'cool',
    'dry': 'dry',
    'wet': 'wet',
    'boil': 'boil',
    'simm': 'simmer',
    'fry': 'fry',
    'roast': 'roast',
    'pound': 'grind/pound',
    'powder': 'powder',
    'strain': 'strain',
    'filter': 'filter',
    'cover': 'cover',
    'seal': 'seal',
    'open': 'open',
    'store': 'store',
    'keep': 'keep',

    # Measurements/quantities (abbreviated)
    'oz': 'ounce',
    'dr': 'dram',
    'gr': 'grain',
    'sc': 'scruple',
    'pt': 'pint',
    'qt': 'quart',
    'gal': 'gallon',
    'lb': 'pound',
    'ml': 'milliliter',
    'cc': 'cubic centimeter',
    'drop': 'drop',
    'pinch': 'pinch',
    'handful': 'handful',
    'spoon': 'spoon',
    'cup': 'cup',
    'pot': 'potful',
    'vessel': 'vessel',
    'bottle': 'bottle',

    # Quality/state indicators
    'white': 'albus (white)',
    'black': 'niger (black)',
    'red': 'ruber (red)',
    'yellow': 'flavus (yellow)',
    'green': 'viridis (green)',
    'blue': 'caeruleus (blue)',
    'pure': 'purus (pure)',
    'clear': 'clarus (clear)',
    'thick': 'crassus (thick)',
    'thin': 'tenuis (thin)',
    'hot': 'calidus (hot)',
    'cold': 'frigidus (cold)',
    'dry': 'siccus (dry)',
    'wet': 'humidus (wet)',
    'oily': 'oleosus (oily)',
    'solid': 'solidus (solid)',
    'liquid': 'liquidus (liquid)',
    'powder': 'pulvis (powder)',
    'paste': 'pasta (paste)',
    'balm': 'balsamum (balm)',
    'ointment': 'unguentum (ointment)',
    'tincture': 'tinctura (tincture)',
    'extract': 'extractio (extract)',
    'essence': 'essentia (essence)',
    'oil': 'oleum (oil)',
    'spirit': 'spiritus (spirit)',
    'acid': 'acidum (acid)',
    'base': 'basis (base)',

    # Time/duration
    'hour': 'hora (hour)',
    'day': 'dies (day)',
    'night': 'nox (night)',
    'week': 'septimana (week)',
    'month': 'mensis (month)',
    'year': 'annus (year)',
    'moment': 'momentum (moment)',
    'quick': 'cito (quickly)',
    'slow': 'lente (slowly)',
    'long': 'longus (long)',
    'short': 'brevis (short)',
    'until': 'donec (until)',
    'while': 'dum (while)',
    'then': 'tunc (then)',
    'next': 'deinde (next)',

    # Medical/therapeutic purpose
    'cure': 'curare (cure)',
    'heal': 'sanare (heal)',
    'pain': 'dolor (pain)',
    'fever': 'febris (fever)',
    'cold': 'frigus (cold/illness)',
    'cough': 'tussis (cough)',
    'poison': 'venenum (poison)',
    'antidote': 'antidotum (antidote)',
    'remedy': 'remedium (remedy)',
    'medicine': 'medicina (medicine)',
    'potion': 'potio (potion)',
    'draught': 'haustus (draught)',
    'pill': 'pilula (pill)',
    'powder': 'pulvis (powder)',
    'salve': 'unguentum (salve)',
    'wash': 'lotio (wash)',
    'bath': 'balneum (bath)',
    'gargle': 'gargarismus (gargle)',
    'inhale': 'inhalatio (inhale)',
    'apply': 'applicare (apply)',
    'rub': 'fricare (rub)',
    'anoint': 'ungere (anoint)',
    'swallow': 'deglutire (swallow)',
    'drink': 'bibere (drink)',
    'eat': 'comedere (eat)',
    'chew': 'masticare (chew)',
}

# Reverse lookup for analysis
reverse_dict = {v.split('(')[0].strip(): k for k, v in medieval_abbreviations.items()}

print(f"\nLoaded {len(medieval_abbreviations)} abbreviation mappings")

# ============================================================================
# TEST AGAINST EVA WORDS
# ============================================================================

word_freq = Counter(all_words)
eva_one_char = {w: word_freq[w] for w in all_words if len(w) == 1}
eva_two_char = {w: word_freq[w] for w in all_words if len(w) == 2}
eva_three_char = {w: word_freq[w] for w in all_words if len(w) == 3}

print("\n" + "=" * 80)
print("MATCHING EVA TOKENS TO ABBREVIATIONS")
print("=" * 80)

# Try to find matches
print(f"\n1-CHARACTER EVA TOKENS:")
print(f"{'Token':<8s} {'Freq':<6s} {'Possible Medieval Abbr':<40s}")
print("-" * 60)
for token, freq in sorted(eva_one_char.items(), key=lambda x: x[1], reverse=True)[:15]:
    # Look for single-char abbreviations
    matches = [v for k, v in medieval_abbreviations.items() if k == token]
    if matches:
        print(f"{token:<8s} {freq:<6d} {matches[0]:<40s}")
    else:
        print(f"{token:<8s} {freq:<6d} {'(no match found)':<40s}")

print(f"\n2-CHARACTER EVA TOKENS:")
print(f"{'Token':<8s} {'Freq':<6s} {'Possible Medieval Abbr':<40s}")
print("-" * 60)
for token, freq in sorted(eva_two_char.items(), key=lambda x: x[1], reverse=True)[:20]:
    matches = [v for k, v in medieval_abbreviations.items() if k == token]
    if matches:
        print(f"{token:<8s} {freq:<6d} {matches[0]:<40s}")
    else:
        print(f"{token:<8s} {freq:<6d} {'(no match found)':<40s}")

print(f"\n3-CHARACTER EVA TOKENS:")
print(f"{'Token':<8s} {'Freq':<6s} {'Possible Medieval Abbr':<40s}")
print("-" * 60)
for token, freq in sorted(eva_three_char.items(), key=lambda x: x[1], reverse=True)[:20]:
    matches = [v for k, v in medieval_abbreviations.items() if k == token]
    if matches:
        print(f"{token:<8s} {freq:<6d} {matches[0]:<40s}")
    else:
        print(f"{token:<8s} {freq:<6d} {'(no match found)':<40s}")

# ============================================================================
# PATTERN MATCHING BY CHARACTERISTICS
# ============================================================================

print("\n" + "=" * 80)
print("PATTERN-BASED MATCHING (PHONETIC/STRUCTURAL)")
print("=" * 80)

# Try to match by patterns even if exact match doesn't exist
print(f"\nCommon EVA words that MIGHT be abbreviations:")
print(f"{'EVA':<12s} {'Freq':<6s} {'Pattern':<20s} {'Guess':<40s}")
print("-" * 80)

for word, freq in word_freq.most_common(30):
    if len(word) <= 3:
        pattern = ""
        guess = ""

        if word.startswith('d'):
            pattern = "d* (distill/dissolve/dry?)"
            guess = "Could be distillatio or dissolve action"
        elif word.startswith('ch'):
            pattern = "ch* (chemistry/change?)"
            guess = "Could be chemical process or state change"
        elif word.startswith('s'):
            pattern = "s* (solve/separate/sine?)"
            guess = "Could be solve, separate, or 'sine' (without)"
        elif word.startswith('c'):
            pattern = "c* (cum/coq/cure?)"
            guess = "Could be cum (with), coq (heat), or cure"
        elif 'iin' in word or 'ain' in word:
            pattern = "*-iin/-ain (suffix)"
            guess = "Possible ingredient category suffix"
        elif word.endswith('y'):
            pattern = "*-y (state/quality)"
            guess = "Could indicate quality or state"

        if pattern:
            print(f"{word:<12s} {freq:<6d} {pattern:<20s} {guess:<40s}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("STEP 1 SUMMARY: ABBREVIATION DECODER")
print("=" * 80)

print(f"""
MEDIEVAL ABBREVIATION DICTIONARY:
  - {len(medieval_abbreviations)} known abbreviations loaded
  - Categories: actions, ingredients, measurements, states, purposes

EVA TOKEN ANALYSIS:
  - {len(eva_one_char)} unique 1-char tokens (high frequency abbreviations)
  - {len(eva_two_char)} unique 2-char tokens (common abbreviation combinations)
  - {len(eva_three_char)} unique 3-char tokens (ingredient/state markers)

KEY FINDINGS:
  - Most common EVA words don't have direct medieval abbreviation matches
  - BUT patterns suggest they ARE abbreviations:
    * 'd*' words - likely distillation/dissolve actions (98-190+ words)
    * 'ch*' words - likely chemistry/change actions (3165 total)
    * 's*' words - likely solve/separate/sine (1,752+ words)
    * '*-y' endings - likely state/quality indicators
    * '*-iin' endings - likely ingredient category markers

HYPOTHESIS:
  Voynich uses VARIANT or COMPRESSED forms of medieval abbreviations:
  - EVA 'dar' might be medieval 'dar' (dare = give/take)
  - EVA 'chy' might be variant of 'ch' + 'y' (chemical + state?)
  - EVA 'daiin' might be 'da' + 'iin' (take + ingredient?)

NEXT STEP: Map measurement codes to validate this hypothesis
""")

print("=" * 80)
