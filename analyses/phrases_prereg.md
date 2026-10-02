# Pre-registration: repeated phrases and how words link

Committed 2026-10-02, **before** the tests below are run. Amend only below the line at the end.

## Background

`output/writing_types_report.md` found that word order carries information. If the text is a language
(natural or made up), part of that should come from **set phrases** (word pairs that go together far more
often than chance), and from **grammar links** (one word's form constraining the next word's form).

## Data

Paragraph text, Currier A and Currier B analysed separately. As before, only **interior** neighbouring pairs
are used (neither word first or last on its line), so line-layout habits are excluded.

## R1. Set phrases

A pair (word1, word2) is a **set phrase** if it occurs at least 5 times and at least 3 times as often as
expected from the two words' frequencies. Statistic: the number of distinct set phrases. Null: interior words
shuffled within each line (1,000 shuffles, seed 20261002). Pass: p < 0.01, for A and for B separately.

## R2. Grammar links

For each interior pair, take the first word's beginning and ending (first and last 2 letters) and the same for
the second word. Four links are measured, as mutual information with the same within-line shuffle as the null:

1. ending of word 1 → beginning of word 2
2. ending of word 1 → ending of word 2
3. beginning of word 1 → beginning of word 2
4. beginning of word 1 → ending of word 2

Each link with p < 0.01 counts as real. Links are ranked by excess over the null. The strongest link shows
which parts of neighbouring words depend on each other. In many languages that is agreement between endings
(link 2), or an ending choosing the next word (link 1).

## Descriptive

The top set phrases (by count) and the most frequent three-word sequences, with the sections they occur in.
These are candidates for formulas, not readings.

---
Amendments (dated, below this line only):

**2026-10-02, results.** R1 PASS in A (16 vs 4.8) and B (100 vs 28.7), p = 0.001. R2: all four links are real
in B. In A, links 1–3 are real (link 4 p = 0.022). The strongest link is ending → next beginning, in both A
and B. An extra check (labelled) with uncertain spaces unsplit gives the same conclusions. Write-up:
`output/phrases_report.md`.
