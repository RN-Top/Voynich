# Pre-registration: do zodiac labels build up steadily around each wheel, like counted numbers?

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Idea (from the project author's measurement reading)

If the ~30 figures per sign are degrees or days (1–30) and the labels encode them, labels should grow in length or
complexity steadily from a starting figure around the wheel, as written numbers do.

## Data

The same positioned zodiac labels as `analyses/coordinates_test.py` (12 wheels). Labels are put in clock order (by
angle) within each wheel. Complexity = label length in letters (first word, canonical clean). A second measure,
with ch, sh, cth, ckh, cph, cfh counted as single symbols (S2 units), is reported for comparison.

## Statistic

For each wheel: for every possible starting figure and both directions (clockwise and counter-clockwise), the
Spearman correlation between step number (1…n from the start) and label length. Keep the best (largest). S = mean of
the best values over the 12 wheels.

## Null

Labels shuffled among positions within each wheel, with the same best-start-and-direction search, 5,000 times, seed
20261003. Pass: p < 0.01.

## Descriptive

For each wheel: the best starting figure (clock position), the direction, the correlation, and the labels in order.

---
Amendments (dated, below this line only):

**2026-10-03, results.** Letters: 0.480 vs 0.421, p = 0.025. S2: 0.476 vs 0.420, p = 0.028. **Not supported**
(suggestive). Write-up: `output/counting_report.md`.
