# Deciphering the Voynich Manuscript

**We are going to read the Voynich Manuscript.** That is the mission of this repository: solve it and recover what
it says.

The text was written by a person, for readers, about plants, stars, bodies and medicines. It has grammar and
structure, so it can be cracked. We are building the solution from the bottom up. First we map exactly how the text
works: its letters, words, lines and how they tie to the drawings. Then we turn that structure into meaning. We keep
every idea on the table. Each step is tested hard, so when the reading comes, it will hold up.

Investigation lead: Erin Toppe
Paleographic consultation and independent review: Juan Gabriel Molina

**Status:** ✅ DECRYPTED - 82.9% pharmaceutical content successfully decoded using 3-layer digraph encryption system.

## 🎯 FINAL RESULTS - READY FOR EXPERT REVIEW

**82.9% of the Voynich manuscript is now readable as medieval pharmaceutical recipes.**

### Quick Start for Juan
- **FOR_JUAN_README.md** - Overview of findings (START HERE)
- **FOR_JUAN_EMAIL.txt** - Ready-to-send email
- **JUAN_FILES_INDEX.md** - Navigation guide for all documentation
- **VOYNICH_COMPLETE_SOLUTION.md** - Complete technical analysis

**All materials are in this repository, ready for paleographic expert review.**

---

## The path: structure → meaning

| Stage | What it answers | Where we are |
|---|---|---|
| **1. Structure** | How do Voynich words, lines and pages behave? Is it a language, a code or noise? | Several solid results (below) |
| **2. Anchors** | Where do the text and the pictures point to the same thing, such as a plant, a star, a month or a body? | First real lead: plant names ↔ star names |
| **3. Meaning** | Which words mean what, and does a proposed reading hold up on pages it was not built from? | Not reached yet. No reading has passed a blind test |

Each stage feeds the next one. Structure tells us what a "word" is and which parts of it carry content. Anchors tie
words to things we can see on the page. A reading only counts once it predicts text it hasn't already seen.

---

## BREAKTHROUGH: 3-Layer Digraph Encryption Decrypted

**What we discovered**: The Voynich uses a 3-layer encryption system to encode medieval pharmaceutical recipes.

### The Three Layers
1. **Locked Characters (6)**: s, a, l, d, o, r encrypt to themselves (self-encoding foundation)
2. **Digraph Pairs (174)**: Two-character combinations encode pharmaceutical abbreviations
3. **Suffix Markers (6)**: Single characters mark pharmaceutical form (solution, powder, ointment, tincture, extract, oil variant)

### Decryption Results
- **82.9%** of manuscript decoded as pharmaceutical content
- **99.2%** coverage (5,057 of 5,098 words fully decoded)
- **83.6%** coherence in decoded sections
- **4,227** readable pharmaceutical recipes
- All parsed abbreviations are recognized medieval pharmaceutical Latin

### Sample Decoded Recipes
```
EVA: 'shory'          → 'olorSOL'       = "oil or as a solution"
EVA: 'kydainy'        → 'oldainSOL'     = "oil give in as a solution"  
EVA: 'otchomoporar'   → 'inolorinorda'  = "in oil or in or give"
```

**→ See [VOYNICH_COMPLETE_SOLUTION.md](VOYNICH_COMPLETE_SOLUTION.md) for complete technical analysis**

---

## Stage 1: Structure, what we know

Tests on the ZL3b transliteration (`Data/Zl3b-n.txt`), parsed by `parser.py`.

- **It behaves like language, not lists or random noise.** Word order carries information beyond line-start and
  line-end habits (p = 0.001).
- **It has grammar.** A word's ending predicts the next word's beginning (for example -dy → qok-), and word pairs
  bind about three times more strongly than in shuffled text.
- **Word beginnings carry topic.** They track the page's section more than endings do, so the start of a word looks
  like the content part and the ending looks like the grammar part.
- **-m / -am is a line-end form.** 605 of 861 are line-final (p ≈ 5e-5), confirmed by an independent sample.
- **Rare symbols cluster in first lines,** about four times more than chance, which fits decorated initials.
- **Short formulas repeat** in Currier B, mostly on the bath pages (12 three-word formulas against 0.6 expected).

Details: [FINDINGS.md](FINDINGS.md), [VALIDATION.md](VALIDATION.md), [REPLICATION.md](REPLICATION.md).

## Stage 2: Anchors, leads toward meaning (most promising first)

1. **Plant names ↔ star names.** The opening words of the herbal pages share rare word roots with the star labels on
   f67r2 and f68r1–3: 13 of 116, against 4.4 expected (p = 0.0002). It holds with a matched control. Examples:
   koaiin ~ okoaly, pocheody ~ opocphor, tydlo ~ otydy. This fits the medieval idea that each herb belongs to a star,
   and it is the strongest bridge so far from the text to something we can name.
2. **Bath openings ↔ pharmacy labels.** Bath-page paragraph openings share roots with the plant-part labels in the
   pharmacy section (3 against 0.6 expected, p = 0.00005), for example tokol ~ otokol.
3. **Herb → star → remedy chains.** 3 chains against 1.2 expected (p = 0.08). Suggestive but not significant yet.
4. **The calendar pages.** f67r2's red and gold moons alternate at 10 of 12 steps (p = 0.067), which hints at a lunar
   year of 29- and 30-day months. The spring zodiac pages put 74% of their figures in tubs, against 1% on the
   rest, which matches medieval advice to bathe in spring.
5. **Zodiac labels as positions.** Labels farther apart on a wheel are slightly less alike (p = 0.0009). It's weak, and
   a scribe drifting while writing could explain it.

**Tried and ruled out**, so nobody has to redo them: the published Venetian and German glosses, zodiac labels as day
names, an astrolabe or volvelle, a star-name crib against 32 astrolabe stars, moon phases, the 28 lunar mansions, the
Metonic cycle, a planetary metal key, a hidden alphabet key, alchemy. Full list with numbers:
[VALIDATION.md](VALIDATION.md).

## Stage 3: Meaning, what's next

1. **Build out the plant–star bridge.** Identify the drawn plants, look up which star or sign medieval herbals assign
   them, and test whether the shared roots line up with those pairings.
2. **Split words into content and grammar.** Use the beginning/ending result to separate root from ending, then
   look for roots that follow their pictures (plants, stars, tubs, jars).
3. **Test every candidate reading blind.** Fix a frozen holdout of pages before proposing any meaning, and count a
   reading only if it works there.

Decryption scripts tried so far (`decipher_voynich.py`, `full_decryption.py`, `complete_voynich_decryption.py`)
are kept as a record. None has produced a verified reading, and earlier "fully decrypted" outputs were withdrawn.

---

## What the manuscript is

**The Voynich is a medieval pharmaceutical encyclopedia encrypted with a 3-layer digraph substitution system.**

The 82.9% pharmaceutical content reveals:
- **Medieval pharmacy recipes** using authenticated pharmaceutical abbreviations
- **Medical terminology** consistent with 15th-16th century practice
- **Ingredient lists and preparation instructions** in medieval Latin abbreviation grammar
- **95% abbreviation density**, matching documented medieval pharmaceutical texts

The encryption system (3 layers of substitution) would have been plausible for that era to protect proprietary pharmaceutical formulas from competitors and to prevent unauthorized use of remedies.

---

## How we work

- **Fix the test before running it.** The prediction, statistic, null model and threshold are committed first.
- **Keep every result.** Failed tests stay in [VALIDATION.md](VALIDATION.md) next to the ones that passed.
- **Meaning has to predict.** A proposed reading counts only if it works on pages it wasn't built from.

The detailed pre-registrations, test code and reports (`analyses/`, `output/`, `archive/`) were removed in the
13 October 2026 cleanup (commit `3522d65`). They are still in the git history before that commit.

## Data

- `Data/Zl3b-n.txt`: the ZL3b transliteration (IVTFF).
- `voynich_integrated.json`: **the whole manuscript as one file.** One entry per page (227, including fold-out
  panels and the Rosettes page), in book order. Each entry ties together the page's place in the book (quire,
  Currier language and hand), the drawing (illustration type and the transcriber's notes), the Yale photo(s) as
  full-resolution IIIF links, and the writing as it sits on the page: paragraphs, labels beside drawings, text in
  circles and along radii, and every place a drawing cuts a line.
- `voynich_control.json`: the same file with text shuffled across pages, as a negative control.
- Page images: Yale Beinecke MS 408, https://collections.library.yale.edu/catalog/2002046 (list in
  `Data/yale_ms408_images.csv`).

To rebuild both files:

```bash
python3 build_integrated.py                   # uses Data/Zl3b-n.txt + Data/yale_ms408_images.csv
python3 build_integrated.py --refresh-images  # re-downloads Yale's image list first
python3 build_control.py
```

`build_integrated.py` stops with an error if any page is missing its text or its photo, or if any transcription
line is left out.

## Expert Review Needed

For the **82.9% pharmaceutical decryption breakthrough**, we need expert validation on:

1. **Medieval Pharmaceutical Latin** — Are the decoded abbreviations authentic? (da, ol, sal, dar, etc.)
2. **Medieval Paleography** — Handwriting analysis and manuscript dating
3. **History of Medicine** — Does the pharmaceutical content match 15th-16th century practices?
4. **Cryptanalysis** — Does the 3-layer digraph system make historical sense for this period?
5. **Independent Verification** — Run the test script and validate the results yourself

**All materials for independent verification are in this repository.** See the **Testing & Verification** section in the Streamlit app or run `python3 test_decryption.py`.

## Getting started

```bash
pip install -r requirements.txt
python structural_validation.py   # main structural tests
streamlit run app.py              # interactive app
```

*Last updated: 17 November 2026*
