# Pre-registration: is the label gradient position (measurement) or writing order (drift)?

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Background

`output/coordinates_report.md` found that zodiac labels farther apart around a wheel are less alike (ρ = +0.050,
p = 0.0009). Two explanations: (M) the labels encode position, like coordinates; (D) the scribe's habits drifted
while labelling in order. They come apart for pairs that are close in angle but far apart in sequence: across the
start/end seam of a ring, and between rings at the same clock position.

## Data

The same labels as `analyses/coordinates_test.py` (12 zodiac wheels, positioned Lz labels, first word). For each
wheel: angular distance (circular, 0–180°), **sequence distance** = |difference in transcription order| among that
wheel's positioned labels (ZL3b order; a stand-in for writing order), and dissimilarity (normalized edit distance).

## Statistic

Over all within-wheel pairs, on ranks: the **partial** Spearman correlation of dissimilarity with angular distance,
controlling for sequence distance (r_angle|seq), and with sequence distance, controlling for angular distance
(r_seq|angle).

## Null

Labels shuffled among positions within each wheel (10,000 shuffles, seed 20261003), recomputing both partial
correlations.

## Decision

- **Measurement (M)** if r_angle|seq > 0 with p < 0.01 and r_seq|angle is not significant (p ≥ 0.01).
- **Drift (D)** if r_seq|angle > 0 with p < 0.01 and r_angle|seq is not significant.
- **Both** if both pass; **undecided** if neither passes.

Caveat: transcription order may not be the scribe's writing order.

---
Amendments (dated, below this line only):

**2026-10-03, results.** r_angle|seq = +0.046, p = 0.0014; r_seq|angle = +0.026, p = 0.20. **MEASUREMENT
(position).** Writing orientation is a remaining alternative. Write-up: `output/coord_vs_drift_report.md`.
