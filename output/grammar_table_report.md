# Is the ending → next-beginning grammar the same for every scribe?

Pre-registration: `analyses/grammar_table_prereg.md`. 1,000 within-line shuffles, seed 20261003.

| Scribes | Shared cells | Correlation of log lift | Shuffled mean | p | Result |
|---|---:|---:|---:|---:|---|
| 1 vs 2 | 79 | 0.712 | 0.219 | 0.000999 | PASS |
| 1 vs 3 | 77 | 0.665 | 0.171 | 0.000999 | PASS |
| 2 vs 3 | 110 | 0.879 | 0.358 | 0.000999 | PASS |

**Shared grammar across scribes: YES**

## Split-half check within each scribe (descriptive)

- Scribe 1: odd vs even pages, correlation 0.851 over 62 cells
- Scribe 2: odd vs even pages, correlation 0.913 over 71 cells
- Scribe 3: odd vs even pages, correlation 0.852 over 80 cells

## The grammar table (descriptive)

For each ending: the next-word beginnings it favours most (lift = times more often than chance; count ≥ 10).

| Ending of word | Scribe 1 | Scribe 2 | Scribe 3 |
|---|---|---|---|
| -y | kc- ×2.5, ka- ×2.4, tc- ×2.3 | ls- ×2.4, da- ×1.9, sa- ×1.8 | sa- ×3.8, ra- ×2.4, da- ×1.8 |
| -ol | do- ×1.9, dy- ×1.8, ol- ×1.6 | ke- ×4.9, te- ×3.1, ka- ×2.5 | kc- ×4.6, ke- ×3.8, ka- ×3.3 |
| -aiin | ct- ×2.2, ck- ×1.8, ok- ×1.4 | yt- ×2.7, yk- ×2.1, ok- ×2.0 | od- ×2.1, y- ×2.1, yk- ×1.9 |
| -edy | — | so- ×2.5, do- ×2.4, qo- ×2.0 | pc- ×3.3, qo- ×2.1, op- ×1.4 |
| -ar | ok- ×1.5, ot- ×1.5, sh- ×1.5 | al- ×4.1, ar- ×3.3, ai- ×2.3 | al- ×3.4, ar- ×3.2, ai- ×2.9 |
| -ey | ko- ×3.5, ke- ×3.1, kc- ×2.1 | ta- ×4.4, lc- ×2.8, ka- ×2.4 | lc- ×2.2, lk- ×1.9, ka- ×1.8 |
| -dy | qo- ×2.1, ok- ×1.4, ot- ×1.3 | op- ×2.7, yk- ×1.6, da- ×1.6 | da- ×2.1, qo- ×1.8, ot- ×1.3 |
| -eey | ke- ×4.5, qo- ×2.1, da- ×1.3 | qo- ×1.6, da- ×1.3, ot- ×1.2 | lk- ×2.5, te- ×2.3, lc- ×2.2 |
| -or | yt- ×2.1, y- ×2.0, or- ×1.9 | ai- ×7.1, ar- ×4.3, or- ×2.5 | ai- ×5.1, al- ×2.0, ar- ×1.9 |
| -al | da- ×1.8, ok- ×1.6, ch- ×0.9 | ka- ×2.3, da- ×1.9, sh- ×1.6 | ta- ×2.9, ke- ×2.5, ka- ×2.2 |
| -ain | da- ×1.8, sh- ×1.1, ch- ×1.0 | sh- ×1.9, ch- ×1.9, ol- ×1.7 | al- ×1.9, ar- ×1.9, sh- ×1.8 |
| -eedy | — | lc- ×2.5, qo- ×2.2, ot- ×1.0 | qo- ×2.1, lk- ×1.2, ot- ×1.1 |
| -am | — | — | ch- ×2.2 |
| -aiiin | — | — | — |

## Reading the result

- **One grammar, shared by the scribes.** The ending → next-beginning preferences correlate 0.67–0.88 between
  scribes, against 0.17–0.36 for shuffled text (all p = 0.001). Scribes 2 and 3 (both Currier B) agree at 0.88,
  almost as closely as each scribe agrees with itself across odd and even pages (0.85–0.91). Scribe 1 (Currier A)
  agrees less (0.67–0.71): the same grammar with a dialect difference.
- **Rules that recur across scribes** (from the table):
  - **-ar / -or → ai-, al-, ar-** (scribes 2 and 3, up to ×7): e.g. "or aiin", "ar al". This is the source of the
    set phrases "or aiin" and "ar aiin".
  - **-ol → k-words** (ke-, ka-, kc-): scribes 2 and 3, up to ×4.9.
  - **-dy → qo-** (scribes 1 and 3): the classic "…dy qok…" sequence.
  - **-ey / -eey → k-words or l-words** (ke-, ko-, lk-, lc-).
  - **-aiin → y- or o-words** (yt-, yk-, od-, ok-).
- These are the first rules of the system that hold across different writers. They are not readings: they say
  which word forms follow which, not what they mean.
- Note: the shuffled correlation is above zero (0.17–0.36), probably because words on the same line share
  features even after shuffling. The observed values are far above it.
