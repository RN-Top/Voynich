# Pre-registration: does writing orientation explain the zodiac label gradient?

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Background

Zodiac labels are more alike when closer in angle within a wheel, independent of writing order
(`output/coord_vs_drift_report.md`). A remaining explanation is **orientation**: labels at a given compass direction
are written with the page turned the same way, which might shape the letters. Orientation acts on **absolute**
angle, so it would also make labels at the same absolute angle on **different** wheels alike. A measurement
counted within each sign would not, unless every wheel starts at the same clock position.

## Data

The same positioned zodiac labels as `analyses/coordinates_test.py`. Pairs of labels from **different** wheels:
absolute circular angular distance (0–180°) and dissimilarity (normalized edit distance).

## Statistic and null

O1: Spearman correlation between absolute angular distance and dissimilarity over all cross-wheel pairs. Null: labels
shuffled among positions within each wheel (10,000 shuffles, seed 20261003).

## Decision

- **Orientation not supported** (the measurement reading stands against this alternative) if O1 is not significant
  (p ≥ 0.01).
- **Orientation possible** if O1 > 0 with p < 0.01.

---
Amendments (dated, below this line only):

**2026-10-03, results.** O1 = +0.003, p = 0.25. **Orientation not supported**; the measurement reading stands.
Write-up: `output/orientation_report.md`.
