# Representation / transcription transfer

Frozen rules, different input text. Holdout folios are the pre-registered `data/blind_holdout_v1.json` list in every column.

| Result | `zl_canonical` | `zl_alternate` |
|---|---:|---:|
| Tokens | 38,958 | 36,218 |
| -m/-am share at line end | 70.3% | 71.5% |
| -m/-am line-end odds ratio | 20.7 | 20.3 |
| -m/-am within-line shuffle p | 0.0005 | 0.0005 |
| C→L→P→R vs shuffle p | 0.001 | 0.0015 |
| C→L→P→R vs Markov-1 p | 0.075 | 0.13 |
| C→L→P→R vs Markov-2 p | 0.37 | 0.41 |
| C→L→P→R rank (of 24) | 1 | 1 |
| Blind A: line-final AUC | 0.671 | 0.675 |
| Blind A: p | 0.0005 | 0.0005 |
| Blind B: layout AUC | 0.635 | 0.644 |
| Blind B: p | 0.0005 | 0.0005 |
| Blind C: section accuracy | 65.1% | 65.1% |
| Blind C: majority baseline | 65.1% | 65.1% |
| Blind D: stem → ending bits/token | 0.775 | 0.744 |
| Blind D: p | 0.001 | 0.001 |

`zl_alternate` uses the last alternative reading in `[a:b]` and does not split words at uncertain spaces. It tests sensitivity to ZL's editorial choices. It is not an independent transcription; add one with `--corpus`.
