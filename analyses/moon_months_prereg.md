# Pre-registration: the 12 moons of f67r2 as full and hollow months

Date: 2026-10-04. Written and committed before the moons' colours were recorded or their labels placed on them.

## Image

`uploads/yale_hires/f67r_spread.jpg`: Erin's photo of f67r1 (left) and f67r2 (right), 2576 × 1937 px.

## Idea

The medieval lunar year has 12 months that alternate **full** (30 days) and **hollow** (29 days), 354 days in all.
On a low-resolution look, f67r2's 12 moons seemed to alternate between two kinds: a red crescent and a gold disc.
If the ring is a lunar-year diagram, then (1) the two kinds should alternate around the ring, and (2) the 12 moon
labels (`f67r2.52`–`.63`, `@Ls`/`&Ls`) might differ by kind.

## Protocol

1. Record each moon's position (angle around the ring centre) and its kind: `red` (red crescent), `gold` (gold or
   uncoloured disc or crescent) or `unclear`. This is done before looking at which label belongs to it.
2. Then place each of the 12 `Ls` labels on its moon by reading it at 4× zoom.

## Test 1: alternation (picture only)

- **Statistic:** A = the number of colour changes going once around the ring (circular, 12 moons).
- **Null:** all circular arrangements of the observed colour counts, enumerated exactly.
- **Prediction:** A is larger than chance (perfect alternation is A = 12).
- **Threshold:** one-sided p < 0.025.

## Test 2: do the labels split by colour?

- **Similarity:** between two labels, the Jaccard index of their character-bigram sets (with word-boundary marks).
- **Statistic:** W = mean similarity of same-colour pairs − mean similarity of different-colour pairs.
- **Null:** every split of the 12 labels into groups of the observed sizes, enumerated exactly.
- **Prediction:** W > 0.
- **Threshold:** one-sided p < 0.025.
- Moons marked `unclear` are excluded from both tests.

## Known weaknesses

- Only 12 moons, so test 2 has little power.
- The colours may have faded.
- I already saw the photo at normal size before writing this, so the rough colour pattern was known (that is why
  test 1 is "picture only" and exploratory in spirit). The label–colour pairing in test 2 was not known.
