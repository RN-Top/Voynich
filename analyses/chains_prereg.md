# Pre-registration: correspondence chains (herb → star → body)

Date: 2026-10-04. Written and committed before any code for this test exists.

## Idea

A medieval medical-astrology book works by correspondence: one plant ↔ one star or planet ↔ one part of the body ↔
one remedy. If the Voynich does this, the same name roots should run through the sections as **chains**, not only
as pairs. Two pairwise links already hold up: herbal openings ↔ star labels, and bath openings ↔ plant-part labels.

## Units

Same machinery as `plant_star_test.py` and `name_map_test.py`:

- Words come from `words_of`, and 3-letter chunks from `chunks`.
- A chunk is **rare** if it occurs in fewer than `RARE_TYPES` (20) word types in the whole transcription.

## Groups

| Group | Contents |
|---|---|
| H (herb) | First word of every herbal-section paragraph (`P` loci starting a paragraph). |
| S (star) | All `Ls` label words. |
| B (body) | All `Ln` (bathing figures), `Lt` (pools and tubes) and `Lz` (zodiac figures) label words. |
| R (remedy) | All `Lc` (jars) and `Lf` (plant parts) label words. Used only in the secondary test. |

## Primary test

- **Statistic:** C = the number of rare chunks that occur in H **and** S **and** B.
- **Null:** H and S are kept as they are, so the known herb–star link stays in the null. B is replaced by a random
  draw of the same number of label words from all label words that are not in S or B (`R`, `L0`, `La`, `Lp`,
  `Lx`). This asks whether the shared herb–star roots continue into the body labels more than into other labels.
  20,000 draws, seed 20261005.
- **Prediction:** C exceeds the null. One-sided p < 0.05.

## Secondary tests (reported, not confirmatory)

1. The same test with R in place of B (herb → star → remedy).
2. The four-way count H ∩ S ∩ B ∩ R, with B and R together replaced by random draws from the remaining labels.
3. Every complete chain is listed with an example word from each group, for reading.

## Known weaknesses

- **Pool overlap.** The null pool shares the "o + gallows" label style with B, which makes the test conservative.
  That style was matched in the earlier test.
- **Small numbers.** The labels are few, so C may be small.
- **What a chunk link means.** A shared rare chunk is a weak similarity measure. A chain is suggestive, not proof of
  meaning.

## Implementation note (2026-10-04, recorded after the run)

For the four-way secondary test there were fewer "other" labels (392) than B and R together (721), so the null drew
them with replacement. The test is secondary and was not significant either way.
