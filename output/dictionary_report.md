# Do word beginnings follow what a label is attached to?

Pre-registration: `analyses/dictionary_prereg.md`. 10,000 within-page shuffles, seed 20261002.

| Test | Labels | Beginning MI | Shuffled | p | Result | Ending MI | Shuffled | p |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| D1 pharmaceutical: jar vs plant part | 40 jar / 193 plant part | 0.170 | 0.136 | 0.0799 | FAIL | 0.255 | 0.167 | 0.002 |
| D2 biological: figure vs pool/tube | 63 bathing figure / 47 pool / tube | 0.191 | 0.182 | 0.344 | FAIL | 0.166 | 0.171 | 0.524 |

**Verdict: NOT SUPPORTED** (each test needs p < 0.005).

## Candidate dictionary leads (descriptive, not tested)

Beginnings most over-represented on each picture kind (count, times expected):

- **jar**: ko- (3, x3.5), ok- (10, x1.5), da- (3, x1.1), ot- (5, x0.7)
- **plant part**: ol- (9, x1.2), ar- (4, x1.2), sa- (11, x1.2), do- (4, x1.2), dy- (3, x1.2)
- **bathing figure**: do- (4, x1.7), da- (8, x1.1), ok- (17, x1.1), ol- (7, x0.9), ot- (8, x0.6)
- **pool / tube**: ot- (15, x1.5), ol- (7, x1.2), ok- (11, x0.9), da- (5, x0.9)

Beginnings most concentrated in each section of paragraph text, relative to the same Currier language (at least 20 uses):

- **Herbal (A)**: ka- (x1.3), kc- (x1.3), ky- (x1.3), tc- (x1.3)
- **Pharmaceutical (A)**: te- (x2.2), sa- (x1.8), ol- (x1.7), ai- (x1.6)
- **Biological (B)**: rc- (x2.0), so- (x2.0), ls- (x1.7), ol- (x1.7)
- **Cosmological (B)**: yt- (x4.0), or- (x2.2), yk- (x2.1), od- (x2.1)
- **Herbal (B)**: dy- (x2.5), yk- (x2.4), to- (x2.2), kc- (x2.0)
- **Pharmaceutical (B)**: ok- (x1.4), ot- (x1.3), ch- (x1.2), ol- (x1.2)
- **Stars/Recipes (B)**: lk- (x1.8), oa- (x1.6), ra- (x1.5), pa- (x1.5)

## Reading the result

- Labels on different kinds of picture do **not** start differently in a way we can detect, on either the
  pharmacy or the bath pages. The samples are small (40 jar labels; 47 pool labels), so a weak effect could be
  missed. The topic signal found in paragraph text (`writing_types_report.md`) does not show up at label level.
- Not part of the verdict, but worth following: on the pharmacy pages the **endings** of jar labels differ from
  plant-part labels (p = 0.002). Jar and plant labels may be different kinds of word, such as names versus
  descriptions, rather than different topics.
- The lists above are leads, not readings. With counts this small, most of them will be noise.
