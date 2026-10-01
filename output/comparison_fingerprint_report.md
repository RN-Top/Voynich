# Comparison fingerprint (exploratory)

Same generic measurements for every text: lowercase letters, words, ending = last 2 letters. Only `voynich_native` keeps real manuscript lines; every other text is set into lines whose widths are sampled from the Voynich paragraph lines.

| Measurement | `voynich_native` | `voynich_reflowed` | `voynich_shuffled` | `latin_apicius_recipes` | `latin_albertanus_13c` | `latin_bede_8c` | `cipher_apicius_recipes` |
|---|---:|---:|---:|---:|---:|---:|---:|
| Tokens | 35,000 | 35,000 | 35,000 | 7,733 | 35,000 | 35,000 | 7,733 |
| Mean word length | 4.96 | 4.96 | 4.96 | 5.68 | 5.73 | 6.08 | 11.83 |
| Distinct words / tokens (first 30k) | 0.207 | 0.207 | 0.210 | 0.243 | 0.269 | 0.323 | 0.243 |
| Character entropy h1 (bits) | 3.87 | 3.87 | 3.87 | 3.96 | 3.95 | 3.98 | 3.91 |
| Conditional character entropy h2 (bits) | 2.11 | 2.11 | 2.11 | 3.20 | 3.31 | 3.36 | 2.39 |
| Same word twice in a row | 0.84% | 0.84% | 0.37% | 0.21% | 0.07% | 0.01% | 0.21% |
| Stem → ending information (bits/word) | 1.354 | 1.354 | 1.326 | 3.516 | 3.702 | 3.618 | 3.348 |
| Strongest line-final ending: odds ratio | 22.9 | 1.8 | 2.2 | 2.8 | 2.1 | 1.7 | 1.7 |
| Strongest line-final ending | `-am` | `-ld` | `-d` | `-re` | `-ie` | `-ca` | `-qq` |

Caveats: h1/h2 depend on the alphabet (EVA vs Latin letters), so compare their *pattern*, not exact values. A self-citation (Timm & Schinner) comparison is not included: a faithful implementation of the published algorithm is still needed. Line-end measures for re-lined texts show only what line filling alone produces; a fair comparison of real line-end behaviour needs diplomatic transcriptions of medieval manuscripts that keep the original line breaks.
