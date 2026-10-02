# Does the manuscript favour Fibonacci numbers?

Pre-registration: `analyses/fibonacci_prereg.md`. Each target is compared with its two neighbours; no preference means about 1 in 3 of the values in each window land on the target.

## F: Fibonacci

- On target: **11456 of 31424** (36.5%; no preference ≈ 33.3%)
- p = 1.12e-31 → **PASS**

| Count | Target | One below | On target | One above |
|---|---:|---:|---:|---:|
| words per line | 5 | 245 | 310 | 334 |
| words per line | 8 | 336 | 455 | 555 |
| words per line | 13 | 324 | 155 | 67 |
| words per line | 21 | 2 | 5 | 1 |
| letters per word | 5 | 6352 | 8756 | 6808 |
| letters per word | 8 | 3962 | 1572 | 571 |
| letters per word | 13 | 18 | 9 | 2 |
| lines per paragraph | 5 | 144 | 97 | 80 |
| lines per paragraph | 8 | 44 | 31 | 22 |
| lines per paragraph | 13 | 4 | 12 | 8 |
| lines per paragraph | 21 | 1 | 2 | 1 |
| paragraph lines per page | 5 | 2 | 3 | 5 |
| paragraph lines per page | 8 | 10 | 7 | 13 |
| paragraph lines per page | 13 | 11 | 20 | 14 |
| paragraph lines per page | 21 | 2 | 4 | 1 |
| paragraph lines per page | 34 | 0 | 2 | 2 |
| paragraph lines per page | 55 | 2 | 0 | 0 |
| paragraph words per page | 34 | 0 | 1 | 0 |
| paragraph words per page | 55 | 1 | 1 | 1 |
| paragraph words per page | 89 | 2 | 5 | 2 |
| paragraph words per page | 144 | 1 | 0 | 1 |
| paragraph words per page | 377 | 2 | 0 | 1 |
| labels per page | 5 | 3 | 1 | 2 |
| labels per page | 8 | 1 | 2 | 1 |
| labels per page | 13 | 2 | 5 | 1 |
| labels per page | 21 | 1 | 0 | 2 |
| labels per page | 34 | 1 | 1 | 0 |

## D: doubled sequence

- On target: **856 of 2623** (32.6%; no preference ≈ 33.3%)
- p = 0.782 → **FAIL**

| Count | Target | One below | On target | One above |
|---|---:|---:|---:|---:|
| words per line | 10 | 555 | 604 | 462 |
| words per line | 16 | 20 | 12 | 5 |
| words per line | 26 | 3 | 3 | 0 |
| letters per word | 10 | 571 | 181 | 50 |
| lines per paragraph | 10 | 22 | 18 | 12 |
| lines per paragraph | 16 | 6 | 7 | 1 |
| lines per paragraph | 26 | 2 | 1 | 0 |
| paragraph lines per page | 10 | 13 | 12 | 20 |
| paragraph lines per page | 16 | 6 | 12 | 3 |
| paragraph lines per page | 26 | 0 | 1 | 1 |
| paragraph lines per page | 42 | 4 | 1 | 1 |
| paragraph words per page | 42 | 1 | 0 | 0 |
| labels per page | 10 | 1 | 3 | 0 |
| labels per page | 16 | 6 | 0 | 1 |
| labels per page | 26 | 1 | 1 | 0 |
## Extra check (added after the run, not pre-registered): the pass is an artifact

The neighbour comparison assumes counts change smoothly around each target. That fails at the peak of a
distribution, and **5 letters is the most common Voynich word length** (8,756 words, against 6,352 at 4 and 6,808
at 6). That one window supplies almost all of the excess.

- **Without letters-per-word:** 1,119 of 3,374 on target (33.2%, no preference = 33.3%), p = 0.59.
- **Leaving out every window where the target is the peak of its count type:** 28.3%, p = 1.

**Conclusion: no evidence that the manuscript favours Fibonacci numbers.** The doubled sequence also shows no
preference (32.6%, p = 0.78). The pre-registered test design was flawed, and this is recorded here rather than claimed
as a result.

Curiosities, not evidence: the most common page length is 13 paragraph lines (a Fibonacci number), and the most
common line length is 10 words (in the doubled sequence). Each is one number among many possible.
