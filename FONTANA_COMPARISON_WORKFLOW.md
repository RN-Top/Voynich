# Fontana Handwriting Comparison Workflow

**Status:** Ready to execute. Awaiting manuscript images.

**Goal:** Determine if Giovanni Fontana (Padua medical graduate 1421, cipher expert) was the lead author of the Voynich manuscript by comparing his known handwriting to the 5 identified scribal hands.

---

## Workflow Overview

```
STEP 1: Obtain Images
  ↓
STEP 2: Organize Data
  ↓
STEP 3: Run Comparison Script
  ↓
STEP 4: Analyze Results
  ↓
STEP 5: Cross-Reference with CIPERB
  ↓
RESULT: Author identification
```

---

## Step 1: Obtain Manuscript Images

### Fontana Manuscripts (Digitized & Public)

**Secretum de thesauro** (Secret of Treasures)
- Source: Bibliothèque Nationale de France (Paris)
- URL: https://gallica.bnf.fr/ark:/12148/btv1b100331057.image
- What to capture:
  - Title page
  - First 3-5 pages (cipher notation examples)
  - Any colophons or signatures
  - Mathematical diagrams
  - High-resolution JPEGs (save to `data/fontana/secretum/`)

**Bellicorum instrumentorum liber** (Book of War Instruments)
- Source: Bayerische Staatsbibliothek (Munich)
- URL: https://www.digitale-sammlungen.de/en/details/bsb00013084
- What to capture:
  - Title page / colophon
  - Technical diagram pages (3-5 samples)
  - Any handwritten notes or annotations
  - Signature/authorship statements
  - High-resolution JPEGs (save to `data/fontana/bellicorum/`)

### Voynich Hand Samples

**Source:** Lisa Fagin Davis paleographic analysis (2020) or Beinecke digitized pages

Five hands to document:
1. **Main hand** (60-70% of text) — Multiple pages showing standard writing
2. **Hand B** — Representative pages from this scribe
3. **Hand C** — Representative pages
4. **Hand D** — Marginal notes/additions
5. **Hand E** — Rare pages

Save to `data/voynich/hands/` with naming convention:
- `voynich_main_hand_page_001.jpg`
- `voynich_hand_b_page_xxx.jpg`
- etc.

---

## Step 2: Organize Data Structure

```
Voynich/
├── data/
│   ├── fontana/
│   │   ├── secretum/
│   │   │   ├── title.jpg
│   │   │   ├── cipher_notation_01.jpg
│   │   │   ├── cipher_notation_02.jpg
│   │   │   └── ...
│   │   └── bellicorum/
│   │       ├── title.jpg
│   │       ├── diagram_01.jpg
│   │       ├── diagram_02.jpg
│   │       └── ...
│   └── voynich/
│       └── hands/
│           ├── voynich_main_hand_page_001.jpg
│           ├── voynich_hand_b_page_xxx.jpg
│           ├── voynich_hand_c_page_yyy.jpg
│           ├── voynich_hand_d_page_zzz.jpg
│           └── voynich_hand_e_page_www.jpg
├── analyses/
│   └── fontana_handwriting_comparison.py
└── results/
    └── (output goes here)
```

---

## Step 3: Run Comparison Script

Once images are organized in `data/` directory:

```bash
# Run the paleographic analysis
python3 analyses/fontana_handwriting_comparison.py \
    --fontana-dir ./data/fontana \
    --voynich-dir ./data/voynich \
    --output ./results/fontana_comparison.txt
```

**Output:**
- `results/fontana_comparison.txt` — Human-readable report
- `results/fontana_comparison.json` — Structured data for programmatic analysis

---

## Step 4: Analyze Results

### Comparison Matrix

The script generates a comparison table:

| Fontana Manuscript | Voynich Hand | Confidence | Key Matches |
|---|---|---|---|
| Secretum | Main hand | HIGH/MEDIUM/LOW | [specific features] |
| Secretum | Hand B | HIGH/MEDIUM/LOW | [specific features] |
| Secretum | Hand C | HIGH/MEDIUM/LOW | [specific features] |
| Bellicorum | Main hand | HIGH/MEDIUM/LOW | [specific features] |
| Bellicorum | Hand B | HIGH/MEDIUM/LOW | [specific features] |
| etc. | | | |

### What We're Looking For

**Confidence Level: HIGH** if:
- Multiple letter formations match (a, e, r, s, t)
- Abbreviation patterns align
- Flourish styles consistent
- Pen angle/pressure similar
- Cipher notation methods match

**Confidence Level: MEDIUM** if:
- Some letter formations match
- Some inconsistencies present
- Partial characteristic overlap

**Confidence Level: LOW** if:
- Few or no matching characteristics
- Inconsistent evidence

---

## Step 5: Cross-Reference with CIPERB

Once we have a strong Fontana match:

1. **Search CIPERB database** (Padua Medical Faculty 1409-1450)
2. **Find Fontana's enrollment record**
3. **Identify his classmates** (1415-1425 cohort)
4. **Look for documented collaborative work**
5. **Get handwriting samples** from his classmates

**Expected outcome:**
- Identify 4-5 collaborators who wrote the other Voynich hands
- Match each hand to a specific Padua medical student
- Create complete author roster

---

## Documentation

All findings to be documented in:
- `results/fontana_comparison.txt` — Main report
- `results/fontana_comparison.json` — Structured data
- `VOYNICH_AUTHOR_IDENTIFICATION_FINAL.md` — Comprehensive author analysis

---

## Current Status

✅ **Script created and ready to execute**  
⏳ **Waiting for:** High-resolution manuscript images  
📧 **Padua archives:** Email sent (waiting for Liber Rotuli response)  
🔍 **PHAIDRA:** Ready to search for Fontana records  
🗄️ **CIPERB:** Ready to access student prosopography  

---

## Timeline

- **Day 0 (now):** Script ready, waiting for images
- **Day 1-3:** Obtain manuscript images from digital repositories
- **Day 3:** Organize data and run comparison script
- **Day 4:** Analyze results
- **Day 5-7:** Cross-reference with CIPERB (waiting for Padua archive response)
- **Day 7+:** Compile final author identification report

---

## Success Criteria

✅ **Investigation Complete When:**
1. Fontana's handwriting matched to one of the 5 Voynich hands (HIGH confidence)
2. His 4-5 collaborators identified from CIPERB records
3. Each collaborator's handwriting matched to remaining Voynich hands
4. All findings documented with archival references
5. Final author roster published with confidence levels

---

## Next Action

1. Download Fontana manuscript images from digital repositories
2. Organize into `data/fontana/` directory structure
3. Get Voynich hand samples
4. Run: `python3 analyses/fontana_handwriting_comparison.py`
5. Document results and next steps

**Repository:** github.com/RN-Top/Voynich  
**Branch:** claude/voynich-validation-results-o797zw
