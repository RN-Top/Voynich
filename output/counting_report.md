# Do zodiac labels build up steadily around each wheel?

Pre-registration: `analyses/counting_prereg.md`. 12 wheels; best start and direction searched for real and shuffled labels alike; 5,000 shuffles, seed 20261003.

## Complexity = letters

- Mean best correlation: **0.480** (shuffled with the same search: 0.421); p = 0.0248 → **NOT SUPPORTED**

| Wheel | Best start | Direction | Correlation |
|---|---|---|---:|
| f70v2 | 10:00 | clockwise | 0.60 |
| f70v1 | 02:00 | clockwise | 0.36 |
| f71r | 11:00 | counter-clockwise | 0.70 |
| f71v | 05:30 | clockwise | 0.57 |
| f72r1 | 08:30 | counter-clockwise | 0.55 |
| f72r2 | 01:00 | counter-clockwise | 0.29 |
| f72r3 | 01:30 | clockwise | 0.41 |
| f72v3 | 00:00 | counter-clockwise | 0.40 |
| f72v2 | 00:30 | clockwise | 0.44 |
| f72v1 | 05:00 | counter-clockwise | 0.55 |
| f73r | 11:30 | counter-clockwise | 0.47 |
| f73v | 03:30 | counter-clockwise | 0.40 |

## Complexity = S2 symbols

- Mean best correlation: **0.476** (shuffled with the same search: 0.420); p = 0.028 → **NOT SUPPORTED**

## Reading the result

- **Not supported at the threshold.** Labels lengthen steadily around the wheel slightly more than shuffled labels do
  (0.480 vs 0.421 letters; 0.476 vs 0.420 S2 symbols), but p = 0.025–0.028 does not pass p < 0.01.
- The best-fitting starts and directions vary from wheel to wheel (clock positions all round, both directions). A
  shared counting rule would more likely start at a consistent point.
- The position effect found earlier (`coord_vs_drift_report.md`) is therefore **not** a simple "labels get longer as
  you count" pattern. If the labels encode degrees, it is not by length. It might be by which symbols change.
