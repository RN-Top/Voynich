# Pre-registration: measured paint colours across the plant pages

Date: 2026-10-04. Written before any colour measurement.

## Idea (Erin)

There may be patterns or anomalies in the plants' colours that we cannot see by eye. The paints are mineral pigments
(copper blues and greens, iron ochres, red pigments), so a colour profile is also a metal profile.

## Measurement

**Pages.** Every herbal plant page (`section == Herbal`), plus the full-page plants f87r, f87v, f90r, f90v, f93r,
f93v, f94r, f95v, f96r and f96v. The images come from `images/yale/`, scaled to 800 px wide.

**Paint pixels.**
- The vellum background is estimated per page as the median colour of the outer 5% border.
- A pixel counts as paint if its saturation (HSV) exceeds the vellum's by more than 0.12 and it is not dark ink
  (V > 0.25).

**Families.** Each paint pixel is assigned to a family by hue:

| Family | Hue range |
|---|---|
| red | 345–15° |
| ochre/brown | 15–45° |
| yellow | 45–70° |
| green | 70–170° |
| blue | 170–260° |
| other | everything else |

**Profile.** A page's profile is the share of its paint pixels in each family.

## Confirmatory test

- **Question:** do pages with similar colour profiles have similar text?
- **Statistic:** Spearman ρ between the colour-profile distance and the text distance (1 − cosine of root counts,
  as in `flower_colour_test.py`) over all page pairs.
- **Null:** shuffle profiles among pages within Currier language, 10,000 times, seed 20261013.
- **Prediction:** ρ > 0. One-sided p < 0.05.

## Exploratory (reported, not tested)

1. Anomalies: the pages whose profiles are furthest from all others (top 5 by mean distance).
2. Groups: k-means with k = 4 on the profiles, and how the groups line up with scribe, Currier language and position
   in the book.
3. Colour by quire: average profile per quire, to see whether painting changes through the book (different paint
   batches or painters).

## Amendment (2026-10-04, after the first run)

**The first run's measurement failed.** It assigned 90% of the paint to "ochre" and only 2% to green, on pages whose
plants are mostly green. A saturation threshold over the yellow vellum picked up stained vellum and brown ink rather
than paint, so all first-run results are **void** (they were ρ = −0.03, p = 0.79).

**The fix.** Paint is now detected in Lab colour space as a chroma difference from the page's own vellum
(ΔE_ab > 15, with 25 < L < 90 and a 5% border excluded). Families are set by the hue angle of that difference:

| Family | Hue angle |
|---|---|
| red | 315–45° |
| ochre/tan | 45–120° |
| green | 120–215° |
| blue | 215–300° |

The angles were calibrated by eye on five pages (f1v, f2v, f9v, f16v and f42r) so that their known green leaves,
blue flowers and red flowers land in the right family. This was done before the rerun. The test itself is
unchanged, and it is rerun once.
