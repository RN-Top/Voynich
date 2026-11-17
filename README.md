# THE VOYNICH MANUSCRIPT INVESTIGATION

**Investigation Lead:** Erin Toppe  
**Paleographic Consultation:** Juan Gabriel Molina  
**Status:** OPEN INVESTIGATION — Structural analysis underway, no claims of decryption

---

## What This Investigation Is

An honest, rigorous exploration of whether the Voynich Manuscript (Yale Beinecke MS 408) shows measurable integration between its cipher text and botanical/illustrative elements.

**We are NOT claiming:**
- The manuscript is decrypted
- We have solved the cipher
- Fontana authored it (evidence is suggestive, not conclusive)
- Any decoded content is verified

**We ARE investigating:**
- Whether text and images are systematically integrated (structural analysis)
- Whether patterns in that integration are real or statistical artifact
- What methodology could lead to future breakthroughs

---

## The Core Hypothesis

**600 years of analysis failed because it was fragmented.**

Every researcher for 600 years approached the Voynich as two separate puzzles:
- **Approach 1:** Analyze TEXT alone (cipher symbols) → UNSOLVED
- **Approach 2:** Analyze IMAGES alone (plant illustrations) → UNSOLVED

**What if neither works alone because they're meant to work together?**

The hypothesis: The Voynich is ONE integrated cipher system where:
- Text layer + Image layer = complete information architecture
- Neither makes sense in isolation
- Both must be analyzed together

If this hypothesis is correct, standard cipher analysis (text-only) will fail—which matches 600 years of history.

---

## What We've Built

### 1. Real Data Files (from EVA transcription)
- **voynich_integrated.json** — All 226 folio pages/panels with:
  - Transcribed text from Data/Zl3b-n.txt (EVA format)
  - 37,642 total words | 8,673 unique vocabulary forms
  - Metadata: folio order, word counts, text classification
  - Linked to Yale Beinecke images

- **voynich_control.json** — Negative control dataset with:
  - Same 226 folio structure
  - Same word frequencies (preserved exactly)
  - Text shuffled across pages (breaks real relationships)
  - Purpose: Distinguish real integration from statistical artifact

### 2. Methodology
1. Extract folio structure from academic EVA transcription
2. Build integrated dataset preserving folio order and text-image co-location
3. Create negative control by shuffling text while preserving statistics
4. Compare analysis results on BOTH datasets
5. If real relationships exist, integrated data should show different patterns than control

### 3. Manuscript Data Source
- **Yale Beinecke MS 408** — The historical Voynich Manuscript
- 226 folio pages/panels (including foldout spreads)
- Downloaded from Yale's IIIF service (public access)
- Named by folio label (f1r, f1v, f2r, f2v, etc.)

---

## What's Verified ✓

### Structural Integration
- **226 pages/panels analyzed** from actual manuscript
- **100% have text** (all pages contain EVA transcription)
- **42 foldout panels** identified (f67r1-2, f68r1-3, f70r1-2, f72r1-3, f85r1-2, f86v3-6, f89r1-2, f90r1-2, f95r1-2, f102r1-2)
- **184 regular pages** with standard folio numbering
- **5,225 total text lines** extracted from EVA file

### Transcription Quality
- 0 parsing errors in EVA format
- All 226 folio IDs found in source file
- Text/folio mapping verified against academic standard (ZL3b-n.txt)

### Dataset Integrity
- **voynich_integrated.json:** 37,642 words | 8,673 unique forms
- **voynich_control.json:** 37,642 words | 8,673 unique forms (identical)
- Word frequencies preserved exactly in control file
- Control successfully breaks text-image relationships while keeping statistics realistic

---

## What Remains Open

### Functional Decryption
- No reproducible cipher system demonstrated
- No readable plaintext produced
- No validation against historical records

### Authorship
- Fontana's documented cipher systems show architectural similarities to Voynich structure
- Paleographic analysis (Molina) suggests possible handwriting match
- Historical evidence of Fontana's cipher expertise is documented
- **BUT:** None of this constitutes proof of authorship

### Content Validation
- No decoded passages verified against historical sources
- No independent confirmation from other researchers
- No validation of medical/pharmaceutical content

---

## For Researchers

If you have expertise in:
- **Cryptanalysis** — Test hypotheses on our integrated vs. control datasets
- **Paleography** — Examine handwriting against Fontana's documented manuscripts
- **Medieval Latin** — Check if any patterns suggest recognizable language
- **History** — Verify authorship claims or content authenticity
- **Statistics** — Validate our integration analysis methodology

**Please review our work and provide feedback.** This is an open investigation.

---

## Repository Contents

- **Data/Zl3b-n.txt** — Academic EVA transcription (Takeshi Takahashi format)
- **voynich_integrated.json** — All 226 pages with real text and structure
- **voynich_control.json** — Negative control with shuffled text
- **build_integrated.py** — Generates integrated dataset from EVA file
- **build_control.py** — Generates control dataset with shuffled words
- **analyze_eva_structure.py** — Analyzes EVA file structure
- **images/yale/** — Downloaded Voynich page images (Yale Beinecke MS 408)
- **app.py** — Streamlit investigation interface

---

## How to Run

### View the Investigation
```bash
streamlit run app.py
```

### Regenerate Datasets
```bash
python3 build_integrated.py
python3 build_control.py
```

### Download Images
```bash
python3 fetch_yale_images.py        # Full resolution (~500 MB)
python3 fetch_yale_images.py --width 1500  # Smaller size
```

---

## A Note on Previous Claims

Earlier versions of this repository contained claims of complete decryption and solved authorship. Those claims were not substantiated and have been removed. This version reflects honest investigation status: **open questions, real data, and no false certainty.**

---

**Last Updated:** November 17, 2026  
**Investigation Status:** Ongoing — data ready for analysis
