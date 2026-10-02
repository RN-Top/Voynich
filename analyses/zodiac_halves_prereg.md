# Pre-registration: do the two halves of the same zodiac sign share label vocabulary?

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Idea

Aries and Taurus are each drawn over two pages of 15 figures (light and dark halves): Aries f70v1 + f71r,
Taurus f71v + f72r1. If the labels relate to the sign (names of stars, degrees or days of that sign), the two
halves of one sign should share more label vocabulary than pages of different signs do.

## Data

ZL3b zodiac labels (locus code Lz) on the 12 zodiac pages (f70v1–f73v), first word of each label. Each page
is described by the counts of its labels' beginnings (first 2 letters).

## Statistic

Cosine similarity between two pages' beginning counts. S = mean similarity of the two same-sign pairs
(Aries halves, Taurus halves).

## Tests

**Z1.** Null: the mean similarity of two randomly chosen *different-sign* page pairs (all such pairs of pairs
enumerated). p = share of them with mean ≥ S. Pass: p < 0.01.

**Z2 (physical-closeness control).** The same-sign halves face each other in the book, so closeness alone
could make them similar. S must also exceed the mean similarity of the different-sign pairs that are equally
close: pages on the same side of one foldout panel (f70v1–f70v2; f72r1–f72r2, f72r1–f72r3, f72r2–f72r3;
f72v1–f72v2, f72v1–f72v3, f72v2–f72v3), facing pages (f70v2–f71r), and the two sides of one leaf (f71r–f71v).

## Decision

**Supported** if Z1 and Z2 both pass. **Not supported** otherwise. Only two same-sign pairs exist, so only a
large effect can be detected.

---
Amendments (dated, below this line only):
