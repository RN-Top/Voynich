# Pre-registration: re-running earlier leads on the integrated file

Written 17 November 2026, before running. Runner: `analyses/rerun_with_integrated.py`.
Report: `output/rerun_integrated_report.md`.

## What changes with the new file

The words, labels and label positions in `voynich_integrated.json` come from the same ZL3b
transcription the earlier tests used, so tests that only use labels and their positions cannot change.
Those are the zodiac label tests (diagram labels as measurements, label gradient, counting) and label
beginnings vs picture kind, which already took picture kind from the label codes. The runner checks that
their inputs are identical and does not re-run them.

What the new file adds is **what is actually drawn on each page** (ZL3b's illustration type). The earlier
tests decided which pages were "plant pages", "bath pages" and so on from folio-number ranges
(f1–f66 = herbal, f75–f84 = biological, …). That range rule counts f57v (a ring diagram), f58r/f58v and
f65–f66 (text and star pages) as herbal, and it misses the herbal pages inside f87–f102. The re-runs swap
the range rule for the drawn type. Nothing else changes.

## Tests re-run, most promising lead first

| # | Test | Original result | Original pass rule |
|---|---|---|---|
| 1 | Plant openings and star names (`plant_star_test.py`) | Supported, 13 vs 4.4, p = 0.0002 | p < 0.01 |
| 2 | Herb → star → body / remedy chains (`chains_test.py`) | Primary not supported; herb → star → remedy 3 chains, secondary | p < 0.05 |
| 3 | Ground test, labels in their own page's text (`ground_test.py`) | Not supported, p = 0.45 / 0.38 | p < 0.01 |

The scripts are the October versions, restored unchanged from git history. Each is first run on the old
input to confirm it reproduces the October numbers, then on the integrated file.

## Multiple comparisons

There are five decisions (test 1; test 2 primary and two secondaries; test 3 counted once as G1 or G2).
A new "pass" counts only if it also survives Holm correction, with each test's own alpha as the family
level. A result that changes from pass to fail on the new file is reported as a lost lead.
