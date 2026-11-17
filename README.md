# Deciphering the Voynich Manuscript

**We are going to read the Voynich Manuscript.** That is the mission of this repository: solve it and recover what
it says.

The text was written by a person, for readers, about plants, stars, bodies and medicines. It has grammar and
structure, so it can be cracked. We are building the solution from the bottom up. First we map exactly how the text
works: its letters, words, lines and how they tie to the drawings. Then we turn that structure into meaning. We keep
every idea on the table. Each step is tested hard, so when the reading comes, it will hold up.

Investigation lead: Erin Toppe
Paleographic consultation and independent review: Juan Gabriel Molina

**Status:** the structure is largely mapped, and the first bridges from text to meaning are found. Next: turn those
bridges into readable words.

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

## Supporting lines: who wrote it and where

Knowing the author's world (language, training, books) narrows what the text can mean.

- **Giovanni Fontana** (Padua physician and cipher writer, degrees 1418 and 1421). His dates fit the parchment's
  radiocarbon range (1404–1438), and his cipher in *Secretum de thesauro* is mapped in `fontana_cipher_mapping.json`.
  Applying it has not produced readable text yet, and the handwriting comparison isn't finished. Files: `FONTANA_*`,
  `fontana_*.py`, `LETTER_ANALYSIS_BL_vs_FONTANA.md`, `BRITISH_LIBRARY_*`, `LJS51_*`.
- **Medical students around 1410–1430**, at Padua and elsewhere: `CANDIDATE_MEDICAL_STUDENT_GROUPS.md`,
  `MEDICAL_STUDENT_COHORTS_RESEARCH.md`, `documented_students_1410_1430.md`.
- **The medical tradition it may draw on** (Rhazes, university curriculum, the Book of Fermoy):
  `VOYNICH_RHAZES_CONNECTION_SUMMARY.md`, `VOYNICH_AUTHOR_UNIVERSITY_TRAINING.md`, `PRIMARY_SOURCE_CHAIN.md`,
  `fermoy_ms23e29.txt`.

What counts as verified so far: `VERIFIED_VS_UNVERIFIED_FINDINGS.md`.

---

## How we work

- **Fix the test before running it.** The prediction, statistic, null model and threshold are committed first.
- **Keep every result.** Failed tests stay in [VALIDATION.md](VALIDATION.md) next to the ones that passed.
- **Meaning has to predict.** A proposed reading counts only if it works on pages it wasn't built from.

The detailed pre-registrations, test code and reports (`analyses/`, `output/`, `archive/`) were removed in the
13 October 2026 cleanup (commit `3522d65`). They are still in the git history before that commit.

## Data

- `Data/Zl3b-n.txt`: the ZL3b transliteration (IVTFF).
- `voynich_integrated.json`: every folio in book order with its text, built by `build_integrated.py`. Its image
  slots are still empty. `voynich_control.json` is the shuffled control built by `build_control.py`.
- Page images: Yale Beinecke MS 408, https://collections.library.yale.edu/catalog/2002046

## Help wanted

1. An independent check of the structural results ([REPLICATION.md](REPLICATION.md)).
2. Has the plant-name / star-label root link been reported before?
3. Help identifying the herbal plants, and medieval herb–star tables to test against.
4. Historians of 15th-century medicine and astronomy, and paleographers.

## Getting started

```bash
pip install -r requirements.txt
python structural_validation.py   # main structural tests
streamlit run app.py              # interactive app
```

*Last updated: 17 November 2026*
