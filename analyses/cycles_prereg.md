# Pre-registration: do the star-marked paragraphs repeat in cycles (a calendar)?

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Idea

The Stars/Recipes section (f103–f116) has 285 short paragraphs, each marked with a star, on 23 surviving pages.
Folios 109–110 (4 pages) are missing. At 12–19 paragraphs per page the original total would be roughly 335–365,
close to a year of days. If the section is an almanac (one entry per day), similar entries should recur at
calendar spacings: 7 (weeks) or about 30 (months). This also scans every spacing from 2 to 40, to catch a cycle
nobody has guessed.

## Data

Paragraphs are taken from paragraph loci on Stars/Recipes pages, split at the transcription's paragraph markers
(`<%>` … `<$>`), in page order. The gap at folios 109–110 splits them into two runs (f103r–f108v and
f111r–f116r). Pairs are only formed within a run. Each paragraph is represented by the counts of its word roots
(root rule of `analyses/root_dictionary_test.py`).

## Statistic

sim(L) = mean cosine similarity of all paragraph pairs L apart. Neighbouring paragraphs are similar anyway
(writing drifts slowly), so a cycle has to show as a **local peak**: peak(L) = sim(L) − (sim(L−1) + sim(L+1)) / 2.

## Tests

Null: paragraph order shuffled within each run, 10,000 times (seed 20261003).

- **C1 (week):** peak(7). Pass: p < 0.01.
- **C2 (month):** max of peak(L) for L = 27…31; the null takes the same maximum. Pass: p < 0.01.
- **C3 (any cycle):** every L from 2 to 40, Bonferroni threshold 0.01 / 39.

## Decision

- **Calendar-like cycles found** if C1 or C2 passes.
- An unexpected cycle is reported if any C3 lag passes.
- Otherwise **no cycles found**.

---
Amendments (dated, below this line only):

**2026-10-03, results.** C1 FAIL (p = 0.092), C2 FAIL (p = 0.45), C3 none. **No cycles found.** Write-up:
`output/cycles_report.md`.
