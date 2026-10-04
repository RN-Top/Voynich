# Pre-registration: does the bath-section text share roots with the spring zodiac labels?

Date: 2026-10-04. Written before any comparison.

## Idea

The zodiac figures stand in tubs only on the spring pages (March–May; `output/tub_season_report.md`). If the zodiac
pages are a bathing calendar, the bath section's text (section "Biological", f75–f84) should share more vocabulary
with the spring zodiac labels than with the other zodiac labels.

## Data

- **Labels:** zodiac figure labels (`Lz`) from `zodiac_days_test.zodiac_labels()`, split into:
  - **spring:** Pisces, Aries (dark and light), Taurus (dark and light);
  - **rest:** Gemini to Sagittarius.
- **Bath text:** all paragraph words of the Biological section.
- **Roots:** from `root_dictionary_test.root_of`.

## Statistic

- For each label, record 1 if its root occurs in the bath text, otherwise 0.
- **D** = share of spring labels hit − share of other labels hit.

## Null and threshold

- Shuffle the spring/rest assignment at the level of whole signs: 5 spring sign-pages drawn from the 11 sign-pages,
  over all C(11,5) = 462 splits, exactly. Shuffling whole pages keeps each page's own style together.
- One-sided p < 0.05.

## Weakness

Spring pages may differ from the others in writing style (as they do in drawing style). With only 462 splits the
smallest possible p is about 0.002.

## Amendment (before any comparison)

`zodiac_labels()` joins each half-sign onto one page: Aries becomes f70v1 plus f71r, and Taurus becomes f71v plus
f72r1. That gives 10 sign units, not 11. The spring group is therefore Pisces, Aries and Taurus (3 of 10), and the
null runs over all C(10,3) = 120 splits. The smallest possible p is 1/120 ≈ 0.008.
