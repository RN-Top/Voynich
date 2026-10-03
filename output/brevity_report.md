# Do frequent words get shorter? (Zipf's law of abbreviation)

Pre-registration: `analyses/brevity_prereg.md`. Equal samples of N = 7,733 tokens; seed 20261003.

| Text | Types (5+ uses) | Strength −ρ (full sample) | Half-sample interval |
|---|---:|---:|---|
| Voynich A | 266 | 0.220 | 0.198–0.339 |
| Voynich B | 272 | 0.109 | 0.062–0.198 |
| latin_apicius_recipes | 287 | 0.179 | 0.071–0.214 |
| latin_albertanus_13c | 226 | 0.302 | 0.311–0.455 |
| latin_bede_8c | 219 | 0.409 | 0.366–0.503 |
| cipher of Apicius | 288 | 0.173 | 0.091–0.224 |

**Verdict: MIXED.**

## Reading the result

- **Mixed.** Voynich B shows the weakest brevity law of all six texts (0.109), which is notation-like. Voynich A
  (0.220) sits inside the Latin range, above the Latin recipe book (0.179).
- **Genre matters.** The Latin recipe text (Apicius) and its cipher are also weak (0.17–0.18), while prose (Bede,
  Albertanus) is strong (0.30–0.41). Recipe-like, list-like text weakens the law in Latin too, so a weak law in
  Voynich B does not by itself separate "notation" from "recipe-style language".
- Together with the slot test (also mixed), the evidence leans toward freer, more notation-like word-building,
  most of all in Currier B. Neither test decides it.
