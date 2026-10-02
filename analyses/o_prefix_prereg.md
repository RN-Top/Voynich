# Pre-registration: is "o" a label/name-forming prefix?

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Background

`output/plant_star_report.md` and `output/name_map_report.md` found labels of the form "o" + paragraph-opening word
(tokol → otokol, koaiin ~ okoaly). If "o" is a prefix that turns a word into a label or name, then **label** words
starting with "o" should, more often than **paragraph** words starting with "o", be "o" + an existing word.

## Data (ZL3b; word reading as in analyses/plant_star_test.py, rare symbols kept)

- **Label types:** distinct words from all label loci (L…) that start with "o" and have at least 4 letters.
- **Paragraph types:** distinct words from paragraph loci (P) that start with "o" and have at least 4 letters, and
  that never occur in labels.
- **Paragraph vocabulary:** all distinct paragraph words.

A word is **"o + word"** if the word without its first letter is in the paragraph vocabulary.

## Test

Statistic: the number of label types that are "o + word". Null: the label/paragraph membership is shuffled among
all the "o" words, **within each word length** (10,000 shuffles, seed 20261002). The number of label types at each
length stays fixed. Pass: p < 0.01.

## Descriptive

- Rates for labels and for paragraph words, by label group (stars, zodiac, bath figures, pools, jars, plant parts,
  other).
- The most common remainders (the word left after removing "o"), and where in paragraphs those remainders occur:
  share that are line-first or paragraph-first, against the same share for all paragraph words.

---
Amendments (dated, below this line only):

**2026-10-02, results.** 175 of 430 label o-words (41%) are o + word, against 182.6 expected from length-matched
paragraph o-words (39%). p = 0.84. **Not supported**: "o" is a general prefix, not a label-forming one. Write-up:
`output/o_prefix_report.md`.
