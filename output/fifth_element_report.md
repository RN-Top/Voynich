# Fifth-element cycle test

Pre-registration: `analyses/fifth_element_prereg.md`. Paragraph text, 35,038 words; the fifth element is the 4,993 words with no role (`?`). Seed 20261002.

| Placement | 2-word score | 5-word window score |
|---|---:|---:|
| C?LPR | 0.1671 | 0.00005 |
| CL?PR | 0.1544 | 0.00027 |
| CLP?R | 0.1976 | 0.00016 |
| CLPR? | 0.1987 | 0.00027 |

Best placement: **CL?PR** (5-word score 0.00027).

| Control | n | 5-word mean | p | 2-word mean | p (not used for verdict) |
|---|---:|---:|---:|---:|---:|
| within_line_shuffle | 2000 | 0.00040 | 0.945 | 0.1930 | 0.0015 |
| markov1_twins | 1000 | 0.00047 | 0.971 | 0.1968 | 0.195 |
| markov2_twins | 1000 | 0.00050 | 0.988 | 0.1983 | 0.444 |

**Verdict: NOT SUPPORTED** (needs p < 0.01 against both Markov twins).

Descriptive: the best placement ranks 2 of 24 possible five-step cycles. Top three: CLR?P (0.00048), CLPR? (0.00027), CL?PR (0.00027).

Most common last two letters of the `?` words: -ir (534), -ho (391), -eo (390), -s (317), -os (305), -in (258), -es (257), -od (189).
