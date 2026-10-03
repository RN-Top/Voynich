# Do the star-marked paragraphs repeat in cycles?

Pre-registration: `analyses/cycles_prereg.md`. Paragraphs: 157 (f103–f108) + 128 (f111–f116); 10,000 order shuffles, seed 20261003.

- **C1 week (lag 7):** peak +0.0099, p = 0.0916 → **FAIL**
- **C2 month (lags 27–31):** best peak +0.0102, p = 0.445 → **FAIL**
- **C3 any cycle (2–40, Bonferroni p < 0.00026):** none

## Similarity by spacing (descriptive)
- Similarity of neighbouring paragraphs (spacing 1): 0.5373; spacing 40: 0.4605

| Spacing | Mean similarity | Local peak | p |
|---:|---:|---:|---:|
| 2 | 0.5286 | +0.0015 | 0.41 |
| 3 | 0.5168 | -0.0012 | 0.566 |
| 4 | 0.5074 | -0.0065 | 0.813 |
| 5 | 0.5110 | +0.0068 | 0.177 |
| 6 | 0.5010 | -0.0089 | 0.884 |
| 7 | 0.5087 | +0.0099 | 0.0916 |
| 8 | 0.4966 | -0.0066 | 0.808 |
| 9 | 0.4976 | +0.0026 | 0.365 |
| 10 | 0.4933 | -0.0036 | 0.69 |
| 11 | 0.4964 | +0.0039 | 0.297 |
| 12 | 0.4915 | +0.0000 | 0.498 |
| 13 | 0.4866 | -0.0057 | 0.778 |
| 14 | 0.4930 | +0.0073 | 0.174 |
| 15 | 0.4848 | +0.0006 | 0.459 |
| 16 | 0.4754 | -0.0042 | 0.71 |
| 17 | 0.4745 | -0.0014 | 0.569 |
| 18 | 0.4763 | +0.0022 | 0.392 |
| 19 | 0.4737 | +0.0002 | 0.488 |
| 20 | 0.4706 | -0.0037 | 0.677 |
| 21 | 0.4749 | +0.0016 | 0.421 |
| 22 | 0.4759 | -0.0000 | 0.5 |
| 23 | 0.4771 | +0.0018 | 0.415 |
| 24 | 0.4745 | -0.0044 | 0.711 |
| 25 | 0.4808 | +0.0065 | 0.202 |
| 26 | 0.4740 | -0.0029 | 0.641 |
| 27 | 0.4731 | -0.0002 | 0.513 |
| 28 | 0.4725 | +0.0035 | 0.33 |
| 29 | 0.4650 | -0.0087 | 0.86 |
| 30 | 0.4750 | +0.0102 | 0.107 |
| 31 | 0.4646 | -0.0047 | 0.72 |
| 32 | 0.4637 | -0.0010 | 0.549 |
| 33 | 0.4648 | -0.0011 | 0.554 |
| 34 | 0.4680 | +0.0111 | 0.0897 |
| 35 | 0.4490 | -0.0118 | 0.921 |
| 36 | 0.4536 | +0.0015 | 0.425 |
| 37 | 0.4552 | +0.0027 | 0.381 |
| 38 | 0.4513 | -0.0017 | 0.583 |
| 39 | 0.4508 | -0.0051 | 0.721 |
| 40 | 0.4605 | +0.0071 | 0.206 |

## Reading the result

No cycle of any length from 2 to 40 paragraphs, including week (7) and month (27–31) spacings. Similarity falls
slowly with distance (0.54 for neighbours, 0.46 at 40 apart), which is gradual drift and not repetition. If the
section is a calendar, its entries do not reuse vocabulary on a weekly or monthly rhythm detectable at the root
level.
