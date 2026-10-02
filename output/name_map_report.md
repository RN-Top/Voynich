# A map of name links between sections

Pre-registration: `analyses/name_map_prereg.md`. 42 cells, Bonferroni threshold p < 0.00024; 20,000 draws per cell, seed 20261002.

| Opening words from | Label group | Openings | Label words | Shared | Expected | Ratio | p | Link? |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Biological | plant parts | 32 | 210 | 3 | 0.6 | 5.12 | 5e-05 | **yes** |
| Herbal | stars | 114 | 86 | 13 | 4.4 | 2.93 | 0.0001 | **yes** |
| Pharmaceutical | stars | 52 | 86 | 7 | 1.5 | 4.57 | 0.0013 |  |
| Astronomical/Zodiac | jars | 26 | 40 | 3 | 0.4 | 7.96 | 0.00275 |  |
| Astronomical/Zodiac | stars | 26 | 86 | 3 | 0.7 | 4.03 | 0.0272 |  |
| Cosmological | stars | 17 | 86 | 1 | 0.1 | 11.95 | 0.0837 |  |
| Stars/Recipes | plant parts | 23 | 210 | 3 | 1.6 | 1.90 | 0.178 |  |
| Stars/Recipes | pools/tubes | 23 | 56 | 1 | 0.4 | 2.37 | 0.361 |  |
| Cosmological | plant parts | 17 | 210 | 1 | 0.4 | 2.68 | 0.373 |  |
| Biological | stars | 32 | 86 | 1 | 0.5 | 2.00 | 0.429 |  |
| Herbal | jars | 114 | 40 | 3 | 2.4 | 1.23 | 0.43 |  |
| Pharmaceutical | plant parts | 52 | 210 | 5 | 4.3 | 1.17 | 0.435 |  |
| Stars/Recipes | bathing figures | 23 | 65 | 1 | 0.6 | 1.81 | 0.445 |  |
| Pharmaceutical | jars | 52 | 40 | 1 | 0.9 | 1.07 | 0.539 |  |
| Astronomical/Zodiac | bathing figures | 26 | 65 | 1 | 0.7 | 1.38 | 0.544 |  |
| Pharmaceutical | other | 52 | 392 | 8 | 7.7 | 1.04 | 0.545 |  |
| Herbal | other | 114 | 392 | 17 | 16.8 | 1.01 | 0.546 |  |
| Stars/Recipes | stars | 23 | 86 | 1 | 0.7 | 1.34 | 0.555 |  |
| Herbal | plant parts | 114 | 210 | 10 | 10.9 | 0.91 | 0.668 |  |
| Astronomical/Zodiac | plant parts | 26 | 210 | 2 | 2.1 | 0.94 | 0.711 |  |
| Herbal | pools/tubes | 114 | 56 | 2 | 3.5 | 0.57 | 0.853 |  |
| Stars/Recipes | zodiac figures | 23 | 350 | 2 | 2.7 | 0.74 | 0.874 |  |
| Herbal | zodiac figures | 114 | 350 | 12 | 16.1 | 0.75 | 0.939 |  |
| Pharmaceutical | zodiac figures | 52 | 350 | 4 | 6.9 | 0.58 | 0.975 |  |
| Biological | other | 32 | 392 | 1 | 1.9 | 0.53 | 0.981 |  |
| Herbal | bathing figures | 114 | 65 | 1 | 4.1 | 0.24 | 0.982 |  |
| Astronomical/Zodiac | other | 26 | 392 | 2 | 4.2 | 0.48 | 0.993 |  |
| Astronomical/Zodiac | zodiac figures | 26 | 350 | 1 | 3.7 | 0.27 | 0.998 |  |
| Stars/Recipes | other | 23 | 392 | 1 | 3.9 | 0.25 | 0.999 |  |
| Astronomical/Zodiac | pools/tubes | 26 | 56 | 0 | 0.7 | 0.00 | 1 |  |
| Biological | zodiac figures | 32 | 350 | 0 | 2.1 | 0.00 | 1 |  |
| Biological | bathing figures | 32 | 65 | 0 | 0.4 | 0.00 | 1 |  |
| Biological | pools/tubes | 32 | 56 | 0 | 0.4 | 0.00 | 1 |  |
| Biological | jars | 32 | 40 | 0 | 0.3 | 0.00 | 1 |  |
| Cosmological | other | 17 | 392 | 0 | 1.2 | 0.00 | 1 |  |
| Cosmological | zodiac figures | 17 | 350 | 0 | 1.1 | 0.00 | 1 |  |
| Cosmological | bathing figures | 17 | 65 | 0 | 0.2 | 0.00 | 1 |  |
| Cosmological | pools/tubes | 17 | 56 | 0 | 0.1 | 0.00 | 1 |  |
| Cosmological | jars | 17 | 40 | 0 | 0.1 | 0.00 | 1 |  |
| Pharmaceutical | bathing figures | 52 | 65 | 0 | 1.6 | 0.00 | 1 |  |
| Pharmaceutical | pools/tubes | 52 | 56 | 0 | 1.4 | 0.00 | 1 |  |
| Stars/Recipes | jars | 23 | 40 | 0 | 0.4 | 0.00 | 1 |  |

**Cells passing:** 2 (1 besides Herbal × stars). **Map wider than one link: YES.**

## Reading the result

- This rerun uses 20,000 draws. The first run (2,000 draws) could not reach the threshold; see the amendment in
  `analyses/name_map_prereg.md` and `output/name_map_report_2000draws.md`.
- **Two links pass after correction for 42 tests:** Herbal openings × star labels (the earlier finding) and
  **Biological (bath-page) openings × pharmacy plant-part labels** (3 vs 0.6 expected, p = 0.00005). The second
  rests on only 3 opening words, so it is fragile.
- **Same rule in both.** The matches behind the new link (descriptive):
  - f82v opening **tokol** ↔ plant-part labels **otokol** (f88v), **otoky** (f88r, f99v)
  - f83v **poldaky** ↔ **dakocth** (f100r)
  - f84v **otdy** ↔ **otdordy** (f88v)
  
  *tokol → otokol* is exactly "o" + the paragraph-opening word.
- **Near misses that point the same way** (not passing the corrected threshold): Pharmacy openings × star labels
  (7 vs 1.5, p = 0.0013), e.g. *kosar → okos*, *koaiphhy → okoaly*; Zodiac openings × jar labels (3 vs 0.4).
- Overall: labels in one part of the book repeatedly look like **"o" + a word that opens a paragraph in another
  part**. That is consistent with a word-building rule where "o" marks a name or label form. The evidence is two
  passing links plus several near misses, each resting on small numbers.
