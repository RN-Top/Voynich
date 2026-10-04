# Pre-registration: the metal key (planet order as "frequency") and sevens

Date: 2026-10-04. Written and committed before any code for these tests exists.

## Erin's idea

Flowers → colour → metal → planet. Each metal has a place on the medieval scale of the planets (the "music of the
spheres"), and the system runs in sevens: 7 metals, 7 planets, 7 days.

## The key (fixed in advance, from period sources, not from the manuscript)

Planetary tinctures as used by late-medieval heralds (e.g. Sicily Herald, *Le blason des couleurs*, c. 1430s), with
the standard planet–metal pairs:

| Flower colour (`flower_colours.csv`) | Tincture | Planet | Metal |
|---|---|---|---|
| yellow | or | Sun | gold |
| white | argent | Moon | silver |
| red | gules | Mars | iron |
| blue | azure | Jupiter | tin |
| green | vert | Venus | copper |
| (none in the data) | sable / purpure | Saturn / Mercury | lead / quicksilver |

The key is one-to-one, so **grouping by metal is the same as grouping by colour**. That was already tested and was
not supported (`flower_colour_report.md`, p = 0.74). Only the **order** is new.

## Test 1: does the planetary scale order the text?

- **Scale:** the Ptolemaic order from Earth outward, which was also the order of the notes in the music of the
  spheres: Moon 1, Mercury 2, Venus 3, Sun 4, Mars 5, Jupiter 6, Saturn 7.
- **Pages and similarity:** as in `flower_colour_test.py`: the 86 herbal pages with a single flower colour, and the
  cosine similarity of their word-root count vectors.
- **Statistic:** Spearman ρ between |rank difference| and similarity, over **pairs of pages with different
  colours only**. This makes it independent of the earlier same-colour test.
- **Prediction:** ρ < 0, i.e. pages whose metals are neighbouring notes have more similar text.
- **Null:** shuffle the colour labels within Currier language, 10,000 times, seed 20261004.
- **Threshold:** one-sided p < 0.025 (Bonferroni over the two tests).

## Test 2: sevens in book order

- **Pages:** all herbal pages with paragraph text, in their current book order (ZL3b folio order).
- **Statistic:**

  D7 = mean similarity of pages 7 apart − ½ × (mean similarity at lag 6 + mean similarity at lag 8).

  This asks whether pages 7 apart are more alike than their neighbours at lags 6 and 8, so the general "nearby pages
  are alike" effect cancels out.
- **Prediction:** D7 > 0 (a 7-page cycle).
- **Null:** shuffle page order within Currier language, 10,000 times, seed 20261004.
- **Threshold:** one-sided p < 0.025.
- **Descriptive:** the same contrast for lags 3–12, reported alongside so a 7 can be compared with other numbers.

## Known weaknesses

- **Colours:** judged by eye at low resolution, and they may have faded. Blue (Jupiter) dominates with 50 of 86
  pages, and only 1 page is yellow (Sun). Saturn and Mercury have no pages.
- **Book order:** the current order is not the original binding (bifolios were rearranged), so a real 7-cycle could
  be hidden.
- **Scale direction:** some authors reverse the order or give different notes. Test 1 uses distance on the scale, so
  only the order matters, not the direction.
