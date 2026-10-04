# Pre-registration: do the zodiac labels follow the 28 lunar mansions?

Date: 2026-10-04. Written before the code exists.

## Idea (crib)

Medieval astrology divided the Moon's path into **28 mansions**, each 12°51′ wide. Each mansion has its own name and
its own medical and practical uses. A zodiac sign (30°) therefore contains parts of 2 or 3 mansions, and the
boundaries fall at different degrees in each sign. If the 29–30 figure labels of each zodiac wheel are degree
entries that carry mansion information, labels in the **same mansion** should be more alike than neighbouring
labels on opposite sides of a mansion boundary.

## Data

- **Signs and labels:** the 10 signs and their labels in transcription order, from
  `zodiac_days_test.zodiac_labels()` (Pisces to Sagittarius; Aquarius and Capricorn are missing from the book).
- **Degree:** label *i* of *n* in a sign sits at degree d = 30·i/n.
- **Sign index:** k = 0 (Aries) … 11 (Pisces).
- **Mansion:** m = floor((30k + d) / (360/28)).

## Statistic

- **Pairs:** labels within the same sign that are 1–4 places apart.
- **Similarity:** the Jaccard index of character-bigram sets (with word-boundary marks).
- **D** = mean similarity of same-mansion pairs − mean similarity of different-mansion pairs.

## Null

- For each sign independently, shift where degree 0 falls by a random whole number of label positions (0 to n−1),
  recompute the mansion boundaries, and recompute D.
- This keeps every label and every distance, and moves only the boundaries.
- 10,000 draws, seed 20261010.

## Threshold

One-sided p < 0.05.

## Weaknesses

- **Unknown starting point.** We do not know which figure is degree 0, or which way the wheel runs. Transcription
  order is assumed. If that assumption is wrong, the true signal is diluted toward the null, so a null result is
  weak evidence against the idea.
- **Halved signs.** Aries and Taurus are split over two half-pages each, and joined in transcription order.
