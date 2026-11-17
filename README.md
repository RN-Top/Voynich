# The Voynich Manuscript Investigation

**Status: open investigation.** No reading of the text and no author has been confirmed.

Investigation lead: Erin Toppe
Paleographic consultation and independent review: Juan Gabriel Molina

This repository is a working notebook. It follows several lines of inquiry at once, records failed tests next to
successful ones, and does not commit to a single answer. Each line below has its own status and its own files.

**Goals:**
1. Describe how the Voynich text is built, using tests that are fixed before they are run.
2. Identify who made the manuscript.
3. Eventually, read it.

---

## Lines of inquiry

| Line | Question | Status |
|---|---|---|
| [1. Text structure](#1-text-structure) | How do Voynich words and lines behave? | Several results hold up |
| [2. Stars, zodiac and calendar](#2-stars-zodiac-and-calendar) | Do the astronomical pages carry a calendar, star names or an instrument? | One lead and many negative results |
| [3. Text and pictures](#3-text-and-pictures) | Is the text tied to the drawings on its page? | Mixed |
| [4. Authorship: Giovanni Fontana](#4-authorship-giovanni-fontana) | Did Fontana, or his cipher system, produce the manuscript? | Open hypothesis, not demonstrated |
| [5. Authorship: other candidates and context](#5-authorship-other-candidates-and-context) | Who else fits the time, place and medical content? | Open |
| [6. Decryption attempts](#6-decryption-attempts) | Does any proposed key give readable text? | None demonstrated |

---

### 1. Text structure

Tests on the ZL3b transliteration (`Data/Zl3b-n.txt`), parsed by `parser.py`. These describe the text. They do
not decode it.

- **-m / -am is a line-end form.** 605 of 861 -m/-am words are line-final (p ≈ 5e-5), confirmed by an independent
  sample.
- **Word order carries information,** beyond line-start and line-end habits (p = 0.001).
- **Set phrases and a grammar link.** Word pairs bind about three times more strongly than in shuffled text, and a
  word's ending predicts the next word's beginning (for example -dy → qok-).
- **Rare symbols cluster in first lines,** about four times more than chance, which fits decorated initials.
- **Not supported:** the C→L→P→R cycle beyond Markov structure, the published glosses, Fibonacci counts,
  "o" as a name-forming prefix.

Details: [FINDINGS.md](FINDINGS.md), [VALIDATION.md](VALIDATION.md), [REPLICATION.md](REPLICATION.md).
Scripts: `structural_validation.py`, `blind_holdout.py`, `transfer_test.py`, `test_*.py`.

### 2. Stars, zodiac and calendar

About 20 pre-registered tests on the astronomical pages (f67–f73).

- **Lead:** herbal-page opening words share rare word roots with the star labels on f67r2 and f68r1–3. 13 of 116
  match, against 4.4 expected (p = 0.0002), and the result holds with a matched control. Example: koaiin ~ okoaly.
- **Weak:** zodiac labels farther apart on a wheel are slightly less alike (p = 0.0009). A scribe drifting while
  writing around the wheel would give the same result.
- **Suggestive only:** f67r2's red and gold moons alternate at 10 of 12 steps (p = 0.067). On the spring signs, 74%
  of figures stand in tubs, against 1% on the rest (described after looking).
- **Not supported:** zodiac labels as day names, an astrolabe or volvelle, a star-name crib, moon phases, the 28
  lunar mansions, the 19-year Metonic cycle, golden numbers, week or month cycles in the starred paragraphs, a
  planetary metal key.

Details: [VALIDATION.md](VALIDATION.md), [IMAGE_NOTES.md](IMAGE_NOTES.md).

### 3. Text and pictures

- Nearly every page carries both text and drawings (212 of 214 pages in `VOYNICH_INTEGRATED_COMPLETE.json`).
  `build_integrated.py` and `build_control.py` build the dataset and a shuffled control for testing it.
- Plant and star names share roots (line 2), and bath openings share roots with pharmacy labels (p = 0.00005).
- **Not supported:** labels repeated in their own page's text, label beginnings by picture type, pharmacy parts
  naming the same plant as their herbal page.

Files: `fontana_image_text_integration.py`, `IMAGE_TEXT_INTEGRATION_EXTRACTION.md`, `src/spot_pies.py`.

### 4. Authorship: Giovanni Fontana

Giovanni Fontana (Padua, degrees 1418 and 1421) was a physician who wrote in cipher, and his dates fit the
radiocarbon range of the parchment (1404–1438). This makes him a candidate worth testing.

- **What exists:** his cipher in *Secretum de thesauro*, mapped in `fontana_cipher_mapping.json`. The Voynich's
  ratio of circle to geometric symbols (9.8:1) is close to his (about 9:1).
- **What is not shown:** applying his cipher to Voynich text has not produced readable Latin, and handwriting
  comparison is not finished.

Files: the `FONTANA_*` documents and `fontana_*.py` scripts, `LETTER_ANALYSIS_BL_vs_FONTANA.md`,
`BRITISH_LIBRARY_*` (BL MS 635), `LJS51_*` (Penn LJS 51), `MOLINA_COLLABORATION.json`.

### 5. Authorship: other candidates and context

The medical content points to someone trained in university medicine around 1410–1430.

- Padua and other medical student groups of the period: `CANDIDATE_MEDICAL_STUDENT_GROUPS.md`,
  `MEDICAL_STUDENT_COHORTS_RESEARCH.md`, `documented_students_1410_1430.md`.
- The Rhazes and university-curriculum thread: `VOYNICH_RHAZES_CONNECTION_SUMMARY.md`,
  `VOYNICH_AUTHOR_UNIVERSITY_TRAINING.md`, `PRIMARY_SOURCE_CHAIN.md`.
- Medical vocabulary from the Book of Fermoy for comparison: `fermoy_ms23e29.txt`, `extract_fermoy_*.py`.
- Archive access and leads still to check: `CIPERB_ACCESS_RESEARCH_REPORT.md`, `IMMEDIATE_ACTION_PRIMARY_SOURCES.md`.

What counts as verified so far is tracked in `VERIFIED_VS_UNVERIFIED_FINDINGS.md`.

### 6. Decryption attempts

Scripts such as `decipher_voynich.py`, `full_decryption.py` and `complete_voynich_decryption.py` record approaches
that were tried. **None has produced a verified reading.** Earlier "fully decrypted" outputs were removed because
they could not be verified. The 90.2% blind prediction, 99.79% Macer Floridus and Δ = −1.018 claims were withdrawn
(see [VALIDATION.md](VALIDATION.md)).

---

## How this investigation works

- **Fix the test before running it.** The prediction, statistic, null model and threshold are committed before
  the first run.
- **Record every result.** Negative results and design mistakes stay in [VALIDATION.md](VALIDATION.md).
- **Keep authorship open.** A candidate stays a hypothesis until a test that could fail supports it.

Note: the detailed pre-registrations, test code and reports (`analyses/`, `output/`, `archive/`) were removed in the
13 October 2026 cleanup (commit `3522d65`). They are still in the git history before that commit.

## Help wanted

1. An independent check of the structural results (see [REPLICATION.md](REPLICATION.md)).
2. Has the plant-name / star-label root link been reported before?
3. Paleographers who can compare the Voynich hands with Fontana's and with other Padua-trained physicians.
4. Historians of 15th-century medicine and astronomy.
5. Criticism of the methods.

## Getting started

```bash
pip install -r requirements.txt
python structural_validation.py   # main structural tests
streamlit run app.py              # interactive app
```

*Last updated: 17 November 2026*
