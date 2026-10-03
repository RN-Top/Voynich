# Does anything pulse at a regular beat?

Pre-registration: `analyses/rhythm_prereg.md`. 2,000 shuffles, seed 20261003.

## Currier A

**R1, inside lines (same ending k words apart):**

| k | Local peak | Shuffled | p |
|---:|---:|---:|---:|
| 2 | -51.5 | -16.8 | 0.877 |
| 3 | +3.0 | -16.0 | 0.244 |
| 4 | -27.0 | -16.8 | 0.669 |
| 5 | -24.5 | -17.0 | 0.66 |
| 6 | -9.0 | -17.0 | 0.314 |

**R2, down the page (qo- share, k lines apart):**

| k | Local peak | Shuffled | p |
|---:|---:|---:|---:|
| 2 | +0.00038 | -0.00000 | 0.23 |
| 3 | +0.00012 | -0.00002 | 0.408 |
| 4 | -0.00051 | +0.00002 | 0.817 |
| 5 | -0.00078 | -0.00001 | 0.903 |
| 6 | +0.00175 | +0.00001 | 0.0055 |
| 7 | -0.00051 | -0.00000 | 0.759 |
| 8 | -0.00110 | -0.00002 | 0.92 |

## Currier B

**R1, inside lines (same ending k words apart):**

| k | Local peak | Shuffled | p |
|---:|---:|---:|---:|
| 2 | +16.0 | -6.4 | 0.318 |
| 3 | -58.5 | -10.0 | 0.886 |
| 4 | -4.5 | -9.9 | 0.441 |
| 5 | +1.0 | -7.9 | 0.392 |
| 6 | -35.0 | -16.2 | 0.765 |

**R2, down the page (qo- share, k lines apart):**

| k | Local peak | Shuffled | p |
|---:|---:|---:|---:|
| 2 | +0.00072 | -0.00000 | 0.08 |
| 3 | -0.00033 | +0.00000 | 0.737 |
| 4 | -0.00014 | -0.00001 | 0.6 |
| 5 | +0.00042 | +0.00000 | 0.209 |
| 6 | -0.00087 | +0.00002 | 0.95 |
| 7 | +0.00140 | -0.00003 | 0.007 |
| 8 | -0.00099 | -0.00000 | 0.951 |

**Verdict: no rhythm found.**

## Reading the result

- **No beat inside lines.** No ending class recurs at a regular word spacing beyond chance (all p ≥ 0.24).
- **No wave down the page passes.** Two near misses: dialect A, every 6 lines (p = 0.0055), and dialect B, every 7
  lines (p = 0.007). Neither clears the corrected threshold (p < 0.0007). With 14 wave lags tested, one or two
  values this low are expected by chance. They would need a fresh test before anyone made something of them.
