# Repeated phrases and grammar links

Pre-registration: `analyses/phrases_prereg.md`. Paragraph text, interior pairs only, 1,000 within-line shuffles, seed 20261002.

## R1. Set phrases (pairs seen 5+ times and 3+ times more often than chance)

| Text | Pairs | Set phrases | Shuffled mean | p | Result |
|---|---:|---:|---:|---:|---|
| Currier A | 6,721 | 16 | 4.8 | 0.000999 | PASS |
| Currier B | 16,038 | 100 | 28.7 | 0.000999 | PASS |

## R2. Grammar links (which parts of neighbouring words depend on each other)

| Text | Link | MI (bits) | Shuffled | Excess | p |
|---|---|---:|---:|---:|---:|
| Currier A | ending of word 1 → beginning of word 2 | 0.5297 | 0.3742 | 0.1555 | 0.000999 |
| Currier A | beginning of word 1 → beginning of word 2 | 0.5448 | 0.4696 | 0.0752 | 0.000999 |
| Currier A | ending of word 1 → ending of word 2 | 0.3694 | 0.3386 | 0.0308 | 0.000999 |
| Currier A | beginning of word 1 → ending of word 2 | 0.3904 | 0.3747 | 0.0157 | 0.022 |
| Currier B | ending of word 1 → beginning of word 2 | 0.4879 | 0.2006 | 0.2873 | 0.000999 |
| Currier B | beginning of word 1 → beginning of word 2 | 0.3989 | 0.2713 | 0.1277 | 0.000999 |
| Currier B | ending of word 1 → ending of word 2 | 0.2092 | 0.1574 | 0.0518 | 0.000999 |
| Currier B | beginning of word 1 → ending of word 2 | 0.2129 | 0.2006 | 0.0122 | 0.000999 |

## Top set phrases, Currier A (descriptive)

| Phrase | Count | Times expected | Main sections |
|---|---:|---:|---|
| chol chol | 21 | 3.3 | Herbal 18, Pharmaceutical 3 |
| s aiin | 19 | 15.0 | Pharmaceutical 13, Herbal 6 |
| or aiin | 8 | 12.6 | Pharmaceutical 5, Herbal 3 |
| chol shol | 8 | 3.1 | Herbal 8 |
| s or | 7 | 5.3 | Herbal 4, Pharmaceutical 3 |
| o l | 7 | 40.1 | Herbal 4, Pharmaceutical 3 |
| daiin cthol | 6 | 4.3 | Herbal 5, Pharmaceutical 1 |
| d aiin | 6 | 29.6 | Herbal 6 |
| chol cthol | 6 | 4.7 | Herbal 5, Pharmaceutical 1 |
| chol dol | 6 | 3.8 | Herbal 4, Pharmaceutical 2 |
| qokol daiin | 6 | 3.7 | Herbal 4, Pharmaceutical 2 |
| shol shol | 5 | 4.8 | Herbal 4, Pharmaceutical 1 |

Most frequent three-word sequences: chol chol kor (2); dar shey cthar (2); chol daiin cthy (2); chol chy chaiin (2); cho s chol (2); chy daiin cthol (2); chol chol chol (2); cthor chol chor (2)

## Top set phrases, Currier B (descriptive)

| Phrase | Count | Times expected | Main sections |
|---|---:|---:|---|
| or aiin | 40 | 10.1 | Stars/Recipes 13, Cosmological 12 |
| s aiin | 31 | 20.1 | Herbal 12, Stars/Recipes 9 |
| ol shedy | 22 | 3.4 | Biological 18, Stars/Recipes 4 |
| ar aiin | 21 | 5.2 | Stars/Recipes 11, Cosmological 6 |
| chedy qokeey | 19 | 4.0 | Stars/Recipes 15, Biological 4 |
| shedy qokedy | 19 | 3.9 | Biological 17, Herbal 1 |
| r aiin | 19 | 14.4 | Stars/Recipes 13, Biological 4 |
| chedy qokain | 18 | 3.5 | Biological 15, Stars/Recipes 3 |
| shedy qokaiin | 16 | 3.9 | Biological 10, Stars/Recipes 4 |
| shey qokain | 16 | 6.6 | Biological 8, Stars/Recipes 8 |
| qokedy qokedy | 15 | 5.0 | Biological 12, Stars/Recipes 2 |
| qokeedy qokeedy | 15 | 4.4 | Stars/Recipes 9, Biological 6 |

Most frequent three-word sequences: ol s aiin (5); ol shedy qokedy (5); or or aiin (4); chey qol chedy (4); s aiin chey (4); qokedy qokedy qokedy (3); shey qokain chedy (3); ol chedy qol (3)

## Extra check (added after the run, not pre-registered)

Several top phrases are a short piece plus `aiin` ("s aiin", "or aiin"). These could be single words that the
transcription marks with an *uncertain* space, which the parser splits. Rerun with uncertain spaces **not** split
(300 shuffles): R1 still passes (A: 11 vs 3.6; B: 71 vs 21.8; p = 0.003, the floor). R2 keeps the same order,
with ending → beginning strongest in both A and B. "or aiin" and "s aiin" remain set phrases.

## What this means for decoding

- **The text has set phrases**: about 3x more strongly bound word pairs than shuffled text, most of all in
  Currier B (bath and recipe pages: "shedy qokedy", "chedy qokeey", "ol shedy").
- **The strongest grammar link runs from a word's ending to the next word's beginning.** The ending of one
  word predicts how the next word starts, for example -dy followed by qok-. That fits endings being grammar
  that "chooses" what follows, or a writing habit at word joins. It is the clearest grammar-like rule found so far.
- **The beginnings of neighbouring words also go together** (second strongest). This could be topic
  (words about the same thing sit together) or a repeating pattern.
