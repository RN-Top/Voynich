# Pre-registration: do word beginnings follow what the label is attached to?

Committed 2026-10-02, **before** the tests below are run. Amend only below the line at the end.

## Background

`output/writing_types_report.md` found that word beginnings (first 2 letters) track the page's topic more than
endings do. If the script is a made-up or real language whose word beginnings mark meaning categories, labels
on different **kinds of picture** should start differently, even on the same pages.

## Data

ZL3b label loci, by the transcription's own picture codes:

| Code | Attached to | Pages |
|---|---|---|
| Lc | jars / containers | pharmaceutical (f88–f102) |
| Lf | plant parts (roots, leaves) | the same pharmaceutical pages |
| Ln | bathing figures | biological (f75–f84) |
| Lt | pools / tubes | the same biological pages |

Each label's first word is used. Beginning = first 2 letters, ending = last 2 letters.

## Tests

**D1.** Pharmaceutical pages: jar labels vs plant-part labels.
**D2.** Biological pages: figure labels vs pool/tube labels.

Statistic: mutual information between word beginning and picture kind. Null: picture kinds shuffled among the
labels **on the same page** (10,000 shuffles, seed 20261002), so page, section and scribe cannot explain it.
Threshold p < 0.005 for each (0.01 split over two tests). The same test is run on endings for comparison, and
reported but not used for the verdict.

## Decision

- **Supported:** D1 and D2 both pass.
- **Partly supported:** one passes.
- **Not supported:** neither.

## Descriptive (not tested)

Candidate dictionary list: for each picture kind, the beginnings most over-represented on it (counted at least
3 times), and for paragraph text, the beginnings most concentrated in each section relative to their Currier
language. These are leads to check, not readings.

---
Amendments (dated, below this line only):
