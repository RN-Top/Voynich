# Pre-registration: where do the rare symbols land?

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Idea (from the project author)

On f56r the first line looks different and contains two near-unique symbols. If the top lines of pages or
paragraphs are special (titles, names, a key), rare symbols should land there more often than chance.

## Data

ZL3b marks every symbol outside the normal alphabet as `@nnn;`. Only paragraph text (locus P) is used for the
test. Comments (`<!…>`) are ignored. A paragraph start is a P locus marked `@` in the locus identifier, and a page's
first line is its first P locus.

## Tests

- **S1, page-first lines.** Statistic: number of rare symbols in each page's first P line, summed over all pages.
  Null: for each page, one of its P lines is chosen at random as "first" (10,000 times, seed 20261002).
- **S2, paragraph-first lines.** Statistic: number of rare symbols in paragraph-start lines. Null: on each page,
  the same number of lines is chosen at random as paragraph starts (10,000 times).

Both nulls keep every page's own rare symbols, so pages that simply have many rare symbols cannot drive the
result. Pass: p < 0.01 for each.

## Descriptive ("what the symbols land on")

For each rare symbol: count, pages, sections, writing type (paragraph, label, ring, radial), position in the word
(alone, start, middle, end) and position in the line (first word, last word, other).

---
Amendments (dated, below this line only):
