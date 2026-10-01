# Pre-registration: is line-final -m/-am a space-saving device?

Committed before any code for this test was written or run. Do not edit after the first run;
add amendments below the line at the end, with a date.

## Hypotheses

- **H_space (abbreviation / compression):** the scribe used -m/-am to save room when a line was
  full, as medieval scribes did with abbreviations at line ends.
- **H_term (terminator):** -m/-am marks the end of a unit (sentence, entry, paragraph), regardless
  of how full the line is.

## Data

Paragraph text only (IVTFF locus type P), canonical `parser.parse_zl3b()`, lines of 2 or more tokens.
A paragraph-final line is one whose source text contains `<$>`. Glyph length means the number of EVA
characters in the cleaned token. A stem is `blind_holdout.stem_of` (control prefix and ending
removed). An "m-final" line is one whose last token ends in -m/-am (`structural_validation.ending_of`).

## Predictions and tests (all p-values from 10,000 permutations, seed 20261001)

**P1 (space pressure).** Among lines that are *not* paragraph-final, m-final lines contain more glyphs
than other lines of the same folio. Statistic: mean of (line glyphs minus folio median line glyphs),
m-final lines minus other lines. Null: shuffle the m-final flag among lines within each folio.
H_space predicts > 0.

**P2 (paragraph ends).** The -m/-am rate among the last tokens of paragraph-final lines, compared with
the last tokens of all other lines. Paragraph-final lines are not full, so H_space predicts a
**lower** rate there. H_term predicts a **higher** rate. Null: shuffle the paragraph-final flag among
lines within each folio. Two-sided.

**P3 (compression).** For line-final tokens whose stem also occurs mid-line, compute token glyph
length minus the mean glyph length of that stem's mid-line tokens. H_space predicts this difference
is more negative for -m/-am tokens than for other line-final tokens. Null: shuffle the -m/-am flag
among these line-final tokens.

**P4 (ordinary words).** The share of line-final -m/-am tokens whose stem also occurs mid-line,
compared with other line-final tokens. H_space predicts the share is not lower; a much lower share
would mean -m/-am words are a special vocabulary. Null: as P3. Two-sided; reported, not decisive.

## Decision rule

- **H_space supported:** P2 is significantly lower (p < 0.01) **and** at least one of P1 or P3 is
  significant (p < 0.01) in the predicted direction.
- **H_term supported:** P2 is significantly higher (p < 0.01).
- **Otherwise:** inconclusive. Report what was found.

---
Amendments (dated, below this line only):
