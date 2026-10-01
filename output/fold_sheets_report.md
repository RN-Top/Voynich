# Do the two halves of a folded sheet belong together?

Pre-registration: `analyses/fold_sheets_prereg.md` (committed before this code). 10,000 random re-pairings
within each gathering, seed 20261001.

**Decision (pre-registered rule): Supported**

| Version | Sheet pairs | S1 shared vocabulary: sheet pairs vs random pairs | p | S2 same word at same spot | p |
|---|---:|---|---:|---|---:|
| (a) all sheet pairs | 50 | 0.570 vs 0.474 | 0.0001 | 0.0077 vs 0.0060 | 0.0031 |
| (b) excluding center-fold / adjacent pairs | 36 | 0.573 vs 0.472 | 0.0001 | 0.0082 vs 0.0065 | 0.0153 |

Descriptive: the book's first and last leaves (f1, f116; different gatherings, so not one sheet) have shared-vocabulary similarity 0.275, higher than 42% of all leaf pairs.

## Reading the result (added after the first run; no numbers above changed)

A follow-up check (exploratory, not pre-registered) compared each sheet only with other leaf pairs by
the **same scribe ($H) in the same Currier language ($L)** in the same gathering. Sheet halves were still
more similar in 21 of 27 sheets (mean +0.079 cosine, sign-flip p ≈ 0.0002), so "same scribe" does not
explain it.

What this supports: **each folded sheet behaves like a unit of writing**. Its two halves were most
likely written together, in one sitting or on one topic. This fits the view that the text was written on
loose sheets before binding.

What it does not show: a positional key. The prediction a key would make most directly, that the same
word sits at the same spot when the sheet is folded, is weak and not significant once neighbouring leaves
are excluded (S2, version b).

Sheet pairs tested (b): f1–f8, f2–f7, f3–f6, f9–f16, f10–f15, f11–f14, f17–f24, f18–f23, f19–f22, f25–f32, f26–f31, f27–f30, f33–f40, f34–f39, f35–f38, f41–f48, f42–f47, f43–f46, f49–f56, f50–f55, f51–f54, f57–f66, f58–f65, f75–f84, f76–f83, f77–f82, f78–f81, f87–f90, f93–f96, f99–f102, f103–f116, f104–f115, f105–f114, f106–f113, f107–f112, f108–f111
