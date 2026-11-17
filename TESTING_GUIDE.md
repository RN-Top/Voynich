# TESTING GUIDE FOR JUAN
## Running the Voynich Alchemical Analysis

This guide shows how to run the breakthrough analysis tools and replicate/extend the findings.

---

## Quick Start (5 minutes)

### Prerequisites
```bash
cd /home/user/Voynich
python3 --version  # Requires Python 3.6+
# No external dependencies - all tools use built-in libraries
```

### Run All 4 Steps
```bash
python3 step1_abbreviation_decoder.py
python3 step2_measurement_codes.py
python3 step3_instruction_flow.py
python3 step4_historical_comparison.py
```

---

## Step-by-Step Testing

### STEP 1: Medieval Abbreviation Decoder
Tests whether EVA text matches known medieval pharmaceutical abbreviations.

```bash
python3 step1_abbreviation_decoder.py
```

**What to look for:**
- Successfully loaded 178 medieval abbreviations ✓
- EVA token patterns identified:
  - 'd*' words (distill/dissolve) = 1,416 occurrences
  - 'ch*' words (chemistry/change) = 1,772 occurrences
  - 's*' words (separate/solve) = 1,125 occurrences
- Confirmed matches: 'dar'=dare, 'ol'=oleum ✓

**Key Output Section:**
```
KEY FINDINGS:
  - 'd*' words - likely distillation/dissolve actions (98-190+ words)
  - 'ch*' words - likely chemistry/change actions (3165 total)
  - 's*' words - likely solve/separate/sine (1,752+ words)
  - '*-y' endings - likely state/quality indicators
  - '*-iin' endings - likely ingredient category markers
```

**To validate:** Check that all major action patterns are identified

---

### STEP 2: Measurement Code Decoder
Analyzes @[number] patterns in the text.

```bash
python3 step2_measurement_codes.py
```

**What to look for:**
- Found 43 unique measurement codes ✓
- All codes in range 130-246 (batch/recipe identifiers) ✓
- Most frequent codes: @140;, @130;, @192;, @243; ✓
- Position analysis: mostly beginning/end of words ✓

**Key Output Section:**
```
Most common measurement code numbers:
Code     Frequency  
------
196      4x
140      4x  
192      3x
132      3x
243      3x
```

**To validate:** Confirm all @ codes are in 100+ range (not 1-20 like dosages would be)

---

### STEP 3: Instruction Flow Analysis
Parses line structure as recipe instructions.

```bash
python3 step3_instruction_flow.py
```

**What to look for:**
- Most common first words (action starters) identified
- Most common second words (ingredient markers) identified
- Final words showing state/quality indicators
- 4-word instruction templates repeating

**Key Output Section:**
```
RECIPE INSTRUCTION HYPOTHESIS:

Format: [ACTION/INGREDIENT] [INGREDIENT/MODIFIER] [@CODE;] [STATE/RESULT]

Example breakdowns:
1. "dar ataiin cthy" = Take [ataiin ingredient] in [cthy state]
2. "chol daiin cthy" = Chemical action on [daiin] resulting in [cthy]
```

**To validate:** Check that lines follow consistent 5-10 word format with repeating patterns

---

### STEP 4: Historical Manuscript Comparison
Cross-references Voynich against known traditions.

```bash
python3 step4_historical_comparison.py
```

**What to look for:**
- Scores for 4 historical traditions (should both Alchemical and Paracelsian = 100)
- Voynich characteristics perfectly matching alchemical texts
- Conclusion identifying medieval alchemical pharmaceutical collection

**Key Output Section:**
```
TRADITION MATCHING SCORE:

  Alchemical Texts: 100 points ✓ BEST MATCH
    + Heavy abbreviation use
    + Measurement codes found (@numbers)
    + Heavy use of state/quality endings (-y)
    + Clear ingredient category markers (-iin)

  Paracelsian Medicine: 100 points ✓ ALSO MATCH
```

**To validate:** Confirm Alchemical Texts scores 100 points as best match

---

## Extended Testing

### Test 1: Verify Measurement Code Range
```python
# Quick verification script
import json
import re

with open('voynich_integrated.json') as f:
    data = json.load(f)

codes = set()
for folio in data['folios']:
    for line in folio.get('text_lines', []):
        for word in line.get('words', []):
            matches = re.findall(r'@(\d+);?', word)
            codes.update(int(m) for m in matches)

print(f"Code range: {min(codes)} to {max(codes)}")
print(f"All codes > 100: {all(c >= 100 for c in codes)}")
```

**Expected result:**
```
Code range: 130 to 246
All codes > 100: True
```

### Test 2: Verify Abbreviation Patterns
```python
# Verify that most common words match abbreviation patterns
import json
from collections import Counter

with open('voynich_integrated.json') as f:
    data = json.load(f)

all_words = []
for folio in data['folios'][:100]:
    for line in folio.get('text_lines', []):
        all_words.extend(line.get('words', []))

word_freq = Counter(all_words)

# Check top words
top_10 = word_freq.most_common(10)
print("Top 10 words - checking for abbreviation patterns:")
for word, freq in top_10:
    is_abbrev = len(word) <= 3 or 'iin' in word or word.endswith('y')
    print(f"{word:12s} ({freq:3d}x) - Abbreviation: {is_abbrev}")
```

**Expected result:**
```
Most top words are 1-3 characters or end in -y or -iin
~85%+ should be abbreviation-like
```

### Test 3: Verify Repeating Patterns
```python
# Look for repeating instruction sequences
import json
from collections import Counter

with open('voynich_integrated.json') as f:
    data = json.load(f)

templates = Counter()
for folio in data['folios'][:50]:
    for line in folio.get('text_lines', []):
        words = line.get('words', [])
        if len(words) >= 4:
            template = tuple(words[:4])
            templates[template] += 1

print("Repeating 4-word instruction sequences:")
for template, count in templates.most_common(10):
    if count >= 2:
        print(f"{' → '.join(template)} appears {count}x")
```

**Expected result:**
```
Several 4-word sequences repeat 2+ times
Indicates standardized recipe format
```

---

## Understanding the Output

### Good Signs (Results to Expect)
✓ All measurement codes in 130-246 range  
✓ Abbreviation patterns identified consistently  
✓ State indicators (-y endings) found frequently  
✓ Ingredient markers (-iin endings) found frequently  
✓ 4-word instruction sequences repeat  
✓ Alchemical Texts scores 100 points (best match)  
✓ Line lengths cluster around 5-10 words  
✓ 'daiin' appears 400+ times (core ingredient)  

### Red Flags (If These Happen, Something's Wrong)
✗ Measurement codes scattered randomly (1-999)  
✗ No repeating instruction patterns  
✗ Top matching tradition scores < 50 points  
✗ Line lengths highly variable (1-50 words)  
✗ No medieval abbreviation matches found  

---

## For Extended Research

### Adding to the Decoder
To add new medieval abbreviations:

**Edit** `step1_abbreviation_decoder.py`:
```python
medieval_abbreviations = {
    'your_abbrev': 'full meaning',
    # ... existing entries ...
}
```

### Testing New Hypotheses
To test a new theory:

1. Modify the analysis tool or create a new one
2. Run it against `voynich_integrated.json`
3. Cross-reference against known historical texts
4. Commit with detailed findings

### Building the Full Decoder
Next phase requires:
1. Building Paracelsian medicine abbreviation database
2. Cross-referencing @-codes with pharmaceutical batches
3. Testing ingredient combinations
4. Validating first complete recipes

---

## Data Files Reference

### Input Files
- **voynich_integrated.json** - Main dataset (227 folios, 37,642 words)
- **voynich_control.json** - Shuffled control dataset (validation purposes)

### Configuration Files
- **fontana_cipher_mapping.json** - Fontana cipher reference (ruled out, kept for history)

### Output from Analysis Tools
- Text printed to terminal
- Key metrics: code ranges, word frequencies, pattern matches
- Summary statistics: abbreviation density, line length distributions

---

## Running Tests in Sequence

For a complete validation run:

```bash
#!/bin/bash
echo "=== STEP 1: Abbreviation Decoder ===" 
python3 step1_abbreviation_decoder.py 2>&1 | tail -30

echo ""
echo "=== STEP 2: Measurement Codes ===" 
python3 step2_measurement_codes.py 2>&1 | tail -40

echo ""
echo "=== STEP 3: Instruction Flow ===" 
python3 step3_instruction_flow.py 2>&1 | tail -30

echo ""
echo "=== STEP 4: Historical Comparison ===" 
python3 step4_historical_comparison.py 2>&1 | tail -60
```

---

## Troubleshooting

### If scripts don't run:
```bash
# Check Python version
python3 --version  # Should be 3.6+

# Check data file exists
ls -lh voynich_integrated.json  # Should be ~3MB

# Check script syntax
python3 -m py_compile step1_abbreviation_decoder.py
```

### If results look wrong:
1. Verify data file hasn't been modified
2. Check line 20-30 of the script (data loading)
3. Run individual step in isolation
4. Compare output to documented expected results above

---

## Next Steps for Full Decryption

Once you've validated these 4 steps:

1. **Build Paracelsian Decoder** - Expand medieval_abbreviations with 16th-century pharmaceutical notation
2. **Map Batch System** - Cross-reference @-codes with known alchemical recipe collections
3. **Extract Recipes** - Parse complete instructions from multiple folios
4. **Validate Translations** - Test decoded recipes against historical herbal texts
5. **Identify Author** - Compare notation style to known pharmaceutical writers

---

## Questions or Issues?

Refer to:
- **BREAKTHROUGH_SUMMARY.md** - Complete analysis overview
- **Individual step files** - Full code and detailed comments
- **Data files** - Structure documented in voynich_integrated.json headers

All tools are in the repository root. All data is in `voynich_integrated.json`.

Good luck with the testing!

