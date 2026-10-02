# Longer repeated phrases (refrains)

Pre-registration: `analyses/refrains_prereg.md`. Paragraph text, 1,000 within-line shuffles, seed 20261002.
Sequences of a single repeated word are excluded.

| Text | Test | Repeated sequences | Shuffled mean | p | Result |
|---|---|---:|---:|---:|---|
| Currier A | L1: 3 words, 3+ times | 0 | 0.2 | 1 | FAIL |
| Currier A | L2: 4 words, 2+ times | 0 | 0.1 | 1 | FAIL |
| Currier B | L1: 3 words, 3+ times | 12 | 0.6 | 0.000999 | PASS |
| Currier B | L2: 4 words, 2+ times | 1 | 0.2 | 0.162 | FAIL |

**Verdict: PARTLY SUPPORTED.**

**Currier A, 3-word repeats:** none
Where they occur (share of repeats vs share of text): Herbal 0% vs 72%, Pharmaceutical 0% vs 28%

**Currier A, 4-word repeats:** none
Where they occur (share of repeats vs share of text): Herbal 0% vs 72%, Pharmaceutical 0% vs 28%

**Currier B, 3-word repeats:** ol s aiin (5); ol shedy qokedy (5); or or aiin (4); chey qol chedy (4); s aiin chey (4); shey qokain chedy (3); ol chedy qol (3); shedy qokedy qokeedy (3)
Where they occur (share of repeats vs share of text): Stars/Recipes 28% vs 46%, Biological 56% vs 29%, Herbal 5% vs 14%, Cosmological 9% vs 7%, Pharmaceutical 2% vs 2%, Astronomical/Zodiac 0% vs 2%

**Currier B, 4-word repeats:** ol shedy qokedy qokeedy (2)
Where they occur (share of repeats vs share of text): Stars/Recipes 0% vs 46%, Biological 100% vs 29%, Herbal 0% vs 14%, Cosmological 0% vs 7%, Pharmaceutical 0% vs 2%, Astronomical/Zodiac 0% vs 2%

## Reading the result

- **Dialect B has repeated 3-word formulas** (12 vs 0.6 expected), and they cluster on the **bath (Biological)
  pages**: 56% of repeats on 29% of the text. Examples: "ol shedy qokedy", "chey qol chedy", "ol s aiin".
- **No long refrains.** Only one 4-word sequence repeats ("ol shedy qokedy qokeedy", twice, both on bath pages),
  which is within chance. Prayers and litanies usually repeat long lines word for word, and that is not seen here.
- **Dialect A** (herbal and pharmacy) has no repeated 3- or 4-word sequences at all.
- The bath pages are the most formulaic part of the book, written in short repeated phrases. That fits instructions,
  recipes or short charms better than long prayers. It cannot tell a ritual purpose from a practical one.
