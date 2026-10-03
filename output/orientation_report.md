# Does writing orientation explain the zodiac label gradient?

Pre-registration: `analyses/orientation_prereg.md`. 12 wheels, 298 labels, 40,411 cross-wheel pairs; 10,000 shuffles, seed 20261003.

- Cross-wheel correlation, absolute angle vs dissimilarity: **+0.003** (shuffled -0.000), p = 0.252

**Verdict: ORIENTATION NOT SUPPORTED (measurement reading stands).**

## Reading the result

- Labels at the same **absolute** angle on different wheels are not more alike (ρ = +0.003, p = 0.25). Page
  orientation acts on absolute angle, so it does not explain the within-wheel gradient.
- The within-wheel, position-linked similarity (`coord_vs_drift_report.md`) therefore stands as **measurement-like**:
  labels carry information about their position **within their own wheel**.
- This also fits the earlier zodiac test (`zodiac_days_report.md`): labels at the same relative position on different
  signs are not the same words. Each wheel has its own labels, which vary gradually around that wheel.
