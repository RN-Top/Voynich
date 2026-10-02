# Pre-registration: does the manuscript favour Fibonacci numbers?

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Idea (from the project author)

Fibonacci numbers (and the project author's doubled sequence 0, 2, 2, 4, 6, 10, 16, 26, 42) may be built into the
book. If so, counts in the text should land on those numbers more often than on their neighbours.

## Counts (from ZL3b, canonical parser; paragraph text unless stated)

1. words per line
2. letters per word (EVA characters)
3. lines per paragraph
4. paragraph lines per page
5. paragraph words per page
6. labels per page (all label loci, pages with at least one label)

## Test

Counts vary smoothly, so each target number is compared only with its two neighbours. For a target T, take all
values equal to T−1, T or T+1. If T is not special, about 1 in 3 of them should be T. Targets whose neighbours are
themselves targets are left out.

- **F (Fibonacci):** T ∈ {5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610}
- **D (doubled sequence):** T ∈ {10, 16, 26, 42} (6 is left out because its neighbour 5 is Fibonacci)

Statistic: over all six count types and all targets, the number of values equal to T, out of all values in
{T−1, T, T+1}. Each count type gets the same weight. Test: one-sided binomial against 1/3, with the windows of all
count types pooled. Pass: p < 0.005 for each of F and D (0.01 split over the two).

Each count type and target is also reported separately (descriptive). A pass would mean the counts favour these
numbers. A fail would mean they land on them about as often as on their neighbours.

---
Amendments (dated, below this line only):

**2026-10-02.** The first run crashed in the hand-written binomial function (number overflow) before printing any
result. It was replaced by `scipy.stats.binom.sf`, the same one-sided binomial test.

**2026-10-02, results.** F formally PASS (36.5%, p = 1e-31), D FAIL (32.6%, p = 0.78). An extra check (labelled)
shows the F pass comes entirely from the word-length peak at 5 letters, which breaks the test's smoothness
assumption. Without it the result is 33.2% (p = 0.59). **Conclusion: not supported.** The design flaw is recorded in
`output/fibonacci_report.md`.
