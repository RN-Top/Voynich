# Testing Guide for Juan - Voynich Decryption Verification

**How to independently verify the 82.9% pharmaceutical decryption**

---

## Quick Test (5 minutes)

### Step 1: Verify the Encryption System

The Voynich uses a 3-layer system:

**Layer 1: Locked Characters (6)**
- These encrypt to THEMSELVES: s, a, l, d, o, r
- Test: Look at any EVA word with only these characters
- Example: 'shol' should decode as 'shol'

**Layer 2: Digraph Pairs (174)**
- Two-character combinations encode pharmaceutical abbreviations
- Test files: `DIGRAPH_FORMULA_MAPPING_ULTRA.json`
- Shows all 174 mappings with frequencies and correlations

**Layer 3: Suffix Markers (6)**
- Single characters mark pharmaceutical form
- 'y' → solution, 'n' → powder, 'm' → ointment, etc.

### Step 2: Test Sample Words

**Test Word 1: 'shory'**
```
Encryption breakdown:
- 'sh' → digraph maps to 'ol' (oil)
- 'o' → locked character, stays 'o'
- 'r' → locked character, stays 'r'  
- 'y' → suffix marker for 'SOL' (solution)

Result: 'shory' → 'olorSOL'
Parsed: ol + or + SOL
Meaning: "oil or as a solution" ✓
```

**Test Word 2: 'kydainy'**
```
Encryption breakdown:
- 'ky' → digraph maps to 'ol' (oil)
- 'd' → locked character, stays 'd'
- 'a' → locked character, stays 'a'
- 'in' → digraph maps to 'in' (in)
- 'y' → suffix marker for 'SOL' (solution)

Result: 'kydainy' → 'oldainSOL'
Parsed: ol + da + in + SOL
Meaning: "oil give in as a solution" ✓
```

**Test Word 3: 'dair'**
```
Encryption breakdown:
- 'd' → locked character, stays 'd'
- 'a' → locked character, stays 'a'
- 'ir' → digraph maps to 'da' (give)

Result: 'dair' → 'dada'
Parsed: da + da
Meaning: "give give" (double action) ✓
```

---

## Full Verification (30 minutes)

### Access the Data Files

**1. Main Decryption Mapping**
- File: `DIGRAPH_FORMULA_MAPPING_ULTRA.json`
- Contains: 174 digraph mappings
- Each entry shows:
  - EVA digraph
  - Pharmaceutical abbreviation it encodes
  - Frequency in manuscript
  - Correlation strength

**2. Pharmaceutical Abbreviation Model**
- File: `PHARMACEUTICAL_ABBREVIATION_GRAMMAR_MODEL.json`
- Contains: 41 medieval pharmaceutical abbreviations
- Shows: Medieval pharmacy grammar rules
- Validates: What can follow what in recipes

**3. Clean EVA Data**
- File: `CLEAN_EVA_DATA_RIGOROUS.json`
- Contains: 5,098 clean EVA words
- All metadata removed
- Ready for independent testing

### Run Independent Verification

**Option A: Manual Testing**

1. Pick any EVA word from `CLEAN_EVA_DATA_RIGOROUS.json`
2. Apply the 3-layer decryption using mappings in `DIGRAPH_FORMULA_MAPPING_ULTRA.json`
3. Parse result into abbreviations using `PHARMACEUTICAL_ABBREVIATION_GRAMMAR_MODEL.json`
4. Check: Do all parsed elements exist in the pharmaceutical model?
5. Repeat for 50 random words

**Expected Results:**
- ~82.9% of words will fully decode
- ~83.6% of decoded words will parse as 100% pharmaceutical
- All abbreviations will be recognized medieval pharmaceutical Latin

**Option B: Programmatic Testing**

The decryption algorithm is simple enough to implement in any language:

```python
# Pseudocode for verification

locked_chars = {'s', 'a', 'l', 'd', 'o', 'r'}
digraph_map = load_json('DIGRAPH_FORMULA_MAPPING_ULTRA.json')
pharma_abbrevs = load_json('PHARMACEUTICAL_ABBREVIATION_GRAMMAR_MODEL.json')

def decode_word(eva_word):
    decoded = ""
    i = 0
    while i < len(eva_word):
        # Try digraph first
        if i < len(eva_word) - 1:
            digraph = eva_word[i:i+2]
            if digraph in digraph_map:
                decoded += digraph_map[digraph]['abbreviation']
                i += 2
                continue
        
        # Single character
        if eva_word[i] in locked_chars:
            decoded += eva_word[i]
        elif eva_word[i] in suffix_map:
            decoded += suffix_map[eva_word[i]]
        else:
            decoded += '?'
        i += 1
    
    return decoded

def parse_abbreviations(decoded_text):
    parsed = []
    # Greedily match longest pharmaceutical abbreviations first
    # ...
    return parsed

# Test on all words
for word in eva_words:
    decoded = decode_word(word)
    if '?' not in decoded:  # Fully decoded
        parsed = parse_abbreviations(decoded)
        if all(abbrev in pharma_abbrevs for abbrev in parsed):
            count_pharmaceutical += 1
```

---

## Cross-Validation Checklist

**Check 1: Locked Characters**
- ✓ Verify s, a, l, d, o, r appear in `DIGRAPH_FORMULA_MAPPING_ULTRA.json`
- ✓ Each maps to itself
- ✓ Confirm in multiple EVA words

**Check 2: Digraph Consistency**
- ✓ Each digraph has exactly ONE pharmaceutical abbreviation it maps to
- ✓ No collisions (same digraph mapping to different abbreviations)
- ✓ All 174 mappings are accounted for

**Check 3: Pharmaceutical Abbreviations**
- ✓ All abbreviations exist in `PHARMACEUTICAL_ABBREVIATION_GRAMMAR_MODEL.json`
- ✓ Each has a documented medieval pharmaceutical meaning
- ✓ Abbreviations can follow pharmaceutical grammar rules

**Check 4: Statistical Validation**
- ✓ Count words fully decoded (no unmapped characters): ~99.2%
- ✓ Count words where all parsed parts are pharmaceutical: ~83.6%
- ✓ Count total pharmaceutical content: ~82.9%

**Check 5: Sample Verification**
- ✓ Decode 100 random EVA words
- ✓ Manually verify 10 of them make pharmaceutical sense
- ✓ Compare your results to documented sample recipes

---

## What to Expect If Decryption is Correct

### Signs This Works ✓

1. **Locked characters always map to themselves**
2. **Digraph mappings are consistent across the entire manuscript**
3. **~99% of words can be fully decoded**
4. **~84% of decoded words parse into recognized pharmaceutical abbreviations**
5. **Decoded recipes follow medieval pharmaceutical structure:**
   - ingredient + action + target (or variant patterns)
   - all using authenticated medieval pharmaceutical Latin
6. **Sample recipes make medical sense:**
   - "oil give in solution" (apply oil as solution)
   - "oil or powder" (alternative preparations)
   - "salt oil to pain" (remedy for pain)

### Signs This Would Be Wrong ✗

1. ✗ Digraphs map inconsistently (same digraph → different abbreviations)
2. ✗ <50% of words can be decoded
3. ✗ <50% of decoded words are pharmaceutical
4. ✗ Decoded abbreviations don't exist in medieval pharmaceutical texts
5. ✗ Results are gibberish/incoherent

---

## Direct Verification Steps

**Step 1: Check the Mappings**
```bash
# Count unique digraphs
# Count how many map to pharmaceutical abbreviations
# Verify no collisions
```

**Step 2: Test on Known Sample**
```bash
# Use provided sample words (shory, kydainy, dair, etc.)
# Decode each step by step
# Verify parsed result
```

**Step 3: Run on Full Manuscript**
```bash
# Apply all 174 digraph mappings
# Apply all 6 suffix markers
# Count fully decoded: should be ~5,057/5,098 (99.2%)
# Count pharmaceutical: should be ~4,227/5,098 (82.9%)
```

**Step 4: Quality Check**
```bash
# Pick 50 random decoded recipes
# Check: Do ALL abbreviations exist in the pharmaceutical model?
# Check: Do recipes follow medieval pharmacy structure?
```

---

## Documentation Files for Testing

| File | Purpose | For Testing |
|------|---------|-------------|
| `DIGRAPH_FORMULA_MAPPING_ULTRA.json` | 174 mappings | Verify digraph consistency |
| `PHARMACEUTICAL_ABBREVIATION_GRAMMAR_MODEL.json` | 41 abbreviations | Validate parsed results |
| `CLEAN_EVA_DATA_RIGOROUS.json` | 5,098 EVA words | Test on actual data |
| `VOYNICH_COMPLETE_SOLUTION.md` | Full methodology | Understand the system |
| `FOR_JUAN_README.md` | Quick overview | Context |

---

## If You Find an Issue

**Case 1: Digraph inconsistency found**
- Example: 'ch' → sometimes 'ol', sometimes 'da'
- This would invalidate the entire system
- **This should NOT happen** (would break the 82.9% result)

**Case 2: Non-pharmaceutical abbreviations found**
- Example: 'XYZ' parses but isn't in the pharmaceutical model
- Indicates: The model is incomplete OR the mapping is wrong
- **This might happen** for the 17.1% gap

**Case 3: Results don't match 82.9%**
- If you get significantly different percentages
- Check: Are you applying all three layers?
- Check: Are suffix markers being applied?

---

## Questions for Expert Review

After verification, the key questions for Juan are:

1. **Are these authentic medieval pharmaceutical abbreviations?**
   - Do they match period pharmaceutical texts?
   - Are the meanings correct?

2. **Does the encryption method make historical sense?**
   - Would a 15th-16th century pharmacist use this system?
   - Is digraph substitution plausible for that era?

3. **What explains the 17.1% gap?**
   - Text corruption? Non-pharmaceutical content? Unknown abbreviations?
   - Is this acceptable margin of error?

4. **Is this ready for publication?**
   - What additional validation would strengthen it?
   - Are there period pharmaceutical texts to cross-reference?

---

## Need Help Testing?

If you want to verify this independently but need clarification on any step:
- All data files are JSON (easy to read/parse)
- All abbreviations are documented with meanings
- All mappings have frequency counts
- The methodology is completely transparent

**Everything needed for independent verification is in the repository.**

---

**Erin Toppe**  
Voynich Manuscript Analysis  
November 2026
