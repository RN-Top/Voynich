# Writing types, word order and topic location

Pre-registration: `analyses/writing_types_prereg.md`. Seed 20261002.

## Profiles

| Type | Words | Distinct | Mean length | Common beginnings | Common endings | Words also in other paragraph text |
|---|---:|---:|---:|---|---|---:|
| Paragraph, Currier A | 11,362 | 3,198 | 4.75 | ch- 19%, qo- 10%, da- 9%, sh- 9% | -in 15%, -ol 14%, -or 10%, -hy 9% | 76% |
| Paragraph, Currier B | 23,676 | 4,900 | 5.06 | qo- 17%, ch- 15%, sh- 9%, ok- 6% | -dy 23%, -in 17%, -ey 11%, -ar 8% | 68% |
| Ring text (C) | 2,376 | 1,116 | 4.74 | ot- 17%, ch- 16%, ok- 11%, sh- 6% | -dy 12%, -ar 11%, -ey 10%, -in 10% | 77% |
| Labels (L) | 1,190 | 856 | 5.23 | ot- 17%, ok- 16%, ch- 6%, da- 5% | -dy 15%, -ar 9%, -al 8%, -in 6% | 60% |
| Radial text (R) | 354 | 283 | 5.18 | ok- 17%, ch- 12%, ot- 9%, da- 8% | -dy 15%, -ey 14%, -ar 9%, -hy 8% | 73% |

For the paragraph types, the last column compares A with B; for the others, with all paragraph text.

## W1. Does word order carry information? (interior words only)

| Type | Pairs | MI (bits) | Shuffled mean | Excess | p | Result |
|---|---:|---:|---:|---:|---:|---|
| Paragraph, Currier A | 6,721 | 1.8775 | 1.8056 | 0.0719 | 0.000999 | order matters |
| Paragraph, Currier B | 16,038 | 2.1264 | 1.9895 | 0.1368 | 0.000999 | order matters |
| Ring text (C) | 2,125 | 0.8958 | 0.8141 | 0.0817 | 0.000999 | order matters |
| Labels (L) | <1500 | | | | | too small |
| Radial text (R) | <1500 | | | | | too small |

## W2. Does the start or the end of a word carry the topic? (paragraph text)

| Word part | Distinct values | MI with section | Shuffled mean | Excess | p |
|---|---:|---:|---:|---:|---:|
| beginning | 203 | 0.1559 | 0.0608 | 0.0951 | 0.0005 |
| ending | 204 | 0.1188 | 0.0585 | 0.0603 | 0.0005 |

**W2 result:** beginning > ending (larger excess first)

## Extra check (added after the run, not pre-registered)

Identical neighbouring words ("qokedy qokedy") are about 0.8% of pairs. Removing the second word of each such pair
and rerunning W1 changes nothing: excess 0.073 (A), 0.140 (B), 0.075 (ring text), all p = 0.001. The word-order
effect is not caused by repeats.

## What this means for decoding

- **Word order carries information** in all three testable types, about twice as much in Currier B as in A.
  Words depend on their neighbours, which a list, a table or randomly generated text would not show.
- **The beginning of a word tracks the topic more than the ending does.** This holds even with the A/B
  difference removed. So a dictionary should be built on word beginnings (with the rest of the word), and
  endings treated as grammar or line-layout markers (like -m/-am at line ends).
- Next step: group words by beginning and see which beginnings concentrate in which section and next to which
  pictures (labels), the way a made-up language with category prefixes would.
