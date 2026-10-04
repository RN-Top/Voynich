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
