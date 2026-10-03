# Glue words and content words

Pre-registration: `analyses/glue_words_prereg.md`. Currier B paragraph text; 132 words with 30+ uses; 10,000 shuffles within frequency bands, seed 20261003.

- Spearman correlation, length vs unevenness: **-0.016** (shuffled within frequency bands: +0.045)
- p = 0.773 → **NOT SUPPORTED**

## Most even words (glue candidates)

| Word | Uses | Length | Unevenness | Main section |
|---|---:|---:|---:|---|
| y | 176 | 1 | 0.012 | Stars/Recipes |
| opchedy | 48 | 7 | 0.022 | Stars/Recipes |
| otedy | 140 | 5 | 0.030 | Stars/Recipes |
| saiin | 86 | 5 | 0.036 | Stars/Recipes |
| ykeey | 30 | 5 | 0.037 | Stars/Recipes |
| lor | 34 | 3 | 0.041 | Stars/Recipes |
| otal | 104 | 4 | 0.047 | Stars/Recipes |
| o | 81 | 1 | 0.048 | Stars/Recipes |
| chey | 249 | 4 | 0.049 | Stars/Recipes |
| ain | 100 | 3 | 0.051 | Stars/Recipes |
| okal | 98 | 4 | 0.052 | Stars/Recipes |
| sheol | 66 | 5 | 0.053 | Biological |
| daiin | 316 | 5 | 0.053 | Stars/Recipes |
| keedy | 62 | 5 | 0.059 | Stars/Recipes |
| okaiin | 170 | 6 | 0.061 | Stars/Recipes |
| sar | 53 | 3 | 0.061 | Biological |
| otey | 36 | 4 | 0.069 | Biological |
| cheol | 98 | 5 | 0.069 | Stars/Recipes |
| qotar | 62 | 5 | 0.069 | Stars/Recipes |
| sheey | 102 | 5 | 0.071 | Stars/Recipes |

## Most topic-bound words (content candidates)

| Word | Uses | Length | Unevenness | Main section |
|---|---:|---:|---:|---|
| ykaiin | 35 | 6 | 0.951 | Cosmological |
| sol | 45 | 3 | 0.814 | Biological |
| qol | 136 | 3 | 0.808 | Biological |
| olkain | 34 | 6 | 0.808 | Biological |
| cheky | 46 | 5 | 0.654 | Herbal |
| chor | 31 | 4 | 0.595 | Stars/Recipes |
| sheody | 30 | 6 | 0.540 | Stars/Recipes |
| cheo | 43 | 4 | 0.536 | Stars/Recipes |
| chody | 44 | 5 | 0.521 | Stars/Recipes |
| dy | 121 | 2 | 0.493 | Biological |
| lkeey | 38 | 5 | 0.462 | Stars/Recipes |
| cheody | 54 | 6 | 0.447 | Stars/Recipes |
| dol | 43 | 3 | 0.444 | Biological |
| oly | 49 | 3 | 0.437 | Biological |
| dam | 42 | 3 | 0.426 | Herbal |
| am | 59 | 2 | 0.414 | Stars/Recipes |
| olchedy | 35 | 7 | 0.406 | Biological |
| dshedy | 32 | 6 | 0.405 | Biological |
| otam | 38 | 4 | 0.401 | Stars/Recipes |
| qokain | 275 | 6 | 0.374 | Biological |

## Reading the result

- **No glue/content split by length.** Among words of similar frequency, short words are no more evenly spread
  across sections than long ones (ρ = −0.02 against +0.05 shuffled; p = 0.77).
- Some of the most topic-bound words are among the shortest (*sol, qol, dy, am, dam, oly*), and some of the most
  even are long (*opchedy, okaiin*). In natural languages the short, frequent words are mostly topic-neutral.
- This is one more way the text differs from an ordinary language written in a new alphabet. It fits a system where
  short words are not grammar particles. They might be abbreviations, codes or names, or "words" might not
  correspond to spoken words one-to-one.
- The lists above are still useful: the even words (*y, otedy, saiin, otal, chey, daiin, okaiin…*) behave like
  general-purpose items, and the uneven ones (*qol, sol, olkain, ykaiin, cheky…*) like topic-specific ones.
