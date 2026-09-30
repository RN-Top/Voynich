# Structural validation report

Generated 2026-09-30T20:54:21+00:00 by `structural_validation.py` (seed 20260930, corpus SHA-256 `3e617b2dd4c17736…`).
Scope: locus types P, 35,038 tokens, 4,130 lines, 207 folios.

Every number below is recomputed from the corpus on each run. Nothing is hard-coded.
Significance threshold for PASS: p < 0.01.

## 1. Line-end enrichment of -m / -am

- 861 tokens end in -m/-am; 605 are line-final.
- Line-end incidence 14.7% vs mid-line 0.8%; odds ratio 20.70; Fisher p (greater) < 1e-300.
- Within-line shuffle (20,000 perms): observed 605 vs null mean 102.1, p = 5.00e-05 → **PASS**

All ending classes, for comparison (lines of ≥ 2 tokens):

| ending | state | n | share line-final | odds ratio | Fisher p (greater) |
|---|---|---:|---:|---:|---:|
| `am` | R | 684 | 73.0% | 22.99 | 2.1e-314 |
| `m` | R | 177 | 59.9% | 11.52 | 4.2e-53 |
| `y` | P | 4236 | 18.3% | 1.85 | 2.3e-41 |
| `dy` | C | 2275 | 18.5% | 1.80 | 6.3e-23 |
| `aiiin` | L | 113 | 16.8% | 1.52 | 6.7e-02 |
| `al` | P | 1814 | 13.0% | 1.13 | 4.5e-02 |
| `?` | ? | 4988 | 12.1% | 1.05 | 1.6e-01 |
| `aiin` | L | 3646 | 10.6% | 0.89 | 9.9e-01 |
| `ain` | L | 1626 | 9.9% | 0.82 | 9.9e-01 |
| `ar` | L | 2405 | 7.9% | 0.63 | 1.0e+00 |
| `edy` | C | 2837 | 6.3% | 0.48 | 1.0e+00 |
| `or` | L | 2047 | 5.8% | 0.45 | 1.0e+00 |
| `ol` | P | 3282 | 5.7% | 0.43 | 1.0e+00 |
| `ey` | C | 1957 | 5.5% | 0.42 | 1.0e+00 |
| `eedy` | C | 1184 | 4.6% | 0.36 | 1.0e+00 |
| `eey` | C | 1741 | 3.2% | 0.24 | 1.0e+00 |

## 2–3. C→L→P→R cycle against lower-order nulls

Observed: 0.2216 of known-state adjacent pairs follow the cycle; 0.0012 of 4-token windows run a full cycle step.

| null | n | pair-score mean | pair p | 4-window mean | 4-window p |
|---|---:|---:|---:|---:|---:|
| within_line_shuffle | 5000 | 0.2146 | 0.002 (PASS) | 0.00157 | 0.885 (FAIL) |
| markov1_twins | 1000 | 0.2188 | 0.126 (FAIL) | 0.00151 | 0.853 (FAIL) |
| markov2_twins | 1000 | 0.2209 | 0.398 (FAIL) | 0.00145 | 0.787 (FAIL) |

A Markov-1 twin reproduces the bigram table by construction, so the pair score cannot beat it; the 4-window score is the one that could show structure beyond adjacent pairs.

## 3b. State-order tournament

| split | tokens | CLPR rank (linear, of 24) | CLPR rank (cyclic, of 6) | top linear orders |
|---|---:|---:|---:|---|
| full_corpus | 35,038 | 1 | 1 | CLPR (5101), LPCR (5046), RCLP (4931) |
| folio_half_A | 16,819 | 1 | 1 | CLPR (2429), LPCR (2382), RCLP (2352) |
| folio_half_B | 18,219 | 1 | 1 | CLPR (2672), LPCR (2664), RLPC (2603) |
| currier_A | 11,362 | 5 | 3 | CPLR (1556), RLPC (1543), LPCR (1542) |
| currier_B | 23,676 | 2 | 2 | PCLR (3840), CLPR (3681), RPCL (3652) |
| untouched_folios | 33,272 | 1 | 1 | CLPR (4845), LPCR (4805), RCLP (4681) |

## 4. Predictive-state test (train on one folio half, test on the other)

- Majority baseline accuracy 28.3%; state-conditioned accuracy 31.7%.
- Information gain 0.0173 bits/token (2.076 → 2.058).
- Information gain measures how much the current state tells you about the next one. It is a property of the state labels, not of the C->L->P->R order.

## 5. Affix-role tournament

- Parser consistency check: 0 mismatches.
- Observed best cycle score 0.2216 (best cycle CLPR); shuffled groupings mean 0.2394 ± 0.0069; p = 0.987 → **FAIL**
- Endings stay fixed; which ending belongs to which state is shuffled (group sizes preserved), and each shuffle gets its best of the 6 cycles.

## 6. Semantic permutation tournament

- 14 glossed tokens, 3,113 occurrences.
- Published glosses place 28.1% of occurrences in the expected section; shuffled glosses 26.8% ± 7.0%; p = 0.411 → **FAIL**
- Pre-registered domain → section map: `{"Botanical": ["Herbal"], "Humoral": ["Herbal"], "Astronomical": ["Astronomical/Zodiac", "Cosmological"], "Solvent": ["Biological"], "Compounding": ["Pharmaceutical", "Stars/Recipes"]}`
- Glosses are shuffled among the glossed tokens. Only section preference is tested; operational glosses (heat, drain, ...) have no independent target in the manuscript yet and cannot be scored.

## 7. Holdout hygiene

- Declared holdout folios: f70v2, f71r, f72r1, f72v1, f72v2
- Also listed as already-used (SEEN_FOLIOS): f70v2, f71r, f72r1, f72v1, f72v2 → **CONTAMINATED**
- On untouched folios, 2,924 of 33,272 tokens (8.8%) are exact dictionary entries.
