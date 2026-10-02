# Pre-registration: does the text repeat longer phrases, like prayers, charms or refrains?

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Idea (from the project author)

The book may serve a larger spiritual purpose. A meaning-free trace of ritual or devotional writing (prayers,
charms, blessings, litanies) is the repetition of **longer** word sequences: refrains and set invocations.
`output/phrases_report.md` already found short set phrases (pairs). This asks about 3- and 4-word runs.

## Data

Paragraph text (locus P), Currier A and Currier B separately. Sequences are counted within lines only. A sequence
must contain at least 2 different words, so plain repetition such as "qokedy qokedy qokedy" does not count.

## Tests

- **L1 (3 words):** number of distinct 3-word sequences occurring 3 or more times.
- **L2 (4 words):** number of distinct 4-word sequences occurring 2 or more times.

Null: words shuffled within each line (1,000 shuffles, seed 20261002). This keeps every line's words but
removes their order. Threshold p < 0.005 per test (0.01 split over A and B).

## Decision

- **Supported (longer refrains present):** L2 passes in A or B.
- **Partly supported:** L1 passes but L2 does not.
- **Not supported:** neither passes.

## Descriptive

The most repeated 3- and 4-word sequences, and the share of their occurrences in each section compared with
that section's share of the text. This shows whether repeats cluster in the bath and recipe pages.

A positive result shows formulaic, refrain-like writing. That is typical of ritual text, but also of recipes and
instructions, so it cannot by itself prove a spiritual purpose.

---
Amendments (dated, below this line only):

**2026-10-02, results.** L1 PASS in B (12 vs 0.6, p = 0.001), FAIL in A (0). L2 FAIL in both (B: 1 vs 0.2,
p = 0.16). **Partly supported**: short 3-word formulas, concentrated on the Biological pages, and no long
refrains. Write-up: `output/refrains_report.md`.
