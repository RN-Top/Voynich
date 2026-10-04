# Pre-registration: do f67r2's crescents run through a waxing/waning cycle?

Date: 2026-10-04. Written before any crescent direction is recorded.

## Idea

The coloured crescent on each of f67r2's 12 moons sits on one side of the face. Medieval moon-phase drawings put
the lit crescent on one side when the Moon is waxing and on the other when it is waning. If the ring shows a cycle
of phases, crescents facing the same way should come in **runs** around the ring.

## Recording

- **Source:** `uploads/yale_hires/f67r_spread.jpg`; moon positions from `analyses/moon_months_f67r2.csv`.
- **Crops:** each moon is cropped and rotated so that the ring centre is directly below it. To the right is then
  clockwise.
- **Direction:** the crescent is recorded as
  - `CW`: thicker part on the clockwise side;
  - `ACW`: thicker part on the anticlockwise side;
  - `out` or `in`: thicker part toward the rim or the centre, or unclear.

  Directions are recorded on a contact sheet before computing anything.

## Test

- **Moons used:** only those recorded `CW` or `ACW`, in ring order (circular).
- **Statistic:** C = the number of direction changes between neighbours.
- **Null:** every circular arrangement with the same counts, enumerated exactly.
- **Prediction:** C is **smaller** than chance (runs).
- **Threshold:** one-sided p < 0.05. If fewer than 8 moons are usable, the test is reported as not runnable.

## Secondary (descriptive)

Cross-tabulation of crescent direction against moon colour (red/gold), with Fisher's exact test.
