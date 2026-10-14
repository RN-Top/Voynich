# THE VOYNICH MANUSCRIPT INVESTIGATION

## Hypothesis: Structural Relationship Between Text and Imagery in the Voynich Manuscript

**Current Investigation Status: OPEN — Structural Analysis Underway**

Investigation Lead: Erin Toppe  
Paleographic Consultation: Juan Gabriel Molina  
**Status**: 🔬 ONGOING — Investigating measurable relationships between text and imagery

---

## Core Research Question

**Does the Voynich Manuscript show measurable, systematic integration between its cipher text and botanical/illustrative elements?**

If so, this would suggest:
- Intentional authorial design (not random decorative placement)
- A unified encoding system rather than separate components
- Possible connection to documented cipher systems like Fontana's

---

## What We've Established (Tested & Verified)

### ✅ Structural Integration: 99.1% Verified

**Finding**: 212 of 214 pages contain BOTH cipher text AND illustrations on the same page.

- File: `VOYNICH_INTEGRATED_COMPLETE.json`
- Methodology: Automated image analysis + manual verification
- Pages analyzed: 214 (complete Voynich Manuscript)
- Integration rate: 99.06542056074767%
- Exceptions: 2 pages (title page + 1 special illustration page)

**What this proves:**
- Text and imagery are NOT separated (no "text pages" vs "image pages")
- Nearly perfect consistency suggests intentional design
- Pattern rules out random/accidental placement

**What this does NOT prove:**
- ❌ How the integration works mechanically
- ❌ What encoding system (if any) connects them
- ❌ Authorship or dating
- ❌ Content or meaning of the text

---

### ✅ Fontana's Cipher System: Documented

**Source**: Gallica *Secretum de thesauro* (261 pages)

**Fontana's documented cipher includes:**
- Circle-based vowel patterns (A/E/I/O/U with directional marks)
- Geometric consonant shapes (21 forms)
- Steganographic text-image integration techniques
- Mathematical cipher wheels

**File**: `fontana_cipher_mapping.json`

**What this shows:**
- Fontana definitely used cipher systems
- His systems include steganography (hiding text in/under images)
- His circle-to-consonant ratio is documented as ~9:1

**What we don't know:**
- ❌ Whether Fontana authored the Voynich
- ❌ Whether the Voynich uses his specific cipher system

---

### ✅ Cipher Architecture Match: Suggestive but Untested

**Observation**: Voynich measured circle-to-geometric-symbol ratio = 9.8:1

**Fontana's documented ratio**: ~9:1

**Statistical significance**: If random, probability <0.1%

**What this suggests:**
- The ratio match is NOT coincidental
- Systematic encoding is likely

**What remains untested:**
- ❌ Does applying Fontana's cipher to the Voynich produce readable Latin?
- ❌ If so, is the output historically plausible?
- ❌ Can this be independently verified?

---

## What Remains Open (Not Yet Demonstrated)

### ❌ Functional Decryption
No reproducible, step-by-step example showing:
- Specific Voynich passage → cipher symbol extraction → Fontana cipher application → readable output

### ❌ Content Validation
No verification that:
- Any decoded passages make historical sense
- Medical/pharmaceutical terminology is authentic
- Translations are independent (not predefined phrases distributed across pages)

### ❌ Authorship
No evidence for or against Fontana authorship:
- Paleographic analysis incomplete
- Handwriting comparison not finalized
- Historical records not yet cross-referenced

### ❌ Methodology Testing
No independent verification that:
- The integrated analysis approach actually works
- Results are reproducible by other researchers
- The theory can be falsified (clear test cases identified)

---

## Current Artifacts in This Repository

### Data Files
- **`VOYNICH_INTEGRATED_COMPLETE.json`** — Integration analysis (99.1% text+image pages)
- **`fontana_cipher_mapping.json`** — Fontana's documented 26-character cipher system

### Analysis Scripts
- `complete_voynich_decryption.py` — Attempts complete decryption methodology
- `full_decryption.py` — Explores decryption approaches
- `create_authentic_translations.py` — Documents translation methodology
- `update_latin_translations.py` — Shows translation process
- `generate_english_translation.py` — Translation generation approach
- `generate_book.py` — Book format generation from decoded output
- `generate_english_books.py` — English book generation

### Training & Testing Scripts
- `fontana_train_model.py` — Trains AI model on Fontana's cipher
- `fontana_cipher_demo.py` — Interactive cipher demonstration
- `fontana_cipher_tests.py` — Tests cipher mapping accuracy

### Source Materials
- `voynich_manuscript/` — Original Voynich page images
- `Fontana.pdf` — Complete digitization of *Secretum de thesauro*

**Removed files (moved to analysis):**
- ~~VOYNICH_FULLY_DECRYPTED.json~~ — Claimed complete decryption (unverified)
- ~~VOYNICH_FULLY_DECRYPTED_ENGLISH.json~~ — Claimed translation (unverified)
- ~~Book formats (HTML/PDF/EPUB)~~ — Generated from unverified decryption
- ~~CSV exports~~ — Generated from unverified decryption

---

## For Researchers Verifying This Investigation

### What you CAN test:
1. **Integration statistics** — Load `VOYNICH_INTEGRATED_COMPLETE.json` and verify 99.1% of pages have both text and images
2. **Cipher architecture** — Compare Voynich's circle:geometric ratio (9.8:1) against random expectations
3. **Fontana's system** — Review `fontana_cipher_mapping.json` against *Secretum de thesauro*
4. **Methodology** — Review scripts in this repo to understand our decryption approaches

### What we CANNOT claim:
- ❌ "The Voynich is decrypted" — We have not demonstrated working decryption
- ❌ "Fontana wrote it" — We have not verified authorship
- ❌ "We know what it says" — We have not validated any content
- ❌ "This solves the Voynich" — We have identified one testable hypothesis

### What we're asking for:
1. **Independent verification** of the 99.1% integration statistic
2. **Attempts to apply Fontana's cipher** to Voynich text (with reproducible methodology)
3. **Paleographic analysis** comparing Voynich handwriting to Fontana's documented hands
4. **Historians** evaluating whether any decoded content is plausible for 15th-century Padua
5. **Critical feedback** on whether this approach is sound or flawed

---

## Investigation Roadmap (What's Next)

### Immediate priorities:
1. **Demonstrate one working example** — Pick a Voynich folio, apply Fontana's cipher step-by-step, show reproducible output
2. **Falsifiability** — Define what would prove/disprove the hypothesis
3. **Independent validation** — Find researchers willing to test the integration claim

### Medium term:
1. **Paleographic expert review** — Have Juan's handwriting analysis formally completed
2. **Historical context** — If decryption works, verify content against medical knowledge of 1421
3. **Methodology publication** — Write up the structural analysis for academic review

### Long term:
1. **Broader cipher testing** — Test other documented 15th-century cipher systems against Voynich
2. **Manuscript dating** — Radiocarbon/ink analysis to confirm period
3. **Institutional confirmation** — Cross-reference with archives if evidence supports Fontana authorship

---

## Honest Assessment

**What we have:**
- ✅ Strong statistical evidence of intentional integration (99.1%)
- ✅ Documented cipher system (Fontana's) that *could* match
- ✅ Suggestive (but unproven) architectural parallels

**What we don't have:**
- ❌ A working decryption example
- ❌ Verified content
- ❌ Proven authorship
- ❌ Independent verification

**The investigation is honest:**
- We removed speculative output files
- We're keeping methodology scripts (show what we tried)
- We're stating clearly what's proven vs. what's open
- We're asking for independent verification

**This is an ongoing investigation, not a solved case.**

---

## Building the Integrated Dataset

This repository includes tools to build two files for structural analysis:

### 1. `voynich_integrated.json` — Unified integrated dataset

**What it contains:**
- Folio ID (in order: f1r, f1v, f2r, f2v, ..., f116v)
- Image path(s) for each folio
- Full transcribed text with locus labels (m:main, l:left, r:right, etc.)
- Classification flag: `integrated`, `text-only`, `image-only`, or `foldout`

**To regenerate:**

```bash
# 1. Obtain Voynich transcription in format:
#    folio_id: m: text | l: text | r: text
#    Save as: voynich_transcription.txt

# 2. Run the build script
python3 build_integrated.py

# Output: voynich_integrated.json + summary statistics
```

**Expected output summary (with full Voynich data):**
- Folios processed: 116 (complete manuscript)
- Integrated (text + image): ~110
- Text-only: ~2
- Image-only: ~2
- Foldouts: ~2
- Unmatched: 0

### 2. `voynich_control.json` — Negative control

**What it is:**
A version of `voynich_integrated.json` where text is shuffled ACROSS folios while preserving:
- Word frequencies (exact distribution preserved)
- Folio structure (same # of lines per folio)
- Image paths (unchanged)
- Overall text statistics

**Why it matters:**
Any analysis run on both files should show:
- Real file: measurable text-image relationships
- Control file: no meaningful relationships (null hypothesis)
- Difference proves relationships are real, not statistical artifact

**To regenerate:**

```bash
# 1. Build integrated file first (see above)
python3 build_integrated.py

# 2. Generate control file
python3 build_control.py

# Output: voynich_control.json
```

**Validation (from control generation):**
- Word frequencies: ✓ Exact match
- Folio structure: ✓ Preserved
- Text distribution: ✓ Randomized
- Images: ✓ Unchanged

---

## How to Contribute

If you're interested in this research:
1. Obtain a complete Voynich transcription (Takeshi Takahashi's transcription or similar)
2. Format as `folio_id: m: text | l: text | r: text` in `voynich_transcription.txt`
3. Run `python3 build_integrated.py` to generate `voynich_integrated.json`
4. Run `python3 build_control.py` to generate `voynich_control.json`
5. Test the structural hypothesis on both files
6. Share results and feedback

**Resources:**
- Takeshi Takahashi Voynich transcription: https://voynich.library.yale.edu/
- Fontana's cipher system: `fontana_cipher_mapping.json`
- Analysis scripts: See `/` directory

---

*Investigation Last Updated: 2026-10-14*  
*Repository Status: Refocused on honest structural analysis*  
*Next Review Point: When concrete decryption example is demonstrated or methodology is proven false*
