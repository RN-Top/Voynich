# Do word parts combine freely or under restrictions?

Pre-registration: `analyses/slots_prereg.md`. Words of 5+ letters; equal samples of N = 5,369 tokens; start = first 2 letters, end = last 2 letters. Seed 20261003.

| Text | Eligible tokens | Dependence (0 = free) | 95% interval |
|---|---:|---:|---|
| Voynich A | 6,396 | 0.073 | 0.063–0.079 |
| Voynich B | 15,533 | 0.065 | 0.056–0.071 |
| latin_apicius_recipes | 5,369 | 0.284 | 0.242–0.259 |
| latin_albertanus_13c | 46,672 | 0.123 | 0.092–0.106 |
| latin_bede_8c | 56,501 | 0.101 | 0.071–0.085 |
| cipher of Apicius | 6,371 | 0.218 | 0.194–0.213 |

**Verdict: MIXED.**

## Reading the result

- This is the corrected run. The first run had two resampling errors (see the amendment in
  `analyses/slots_prereg.md`; the first run is kept in `output/slots_report_first_run.md`).
- **By the pre-registered rule: MIXED.** Voynich A's interval (0.063–0.079) touches Bede's (0.071–0.085).
- **The point estimates are the lowest of all six texts:** Voynich B 0.065, Voynich A 0.073, against Latin
  0.101 (Bede), 0.123 (Albertanus) and 0.284 (Apicius), and 0.218 for the enciphered Latin. A word's start tells you
  less about its end in the Voynich than in any Latin text tested.
- The cipher control behaves like its source language, as expected: a letter cipher does not free the slots. So the
  Voynich's looser slots are not explained by simple encipherment of Latin.
- Caveat: half-sample intervals sit below the full-sample estimates for every text (the shuffle correction depends
  on sample size). Compare the intervals with each other, not with the point estimates.
- Reading: Voynich word parts combine **more freely than Latin's**, toward the code/notation end, but not
  decisively separated from Bede's prose. Only one language family was available for comparison.
