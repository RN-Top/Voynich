# Pre-registration: do plant-matching star labels sit on marked stars? (f68r2, f68r3)

Date: 2026-10-04. Written and committed **before** the f68r2 and f68r3 star centres were classified or their
labels were placed on stars.

## Image

`uploads/yale_hires/f68r_foldout_recto.jpg`: Erin's photo of the f68r fold-out (f68r1 | f68r2 | f68r3) from the Yale
viewer, 2576 × 1234 px. Labels are legible at 4× zoom.

## How the idea arose (discovery data, post hoc)

On f68r1 I placed the 29 star labels (`f68r1.8`–`.36`) on their stars and classified each star's centre at 4× zoom
(`analyses/star_centres_f68r1.csv`):

- 8 stars have a **hollow ring** at the centre and 2 have a **dark dot**. The other 19 are plain.
- The five f68r1 labels that share a root with herbal-page openings (okoaly, chocfhy, otydy, @167oeeod…, otochedy;
  see `output/plant_star_report.md`) fall on: plain, plain, ring, ring, ring.
- That is 3 of 5 on marked stars, against 10/29 × 5 = 1.7 expected. The hypergeometric P(≥3) is 0.21 if both rings
  and dots count, and 0.11 if only rings count. **This is not significant.** It was also noticed after looking, so
  it is a hypothesis only.

## Confirmation test (new data only: f68r2 and f68r3)

- **Matching labels** (fixed in advance, from `plant_star_report.md`):
  - f68r2: o@167olch… (.7), oydchy (.17), opocphor (.26)
  - f68r3: otydg (.19)
- **Protocol:**
  1. Make a contact sheet of every drawn star on f68r2 and on f68r3 (crop ±35 px around each centre, 4×).
     Classify each centre as `ring`, `dot` or `plain` **before** assigning labels.
  2. Then place every `@Ls`/`@La` label on its star by reading it at 4× zoom.
  3. Only stars with a label count. Unlabelled stars are excluded.
  4. A matching label that cannot be placed confidently is excluded and reported.
- **Statistic:** X = the number of matching labels on marked stars (`ring` or `dot`), summed over the two panels.
- **Null:** labels are assigned to labelled stars at random within each panel (hypergeometric per panel), and the
  panel results are convolved for an exact P(X ≥ observed).
- **Threshold:** p < 0.05, one-sided.
- **Secondary (reported, not confirmatory):** the same test with only `ring` counted; the result pooled with f68r1
  (which includes the discovery data).

## Known weaknesses

- One reader (me), not blind: label text is partly visible at the edge of the centre crops.
- There are at most 4 matching labels, so the test has very little power. A null result does not rule the idea out.
- f68r3's stars sit inside a large wheel, and many of its labels may not belong to a single star.
