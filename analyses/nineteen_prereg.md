# Pre-registration: is there a 19 (Metonic, golden-number) structure in the diagrams?

Committed 2026-10-03, **before** the search below is run. Amend only below the line at the end.

## Idea (from the project author)

The moon's 19-year (Metonic) cycle, 19 years = 235 lunar months ≈ 6,940 days, underlies the medieval "golden
numbers" 1–19. If the book tracks it, a diagram might have 19 divisions, or a ring text might repeat with period 19.

## Part 1: counts (descriptive)

For every page with ring (C), radial (R) or label (L) loci: the number of ring loci, radial loci and label loci
(by label type), and the number of words in each ring locus. All counts equal to 19, 235 or 6,940 are listed. Small
numbers turn up by chance, so a count of 19 is only noted as a lead, together with how many counts were examined.

## Part 2: period-19 repetition in ring texts (test)

Each ring locus is read as a sequence of tokens, in two ways: words, and single glyphs (rare `@nnn` symbols count as
one glyph). For lag k, the statistic is the number of positions i where token[i] = token[i+k], summed over all ring
loci. Null: tokens shuffled within each ring locus, 10,000 times, seed 20261003.

- **Positive control (must pass for the method to count):** f57v ring, glyph level, lag 17 (ZL3b notes a 17-symbol
  sequence repeated 4 times). Pass at p < 0.01.
- **N1:** all ring loci, word level, lag 19. Pass: p < 0.005.
- **N2:** all ring loci, glyph level, lag 19. Pass: p < 0.005.

If the control fails, N1 and N2 are reported as uninformative.

---
Amendments (dated, below this line only):
