# Pre-registration: plant-name cribs (opening word = plant name?)

Date: 2026-10-04. Written before any plant is identified for this test and before any opening word is compared
with a plant name.

## Idea

Most decipherments begin with names (Linear B began with place names). In medieval herbals, the first word of a
plant's entry is usually its name. If the Voynich herbal openings are plant names in a real language, then for
plants we can identify from the drawings, the opening word should sound like that plant's period name.

## Step 1: identification, without looking at the text

- Erin and Claude independently identify herbal plants from the full-resolution Yale images (`images/yale/`), and
  each records a confidence of high, medium or low.
- Only plants that **both** identify alike with at least medium confidence go forward.
- The identifications are committed to `analyses/plant_ids.csv` **before** any opening word is compared.

## Step 2: candidate names, fixed before comparison

- For each identified plant, list its period names in Latin, Italian, German, Catalan/Occitan and French, from
  standard herbal synonymies. They are written to `analyses/plant_names.csv` and committed before Step 3.

## Step 3: test

**Similarity.** A letter mapping from Voynich glyphs to sounds must be consistent across plants: one glyph maps to
one sound. Score how well the opening words fit their own plant's names under a single shared mapping, chosen by
hill-climbing.

**Null.** Repeat the same fit with the plant labels shuffled among the pages. If a single mapping fits the true
pairing much better than shuffled pairings, that is evidence.

**Threshold and size.** p < 0.01. At least 8 plants are needed for the test to run.

## Weaknesses

- Plant identifications are disputed, and wrong IDs dilute the signal toward the null.
- With a free mapping, short words can match almost anything. The shuffle null controls for that only if the
  search effort is the same for real and shuffled pairings, so the same number of hill-climbing restarts is used
  for each.

## Amendment (2026-10-04): the second opinion

Only 4 plants were agreed between Erin and Claude, so published identifications collected from voynich.nu (Th. Petersen, O'Neill, Holm and ELV) and Wikibooks were added as the second opinion (`analyses/plant_ids_published.csv`). A plant counts as agreed when two of the three sources (Erin, Claude, published) name the same plant. That gives 8 plants (`analyses/plant_ids_agreed.csv`).

**Weakness.** Claude's identifications may not be independent of the published ones, because Claude may have seen them in training. The 4 plants where Erin also agrees are the strongest.

## Amendment (2026-10-04): names and exact test, fixed before any comparison

**Names.** The period names in Latin, Italian, German, Catalan/Occitan and French are in `analyses/plant_names.csv`. They are written down from standard synonymies, before any comparison with the Voynich text.

**Opening words.** The first word of each page, cleaned from ZL3b:

| Page | Opening word |
|---|---|
| f9v | fochor |
| f16r | pocheody |
| f6v | koary |
| f2v | kooiin |
| f2r | kydainy |
| f15v | poror |
| f42r | cho (rare glyph @155 dropped) |
| f32v | kcheodaiin |

**Glyph units.** Each opening word is split into units: ch, sh, cth, ckh, cph, cfh, ee and ii are single units, and every other EVA character is its own unit.

**Mapping.** One mapping sends each unit to a letter a–z or to nothing. The same mapping is used for all 8 pages.

**Score.**
- For a page, take max over its names of 1 − Levenshtein(mapped word, name) / max(length).
- The score is the mean of that over the 8 pages.
- Names are lowercased, with spaces and apostrophes removed.

**Search.** Hill-climbing, 4 restarts × 1,500 single-unit changes, keeping a change if it does not lower the score.

**Null.** The same search with the name lists shuffled among the 8 pages (random derangements). 200 shuffles, with the same search effort as the real run, seed 20261014.

**Result.** p = (shuffles scoring at least the real score + 1) / 201. Threshold p < 0.01.

**Secondary (descriptive).** The same test on the 4 three-way-agreed plants only.
