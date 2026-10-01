# Pre-registration: are the zodiac figure labels names of days?

Committed before any code for this test was written or run. Amend only below the line at the end.

## Background

Each zodiac sign has 29–30 labelled figures. Aries and Taurus are each split over two pages of 15.
That is about one per day of the month, or one per degree of the sign. If each label names a day
(or degree), the label at the same position should be the same, or similar, across different months.

## Data

- Pages with `$I=Z` in ZL3b. Labels are lines with locus type `Lz`, kept in transcription order (the
  transcription lists them ring by ring, in clock order).
- Aries (f70v1 + f71r) and Taurus (f71v + f72r1) are joined in page order to make one 30-label sequence
  each. The result is 10 signs.
- A label's key is the first word of the label (canonical `clean_token`).
- Similarity of two labels: 1 if their first three letters are equal, else 0. This allows for inflected
  forms of the same name.

## Statistic

For every pair of signs (A, B), with n = the shorter length:
- Try every rotation r of B (the start point on each circle is unknown).
- Take the best mean similarity over positions k < n of A[k] vs B[(k + r) mod n].

The statistic is the mean of these best-rotation scores over all sign pairs.

## Null

Shuffle the label order within each sign (10,000 times, seed 20261001) and compute the same statistic,
including the same best-rotation search. One-sided p.

## Decision rule

- **Supported:** p < 0.01.
- **Not supported:** otherwise.

---
Amendments (dated, below this line only):
