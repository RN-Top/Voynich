# Pre-registration: star-name crib and sound-shape comparison with other languages

Committed 2026-10-03, **before** either part is run. Amend only below the line at the end.

## Sound shape

Each word is turned into a consonant/vowel pattern (e.g. *daiin* → C V C C C in S2 units, if i is a consonant).
- **Voynich:** S2 units (ch, sh, cth, ckh, cph, cfh as single symbols, `analyses/freqmatch_test.units`). Vowels =
  **a, e, o, y**, the vowel-like symbols found by Sukhotin in every S2 run (`output/vowels_report.md`). Everything
  else is a consonant.
- **Other languages:** letters whose base form (accents removed) is a, e, i, o, u or y are vowels, and all other
  letters are consonants. Greek is transliterated by vowel class (α ε η ι ο υ ω are vowels).

## Part A: star-name crib (test)

**Star names, fixed before looking:** the common names of medieval astrolabe rete stars, in Latinized Arabic
spellings:
aldebaran, algol, alhabor, algomeisa, alhaioth, rigel, bedalgeuze, alramech, wega, altair, deneb, alferaz, markab,
scheat, alpheta, rasalhague, fomalhaut, menkar, calbalazet, azimech, calbalacrab, algorab, benenaz, mirach,
alioth, dubhe, denebalgedi, athoraye, alnath, alhena, alchameluz, enif.

**Labels:** every word of the star-label loci (Ls). **Statistic:** number of star names whose consonant/vowel pattern
exactly equals that of at least one star-label word. **Null:** the same number of words drawn at random from all
other labels (10,000 draws, seed 20261003). Pass: p < 0.01. The matching pairs are listed (a pattern match is not a
reading).

## Part B: closest languages by sound shape (descriptive)

Profile = token-weighted frequency of consonant/vowel patterns (patterns longer than 10 are pooled).
- Voynich A and B: paragraph tokens.
- Latin: the three CLTK texts (tokens).
- Modern languages: `wordfreq` top 20,000 words, weighted by frequency (Latin-script languages plus Greek).

Distance = Jensen–Shannon divergence between profiles. Report the languages ranked by closeness to Voynich A and
to Voynich B, and the Voynich's distance to its own shuffled-letter version as a reference. Caveats: modern spelling,
spelling conventions, and Arabic and Hebrew excluded because their scripts omit vowels.

---
Amendments (dated, below this line only):

**2026-10-03, results.** Part A: 10 vs 9.3, p = 0.45, **not supported**. Part B (descriptive): nearest languages
are French/English/Catalan/Turkish (A) and English/Latvian/Turkish (B). All are at or beyond the Voynich's distance
to its own shuffled copy, so **no close language**. Write-up: `output/sound_shapes_report.md`.
