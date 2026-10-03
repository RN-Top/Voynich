# Position (measurement) or writing order (drift)?

Pre-registration: `analyses/coord_vs_drift_prereg.md`. 12 wheels, 298 labels, 3,842 pairs; 10,000 shuffles, seed 20261003.

- Rank correlation between angular distance and sequence distance: 0.14 (how far the two can be told apart)
- Dissimilarity with **angle**, controlling for sequence: **+0.046** (shuffled -0.000), p = 0.0014
- Dissimilarity with **sequence**, controlling for angle: **+0.026** (shuffled +0.010), p = 0.196

**Verdict: MEASUREMENT (position).**

## Reading the result

- **Position, not writing order.** Label similarity follows angle around the wheel even after controlling for
  sequence (p = 0.0014). Sequence adds nothing once angle is controlled (p = 0.20). Angle and sequence were well
  separated (rank correlation 0.14), mostly because labels at the same angle on different rings sit far apart in
  sequence.
- This favours the project author's reading that the labels carry **position information**, like coordinates, over
  simple scribal drift.
- **Remaining alternative: writing orientation.** Labels around a wheel are written at different orientations (the
  page is turned), which could change letter forms or habits by angle. That would also tie label form to angle
  without any measurement. A test: whether the similarity follows **absolute** angle (same compass direction on
  different wheels) or only **relative** position within a wheel.
- The effect is small: position explains only a small part of label variation.
