# Is "o" a label/name-forming prefix?

Pre-registration: `analyses/o_prefix_prereg.md`. 10,000 shuffles within word length, seed 20261002.

- Label words starting with o (4+ letters): 430; of these, **175 (41%)** are o + an existing paragraph word.
- Paragraph-only words starting with o: 1111; of these, 438 (39%) are o + an existing word.
- Expected for labels at the same lengths: 182.6
- p = 0.84 → **NOT SUPPORTED**

## By label group (descriptive)

| Group | o-words | o + existing word | Rate |
|---|---:|---:|---:|
| zodiac figures | 181 | 74 | 41% |
| other | 109 | 52 | 48% |
| plant parts | 90 | 52 | 58% |
| stars | 48 | 24 | 50% |
| pools/tubes | 36 | 22 | 61% |
| bathing figures | 31 | 23 | 74% |
| jars | 21 | 5 | 24% |

Paragraph-only o-words for comparison: 39%.

## Where the remainders occur in paragraph text (descriptive)

- Remainders: share of their paragraph uses that are line-first 11.8%, paragraph-first 0.7%
- All paragraph words: line-first 11.8%, paragraph-first 0.8%

Most common remainders (label = o + remainder): aiin (1), cham (1), chey (1), chol (1), chory (1), ckhol (1), ckhy (1), cphy (1), cthey (1), ctho (1), cthy (1), daiin (1), dair (1), dal (1), ddy (1)

Note: the "most common remainders" line counts distinct label types, so every remainder shows 1. It is a list of
examples, not a ranking.

## Reading the result

- "o" + existing word is just as common among ordinary paragraph words (39%) as among labels (41%). **"o" is a
  general, separable prefix in Voynich word-building**, not a marker of labels or names.
- This weakens the interpretation in `plant_star_report.md` and `name_map_report.md` that "o" forms names. The
  links themselves (shared unusual spellings between plant openings and star labels, and between bath openings and
  plant-part labels) are unaffected. They now read best as **shared roots**, with "o" as an ordinary prefix.
- Descriptive, untested: the share varies by label group, from bathing-figure labels (74%) and pools (61%) down to
  jars (24%).
- The remainders are not unusually line- or paragraph-first (11.8% vs 11.8%; 0.7% vs 0.8%).
