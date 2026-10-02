# Pre-registration: a map of name links between sections

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Background

`output/plant_star_report.md` found that herbal-page opening words share unusual spellings with star labels (13 vs
4.4, p = 0.0002). This asks whether that is a single link or part of a wider system, by testing every pairing of
paragraph-opening words from one section with one label type.

## Data (ZL3b, same word reading and "unusual chunk" definition as analyses/plant_star_test.py)

- **Opening words:** the first word of every paragraph-start line (P locus marked `@`), grouped by section: Herbal,
  Pharmaceutical, Biological, Stars/Recipes, Cosmological, Astronomical/Zodiac (sections with at least 10
  opening words).
- **Label groups:** Ls (stars), Lz (zodiac figures), Ln (bathing figures), Lt (pools/tubes), Lc (jars), Lf (plant
  parts), and other labels (L0, La, Lp, Lx).

## Statistic and null

For each cell (section × label group): S = number of opening words that share at least one unusual 3-letter chunk
with the label group. Null: the same number of label words drawn at random from all **other** label groups
(2,000 draws, seed 20261002).

## Decision

Threshold p < 0.01 divided by the number of cells (Bonferroni). Cells that pass are reported as links. The
Herbal × star cell repeats the earlier finding, and is reported but not counted as new. The map is **wider than
one link** if at least one other cell passes.

---
Amendments (dated, below this line only):

**2026-10-02, calibration fix (after seeing the first run).** With 2,000 draws the smallest possible p is 0.0005,
which is above the Bonferroni threshold (0.00024), so no cell could pass. The first run is kept as
`output/name_map_report_2000draws.md` (0 cells passing; the smallest p values were Herbal × stars and Biological ×
plant parts, both 0.0005). The test is rerun once with 20,000 draws. Nothing else changes.
