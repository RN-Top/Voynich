# Blind holdout report

Holdout `blind_holdout_v1`: 43 folios drawn with seed 20261001 and committed 2026-10-01T04:14:24+00:00, before this scorer existed. The model is trained on the other 184 folios only. PASS means p < 0.01.

Only input: each token's ending class from the frozen parser rules. Every target is something that spelling does not determine.

| Target | Holdout size | Score | Chance / baseline | p | Verdict |
|---|---:|---:|---:|---:|---|
| A. Line-final token (15 endings) | 5,508 tokens | AUC 0.671 | 0.501 | 0.0005 | **PASS** |
| A. Line-final token (4 states C/L/P/R) | 5,508 tokens | AUC 0.581 | 0.501 | 0.0005 | **PASS** |
| B. Label / diagram vs paragraph | 6,059 tokens | AUC 0.635 | 0.500 | 0.0005 | **PASS** |
| C. Section of each folio | 43 folios | 65.1% correct | 65.1% (always 'Herbal'); shuffled 29.3% | 0.0005 | **FAIL (ties or trails the majority baseline)** |
| D. Stem predicts its ending | 5,593 tokens | 0.775 bits/token | 0 bits (stem ignored); shuffled stems -1.293 | 0.001 | **PASS** |

Information gain for line-final prediction: 0.0479 bits/token with 15 endings, 0.0337 with the 4-state grouping.

Target D was added on 2026-10-01 and committed before its first run on this holdout. Part of its signal is orthographic (letters next to the ending), so it shows consistent word-building, not meaning.

Rule note (added after the first run, and stricter only): section prediction must also beat the always-guess-the-majority-section baseline to pass. No scores changed.

AUC is the chance that a randomly chosen positive (e.g. a line-final token) gets a higher score than a randomly chosen negative. 0.5 is chance.

## Section predictions per holdout folio

| folio | true section | predicted |
|---|---|---|
| f102v1 | Pharmaceutical | Pharmaceutical |
| f104r | Stars/Recipes | Cosmological |
| f106v | Stars/Recipes | Cosmological |
| f10r | Herbal | Herbal |
| f11r | Herbal | Herbal |
| f13v | Herbal | Herbal |
| f15v | Herbal | Herbal |
| f1v | Herbal | Pharmaceutical |
| f20r | Herbal | Pharmaceutical |
| f20v | Herbal | Herbal |
| f22r | Herbal | Herbal |
| f23r | Herbal | Herbal |
| f25v | Herbal | Herbal |
| f26r | Herbal | Biological |
| f27v | Herbal | Astronomical/Zodiac |
| f28v | Herbal | Herbal |
| f29v | Herbal | Herbal |
| f2r | Herbal | Herbal |
| f35r | Herbal | Herbal |
| f36r | Herbal | Herbal |
| f38v | Herbal | Pharmaceutical |
| f40r | Herbal | Cosmological |
| f42v | Herbal | Herbal |
| f43v | Herbal | Cosmological |
| f44r | Herbal | Herbal |
| f50v | Herbal | Cosmological |
| f52r | Herbal | Astronomical/Zodiac |
| f54r | Herbal | Pharmaceutical |
| f57r | Herbal | Astronomical/Zodiac |
| f65v | Herbal | Astronomical/Zodiac |
| f67v1 | Astronomical/Zodiac | Astronomical/Zodiac |
| f68r3 | Astronomical/Zodiac | Astronomical/Zodiac |
| f69r | Astronomical/Zodiac | Astronomical/Zodiac |
| f70r2 | Astronomical/Zodiac | Astronomical/Zodiac |
| f75r | Biological | Biological |
| f80v | Biological | Biological |
| f85r2 | Cosmological | Cosmological |
| f86v6 | Cosmological | Cosmological |
| f89v1 | Pharmaceutical | Pharmaceutical |
| f8r | Herbal | Herbal |
| f93v | Pharmaceutical | Pharmaceutical |
| f95v1 | Pharmaceutical | Cosmological |
| f99v | Pharmaceutical | Pharmaceutical |
