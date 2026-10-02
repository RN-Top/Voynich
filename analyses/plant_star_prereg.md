# Pre-registration: do plant-page opening words share unusual spellings with star labels?

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Idea (from the project author's f56r find)

The first word of f56r (a plant page) begins "o" + rare symbol @167, as does a star label on f68r2, and a star
label on f68r1 begins with @167. Medieval astrology linked particular stars to particular herbs (e.g. the
Hermetic *Book of the Fifteen Stars*). If the book links plants to stars, the opening words of plant pages
(often taken to be the plant's name) might share unusual spellings with star labels.

## Data (ZL3b)

- **Opening words:** the first word of the first paragraph line of every Herbal-section page.
- **Star labels:** every word of the star-label loci (code Ls).
- **Other labels:** every word of all other label loci (codes L0, La, Lc, Lf, Ln, Lp, Lt, Lx, Lz).
- Words are read with rare symbols kept, each `@nnn;` counted as one letter of its own. Comments and
  uncertain-reading brackets are removed (first reading kept), and `,` `.` `<->` split words.

## Unusual spelling

A three-letter chunk, with word start and end marked, that occurs in fewer than 20 different word types in the
whole transcription.

## Statistic

S = number of opening words that share at least one unusual chunk with at least one star-label word.

## Null

Draw the same number of label words as there are star-label words, at random from the other labels (10,000
draws, seed 20261002), and count S for each draw. Pass: p < 0.01.

## Decision

**Supported** if it passes; the matching opening words, star labels and shared chunks are then listed as leads.
**Not supported** otherwise.

---
Amendments (dated, below this line only):
