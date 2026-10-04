# Pre-registration: Do Voynich closing words match O'Hickey medical vocabulary from the Book of Fermoy?

Date: 2026-10-04. Written before Fermoy vocabulary is extracted.

## Idea

The Voynich contains 44 words that appear at paragraph ends significantly more often than chance (closing vocabulary). If the Voynich was written by or derived from O'Hickey family knowledge, these closing words might share phonetic or morphological patterns with medical terminology from **MS 23 E 29 (The Book of Fermoy)**, an Irish medical treatise written by Donnchadh óg Ó hÍceadha in 1469.

## Data

- **Voynich closing words:** 44 words with p < 0.05 in recipe closing analysis (from `output/recipe_closing_report.md`).
- **Fermoy vocabulary:** Medical terms extracted from MS 23 E 29 transcription, organized by category (symptoms, cures, herbs, methods).

## Statistic

For each Voynich closing word:
1. **Levenshtein distance** to each Fermoy medical term. Count matches where distance ≤ 3 (allowing for spelling variation).
2. **Phonetic similarity:** check if the word shares root consonants or vowel patterns with known Irish medical terms or Latin medical vocabulary O'Hickey would have used.
3. **Substring overlap:** any Voynich closing word that contains a Fermoy term as a substring (or vice versa).

## Prediction

If Voynich was influenced by O'Hickey tradition:
- At least **8–12 Voynich closing words** will have Levenshtein distance ≤ 3 to Fermoy medical terms.
- At least **5–8 words** will show phonetic similarity (shared roots with Irish or Latin medical vocabulary).
- The match rate will be **significantly higher than a shuffled control** (random Fermoy terms matched to random Voynich words).

## Threshold

- **Levenshtein matches:** p < 0.05 in binomial test (observed matches vs. null hypothesis of random matching).
- **Phonetic matches:** expert judgment (will be reported descriptively).
- **Overall:** if ≥8 Levenshtein matches and ≥5 phonetic matches, hypothesis **supported**. Otherwise, **not supported**.

## Null hypothesis

Voynich closing words and Fermoy medical vocabulary are unrelated. Matches will occur at random chance rate (~5% at Levenshtein ≤ 3).

## Controls

1. Shuffle Fermoy vocabulary and retest—matches should drop to ~0.
2. Shuffle Voynich words and test against real Fermoy—matches should drop to ~random.
