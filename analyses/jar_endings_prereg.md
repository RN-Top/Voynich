# Pre-registration: do jar labels carry a "prepared remedy" ending? (split replication)

Date: 2026-10-04. Written before the code exists.

## Idea (medieval lens)

In a medieval pharmacy book, a jar holds a prepared remedy (a syrup, oil or powder), and a plant part is a raw
ingredient. If Voynich word endings mark a class of thing, jar labels should share endings that plant-part labels
lack. `output/dictionary_report.md` found jar and plant-part label endings differ (p = 0.002, pooled over all
pharmacy pages, not part of that verdict).

**Disclosure:** that pooled result already includes the confirmation pages. This is a consistency check across the
two pharmacy blocks, not fully fresh data.

## Data

`dictionary_test.labels()`: the first word of each `Lc` (jar) and `Lf` (plant-part) label, with ending = the last
2 letters.

- **Block 1 (learn):** f88r–f89v2.
- **Block 2 (test):** f99r–f102v2.

## Method

1. **In block 1:** "jar endings" are the endings with at least 2 jar uses whose jar share is above block 1's
   overall jar share.
2. **In block 2:**

   T = share of jar labels with a jar ending − share of plant-part labels with a jar ending.

3. **Null:** shuffle jar/part kinds within each block-2 page, 10,000 times, seed 20261008.
4. **Threshold:** one-sided p < 0.05.
