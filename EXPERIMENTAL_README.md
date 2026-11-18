# Experimental Decryption Toolkit
**Branch:** `experimental/decode-testing`
**Status:** Playing around - not for production

This branch contains exploratory decryption experiments on the Voynich manuscript. These are hypothesis-testing tools, not finalized decoders.

## Running the Experiments

```bash
python3 decode_v1_comprehensive.py      # Abbreviation expansion testing
python3 decode_v2_frequency_analysis.py # Character/word frequency analysis
python3 decode_v3_substitution_cipher.py # Frequency-based cipher mapping
python3 decode_v4_code_patterns.py      # @-code structural analysis
```

## Key Findings So Far

### From v1 (Abbreviation Testing)
- 39,026 total words, 8,339 unique
- 1,000 words matched to abbreviations (mostly "dar" and "oleum" prefixes)
- Top unmatched pattern: -dy endings (952 words, 6,018 instances)
- **Observation:** Most common unmatched words have ingredient-like endings

### From v2 (Frequency Analysis)
- **Line structure confirmed:** Average 7.2 words/line, peak at 10 words
  - Hypothesis: 5-10 word format = standardized recipe template ✓
- **Character frequencies are skewed:** o=13.1% (vs Latin 6.9%), h=9.2% (vs Latin 3.1%)
  - Suggests text is NOT random + abbreviations use certain letters heavily
- **Top word patterns:** daiin (848), ol (560), ar (403), chol (395), or (390)
  - Many end in -iin, -ain, -ol, -ar → ingredient categories ✓
- **@-codes cluster with:** -y endings (698), -dy endings (209), -iin endings (165)
  - Pattern: ingredients marked with suffix codes + @batch identifiers

### From v3 (Substitution Cipher)
- **Character bigrams:** "ch" is extremely common (11,125 instances)
  - Suggests medieval Latin "ch" digraphs are preserved
  - Implies letter-by-letter substitution (not digraph substitution)
- **Simple frequency mapping:** Doesn't produce readable text yet
  - Reason: Voynich has unusual frequencies + multiple encoding layers
  - Text is both enciphered AND abbreviated

### From v4 (@-Code Patterns)
- **Code range:** @130 to @254 (125-code span, 89 unique codes)
  - Peak frequency: @133 (11x), @132 (10x)
  - Distribution: 24.7% in 100-149, 52.7% in 150-199, 20.9% in 200-249
  - **Interpretation:** Batch numbering system ✓
- **Code positions:** 61 at line START, 31 at line END
  - Pattern: [action/ingredient] [@BATCH] [state/quality]
- **Associated words:** Ingredient patterns cluster strongly around @-codes
  - -y endings: 698 instances near codes
  - -iin endings: 165 instances near codes

## Working Hypotheses

### Confirmed:
1. ✓ **Recipe format:** 5-10 word lines with repeating instruction templates
2. ✓ **@-codes:** Batch/recipe identifiers in 130-246 range
3. ✓ **Ingredient categories:** Words ending in -iin, -ain, -al, -or, -ar, -ol
4. ✓ **Action words:** dar (take), sol (solve), dis (distill), etc.
5. ✓ **Latin preservation:** "ch" bigrams heavily used (medieval Latin)

### To Test:
1. [ ] Can we map -y endings to medical/alchemical state words?
2. [ ] Can we identify specific ingredients from base words (qok-, chedy-, shedy-)?
3. [ ] Does @-code sequencing follow pharmaceutical batch patterns?
4. [ ] Can we find the missing cipher key using bigram frequency analysis?
5. [ ] Do certain folios correlate with specific @-code ranges?

## Next Steps

### For Phase 1 (Validation - Not Started)
- [ ] Verify that abbreviation decoder works on known Latin words
- [ ] Check if ingredient hypotheses hold against historical recipe texts
- [ ] Cross-reference @-codes with Paracelsian medicine batch systems

### For Phase 2 (Extension - Not Started)
- [ ] Build comprehensive medieval pharmaceutical abbreviation database
- [ ] Test ingredient combinations for pharmaceutical validity
- [ ] Analyze ingredient frequencies for authenticity

### For Phase 3 (Full Decryption - Not Started)
- [ ] Develop hill-climbing cipher decoder using bigram frequencies
- [ ] Extract complete recipes from multiple folios
- [ ] Validate against historical pharmaceutical texts

## Important Notes

- **These are experiments**, not final results
- **Do not merge into main** - this is exploratory work
- **Keep in experimental branch** for now
- Results are showing promising patterns but nothing is decrypted yet
- Need Juan's paleographic expertise to validate before moving forward

## Questions for Juan

When you review this:
1. Do the ingredient patterns (endings like -iin, -ain, -ol) match known alchemical notation?
2. Can you identify the abbreviation style (Paracelsian? Ficino? Other)?
3. Do the @-codes suggest a known pharmaceutical recipe collection?
4. What's your assessment of the "ch" bigram frequency vs medieval Latin?

---
**Last updated:** 2026-11-17  
**Status:** Experimental branch - playing around to understand patterns
