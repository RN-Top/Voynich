# Scribe vs topic

Pre-registration: `analyses/scribes_prereg.md`. Seed 20261003.

## Who wrote what (paragraph words)

```
section  Astronomical/Zodiac  Biological  Cosmological  Herbal  Pharmaceutical  Stars/Recipes
hand                                                                                         
1                          0           0             0    7371            3193              0
2                          0        6818          1665    2354               0              0
3                          0           0             0     798             535          10428
4                        505           0            39       0               0              0
5                          0           0             0     873               0              0
```

## S1. Writer effect, topic fixed (herbal pages only)

- Scribes: 1 (86), 2 (20), 5 (7), 3 (3). Root–scribe information 0.1772 vs shuffled 0.0489 (excess 0.1283); p = 0.0005 → **PASS**

## S2. Topic effect, writer fixed

- Scribe 1: Pharmaceutical (26), Herbal (86). Root–section information 0.1031 vs 0.0177 (excess 0.0854); p = 0.0005 → **PASS**
- Scribe 2: Herbal (20), Biological (20), Cosmological (6). Root–section information 0.1197 vs 0.0343 (excess 0.0854); p = 0.0005 → **PASS**
- Scribe 3: Stars/Recipes (22), Herbal (3), Pharmaceutical (6). Root–section information 0.0613 vs 0.0456 (excess 0.0157); p = 0.014 → **FAIL**
- **Topic effect confirmed with writer fixed: YES**

## S3. Do the rules hold for every scribe?

| Scribe | Interior pairs | Word order excess (bits) | p | Strongest link | Its p |
|---|---:|---:|---:|---|---:|
| 1 | 6,181 | 0.0711 | 0.000999 | ending → beginning | 0.002 |
| 2 | 7,191 | 0.1147 | 0.000999 | ending → beginning | 0.002 |
| 3 | 8,208 | 0.0970 | 0.000999 | ending → beginning | 0.002 |
| 4 | <1500 | | | too little text | |
| 5 | <1500 | | | too little text | |

**Rules universal across qualifying scribes: YES**

## Scribe profiles (descriptive)

| Scribe | Words | Mean length | Common beginnings | Common endings |
|---|---:|---:|---|---|
| 1 | 10,564 | 4.74 | ch- 20%, da- 9%, qo- 9%, sh- 9% | -in 15%, -ol 15%, -or 10%, -hy 9% |
| 2 | 10,837 | 4.92 | qo- 19%, ch- 13%, sh- 10%, ol- 7% | -dy 27%, -in 15%, -ey 10%, -ol 9% |
| 3 | 11,761 | 5.18 | qo- 16%, ch- 16%, sh- 8%, ot- 7% | -in 19%, -dy 19%, -ey 12%, -ar 9% |
| 4 | 544 | 4.80 | ch- 15%, sh- 10%, da- 8%, ok- 6% | -ey 14%, -in 12%, -dy 9%, -al 9% |
| 5 | 873 | 5.22 | ch- 16%, qo- 11%, sh- 11%, da- 7% | -dy 32%, -ey 9%, -in 7%, -al 7% |

## Reading the result

- **Both effects are real.** Herbal pages written by different scribes use different roots (S1, excess 0.128
  bits). Within a single scribe, roots still change with the section (S2: scribes 1 and 2 pass; scribe 3, whose
  non-recipe pages are few, does not). So the "topic" findings are not just scribe habits, and the "scribe"
  differences are not just topic.
- **Caveat on S1:** scribe 1 writes Currier A and the others mostly Currier B, so writer and dialect cannot be
  separated on herbal pages.
- **The grammar holds for every scribe with enough text** (1, 2, 3). Word order carries information, and the
  strongest link is always a word's ending → the next word's beginning. **These are rules of the shared writing
  system, not one person's habit.**
- **The plant–star link crosses writers.** The herbal openings are by scribe 1 and the star labels by scribe 4, so
  their shared roots come from two different people.
- Each scribe's text is now separated, in book order, in `output/scribes/scribe_<n>.txt` (made by
  `analyses/split_by_scribe.py`).
