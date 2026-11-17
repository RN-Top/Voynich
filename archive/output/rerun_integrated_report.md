# Earlier leads re-run on the integrated file

Pre-registration: `analyses/rerun_integrated_prereg.md`. Runner: `analyses/rerun_with_integrated.py`.
The text in the integrated file is line-for-line identical to ZL3b (5,385 lines checked). The only change
is that page types now come from what is drawn on each page, not from folio-number ranges. That moves 32 pages,
for example 16 plant pages inside f87–f102 that were counted as pharmacy pages, and f1r (text only) is no
longer counted as a plant page. Full list: `output/rerun_integrated_page_types_changed.json`.

Each script first reproduced its October numbers on the old input (`*_report_original.md`).

| Test | Old input | Integrated file | Change |
|---|---|---|---|
| Plant openings vs star names | 13 vs 4.4, p = 0.0002, supported | **14 vs 4.5, p = 0.0001, supported** | Holds and gets slightly stronger. Survives Holm correction (5 decisions). |
| Herb → star → body (primary) | 1 vs 4.8, p = 1.0 | 1 vs 5.5, p = 1.0 | Still not supported |
| Herb → star → remedy (secondary) | 3 vs 1.15, p = 0.075 | 3 vs 1.47, p = 0.21 | Weaker. This was a hint, and it fades. |
| Herb → star → body → remedy | 1 vs 1.0, p = 0.70 | 1 vs 1.3, p = 0.70 | No change |
| Labels in own page's text (G1 bath / G2 all) | p = 0.45 / 0.38 | p = 0.45 / 0.15 | Still not supported |

## What's new in the plant–star matches

- Lost: f1r *fachys* ~ f67r2 *octhys*, because f1r has no plant drawing.
- Gained, from herbal pages the old range rule missed: f90r2 *toealchs* ~ f67r2 *qotoear* and f68r2 *otoeeo*,
  and f90v2 ~ f68r2 (a shared rare-character chunk).

## Not re-run (cannot change)

The zodiac label tests (labels as measurements, label gradient, counting) and label beginnings vs picture kind
use only the labels, their codes and their clock positions. These are identical in the new file, so a re-run
would give the same numbers.
