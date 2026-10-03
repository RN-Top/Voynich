# Pre-registration: does anything pulse at a regular beat inside lines or down pages?

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Idea (from the project author: frequency, transmission, receiver)

A signal-like or metrical text would show a regular beat: a feature recurring every k words within lines, or rising
and falling in waves from line to line down a page.

## Data

Paragraph text, Currier A and B separately (canonical clean words).

## R1: beat inside lines

Interior words only (not first or last on their line). Feature: ending class (`structural_validation.ending_of`).
m(k) = number of interior word pairs k apart on the same line with the same ending class. A beat at k shows as a
local peak: peak(k) = m(k) − (m(k−1) + m(k+1)) / 2, for k = 2…6. Null: interior words shuffled within lines
(2,000 shuffles, seed 20261003). Bonferroni over 5 lags × 2 dialects: p < 0.001.

## R2: waves down the page

For each page, the series of line values "share of the line's words beginning with qo". For line lags k = 2…8:
a(k) = mean product of mean-centred values of lines k apart on the same page. Local peak:
peak(k) = a(k) − (a(k−1) + a(k+1)) / 2. Null: line order shuffled within each page (2,000 shuffles). Bonferroni
over 7 lags × 2 dialects: p < 0.0007.

## Decision

A beat or wave is reported for any lag that passes. Otherwise **no rhythm found**.

---
Amendments (dated, below this line only):
