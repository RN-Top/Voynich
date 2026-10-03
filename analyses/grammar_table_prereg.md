# Pre-registration: is the ending → next-beginning grammar the same for every scribe?

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Background

For scribes 1, 2 and 3 the strongest link between neighbouring words is a word's ending → the next word's
beginning (`output/scribes_report.md`). This builds that link as a table, separately for each scribe, and asks
whether the scribes share the **same** table (one grammar) or each has their own.

## Data

Paragraph text, interior word pairs only (neither word first or last on its line), for scribes 1, 2 and 3.
- Ending of word 1: its ending class from `structural_validation.ending_of` (am, m, eedy, edy, eey, ey, dy, aiiin,
  aiin, ain, or, ar, ol, al, y, or "?").
- Beginning of word 2: its first two letters.

## Statistic

For each scribe, lift(e, b) = observed / expected count of the pair (ending e, next beginning b), where expected
comes from the scribe's own margins. Only cells observed at least 10 times for **both** scribes in a comparison
are used. For each pair of scribes: Pearson correlation of log lift over those cells.

## Test

Null: interior words shuffled within lines for both scribes (1,000 shuffles, seed 20261003), with the same cell
selection and correlation. Pass: p < 0.01/3 for each scribe pair. **Shared grammar** if all three pairs pass.

## Descriptive

The grammar table: for each common ending, the next beginnings with the highest lift (count at least 10), shown per
scribe side by side, plus split-half correlations within each scribe (odd and even pages) for comparison.

---
Amendments (dated, below this line only):
