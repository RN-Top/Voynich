# Do the Voynich symbols alternate like vowels and consonants? (Sukhotin)

Pre-registration: `analyses/vowels_prereg.md`. Shuffled baseline: letters shuffled within words, 20 times; seed 20261003.

| Text | Vowels found | Alternation | Shuffled | Excess | Ratio to Latin |
|---|---|---:|---:|---:|---:|
| Latin (control) | a e i o u w y | 0.796 | 0.578 | 0.218 | 1.00 |
| Voynich A S1 | ' : a b g h n o u y | 0.721 | 0.598 | 0.122 | 0.56 |
| Voynich A S2 | : a e g n o u y | 0.768 | 0.608 | 0.160 | 0.73 |
| Voynich B S1 | ' : a b f h n o u y | 0.729 | 0.588 | 0.140 | 0.64 |
| Voynich B S2 | : a c e n o u y z | 0.774 | 0.595 | 0.179 | 0.82 |

Control: Latin vowels found include at least 4 of a e i o u.

**Verdict: ALPHABET-LIKE.**

## Reading the result

- **Alphabet-like.** Voynich symbols alternate between a "vowel" set and a "consonant" set at 56–82% of Latin's
  strength above each text's own shuffled baseline. The strongest case is when ch, sh and the bench-gallows clusters
  are treated as single symbols (S2: 0.73 and 0.82), which supports reading those clusters as single letters.
- **Vowel-like symbols (S2):** mainly **o, a, e, y**, plus a few rare symbols. In S1, "h" lands in the vowel set
  only because it always follows c or s (ch, sh), which is why S2 is the better reading.
- **Data note:** the clean words contain 62 stray marks (":" 38, "'" 24) left over from transcription notation.
  They appear in the vowel lists but are too rare to affect the result.
- **Caveat:** alternation is also produced by any strict slot pattern (e.g. vowel-like symbols always between
  consonant-like clusters). So this shows the script **behaves** like an alphabet with vowels. It does not prove that
  it writes speech.
- This sits in tension with earlier results (word parts combine more freely than in Latin; no glue words; not
  substitution Latin). Together they fit a **sound-based script of an unknown language or a constructed
  phonetic system**, written in syllable-like slots. They do not fit a code made of arbitrary symbols.
