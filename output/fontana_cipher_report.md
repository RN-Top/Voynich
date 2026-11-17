# Fontana cipher decoder: results

Pre-registration: `analyses/fontana_cipher_prereg.md`. Code: `analyses/fontana_cipher_decoder.py` (seed 1453). Full numbers: `output/fontana_cipher_results.json`.

## Answer

**None of the 36 Fontana-method runs decodes the Voynich.** No invented-alphabet substitution (one sign per letter or several), forwards or reversed, with either sign inventory, makes the text read as Latin, Italian or Venetian. The best keys do beat shuffled Voynich text, but they reach only 4-34% real words (mostly short, repeated ones like *sit*, *et*, *del*), while real Latin and Italian put through the same cipher and solver come back at 94-100% real words, almost letter-perfect.

The test itself works: 12 of 12 positive controls (real Latin or Italian, enciphered with a random key and solved by the same program) pass. Mean letters recovered: latin mono 100%, latin homophonic 100%, italian mono 100%, italian homophonic 99%.

## Controls

| Text | Key type | Language | Test bits/letter (lower = more language-like) | Real-word rate |
|---|---|---|---:|---:|
| Real text, enciphered then solved (positive) | mono | latin | 2.906 | 100.0% |
| Shuffled Voynich (random baseline) | mono | latin | 4.829 (best 4.820) | 1.3% (best 1.3%) |
| Real text, enciphered then solved (positive) | homophonic | latin | 2.906 | 98.2% |
| Shuffled Voynich (random baseline) | homophonic | latin | 3.358 (best 3.355) | 30.3% (best 30.4%) |
| Real text, enciphered then solved (positive) | mono | italian | 2.764 | 100.0% |
| Shuffled Voynich (random baseline) | mono | italian | 4.973 (best 4.967) | 1.8% (best 2.0%) |
| Real text, enciphered then solved (positive) | homophonic | italian | 2.801 | 94.2% |
| Shuffled Voynich (random baseline) | homophonic | italian | 3.215 (best 3.213) | 10.4% (best 10.4%) |
| Shuffled Voynich (random baseline) | mono | venetian | 5.058 (best 5.048) | 0.6% (best 0.6%) |
| Shuffled Voynich (random baseline) | homophonic | venetian | 4.187 (best 4.182) | 2.9% (best 3.2%) |

## All 36 runs

| Signs | Direction | Key | Language | Bits/letter | Real words | Star-name hits (random-key 95th pct) | R1 | R2 | R3 | Decodes? |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| letters | forwards | mono | latin | 3.475 | 7.5% | 0 (0) | pass | fail | fail | **no** |
| letters | forwards | mono | italian | 3.679 | 6.5% | 0 (0) | pass | fail | fail | **no** |
| letters | forwards | mono | venetian | 3.662 | 6.3% | 0 (0) | pass | fail | fail | **no** |
| letters | forwards | homophonic | latin | 3.035 | 15.1% | 0 (0) | pass | fail | fail | **no** |
| letters | forwards | homophonic | italian | 3.094 | 7.7% | 0 (0) | fail | fail | fail | **no** |
| letters | forwards | homophonic | venetian | 3.076 | 4.1% | 0 (0) | pass | fail | fail | **no** |
| letters | word-reversed | mono | latin | 3.581 | 5.2% | 0 (0) | pass | fail | fail | **no** |
| letters | word-reversed | mono | italian | 3.764 | 4.8% | 0 (0) | pass | fail | fail | **no** |
| letters | word-reversed | mono | venetian | 3.812 | 3.7% | 0 (0) | pass | fail | fail | **no** |
| letters | word-reversed | homophonic | latin | 3.087 | 22.8% | 0 (0) | pass | fail | fail | **no** |
| letters | word-reversed | homophonic | italian | 2.906 | 14.5% | 0 (0) | pass | fail | fail | **no** |
| letters | word-reversed | homophonic | venetian | 3.282 | 5.4% | 0 (0) | pass | fail | fail | **no** |
| letters | line-mirrored | mono | latin | 3.609 | 4.2% | 0 (0) | pass | fail | fail | **no** |
| letters | line-mirrored | mono | italian | 3.774 | 5.7% | 0 (0) | pass | fail | fail | **no** |
| letters | line-mirrored | mono | venetian | 3.731 | 1.6% | 0 (0) | pass | fail | fail | **no** |
| letters | line-mirrored | homophonic | latin | 3.050 | 21.8% | 0 (0) | pass | fail | fail | **no** |
| letters | line-mirrored | homophonic | italian | 3.132 | 15.6% | 0 (0) | fail | fail | fail | **no** |
| letters | line-mirrored | homophonic | venetian | 3.250 | 2.7% | 0 (0) | pass | fail | fail | **no** |
| groups | forwards | mono | latin | 3.260 | 12.9% | 0 (0) | pass | fail | fail | **no** |
| groups | forwards | mono | italian | 3.463 | 16.2% | 0 (0) | pass | fail | fail | **no** |
| groups | forwards | mono | venetian | 3.329 | 11.5% | 0 (0) | pass | fail | fail | **no** |
| groups | forwards | homophonic | latin | 2.917 | 8.5% | 1 (0) | pass | fail | pass | **no** |
| groups | forwards | homophonic | italian | 3.035 | 20.7% | 0 (0) | fail | fail | fail | **no** |
| groups | forwards | homophonic | venetian | 3.035 | 20.2% | 0 (0) | pass | fail | fail | **no** |
| groups | word-reversed | mono | latin | 3.393 | 11.9% | 0 (0) | pass | fail | fail | **no** |
| groups | word-reversed | mono | italian | 3.369 | 24.7% | 0 (0) | pass | fail | fail | **no** |
| groups | word-reversed | mono | venetian | 3.584 | 10.4% | 0 (0) | pass | fail | fail | **no** |
| groups | word-reversed | homophonic | latin | 3.033 | 11.3% | 0 (0) | pass | fail | fail | **no** |
| groups | word-reversed | homophonic | italian | 3.103 | 12.2% | 0 (0) | fail | fail | fail | **no** |
| groups | word-reversed | homophonic | venetian | 3.107 | 17.8% | 0 (0) | pass | fail | fail | **no** |
| groups | line-mirrored | mono | latin | 3.353 | 10.0% | 0 (0) | pass | fail | fail | **no** |
| groups | line-mirrored | mono | italian | 3.359 | 24.6% | 1 (0) | pass | fail | pass | **no** |
| groups | line-mirrored | mono | venetian | 3.362 | 11.3% | 0 (0) | pass | fail | fail | **no** |
| groups | line-mirrored | homophonic | latin | 2.953 | 33.9% | 0 (0) | pass | fail | fail | **no** |
| groups | line-mirrored | homophonic | italian | 2.930 | 24.5% | 0 (0) | pass | fail | fail | **no** |
| groups | line-mirrored | homophonic | venetian | 3.174 | 6.9% | 0 (0) | pass | fail | fail | **no** |

## What the closest run reads like

Closest to its language: groups, forwards, homophonic, latin. First three test lines, decoded:

> rerete esuet ret eruet esuet retse

> retuete uret s pet re pre

> peret rae e uet ue ere uet


Most real words: groups, line-mirrored, homophonic, latin (34%). First two test lines:

> essis siste sisti sit siste editet

> ite et sis s sits esissit

Both read as repetitive syllables, not sentences. The low bits/letter of the Voynich runs come from this repetitiveness, which is why R1 passed in most runs and could not on its own tell a decoding from nonsense (a weakness of rule R1, noted here rather than changed after the fact).

**Star-name check:** 2 run(s) pass R3, each with a single hit: pochof → seuen ≈ *semen*; pochof → seeen ≈ *semen*. Random keys average almost zero hits, so one hit clears the 95th percentile (0), but one near-match in 20 words, in runs that otherwise read as nonsense, is best treated as coincidence. No run turns *koaiin*/*okoaly* or the other pairs into star or plant names.

Star-name check for the closest run (Voynich word → decoded → nearest name within one letter):

- koaiin → reet
- koary → reete
- tydlo → rerte
- koair → reest
- pocheody → seuaere
- pochaiin → seuet
- pydchdom → seruret
- pochof → seuen → **semen**
- tocphol → reret
- tdokchcfhy → rrerure
- toealchs → reaetus
- okoaly → ereete
- otydy → erere
- otydg → ererl
- opocphor → eseret
- oydchy → eerue
- otochedy → ereuare
- chocfhy → uere
- qotoear → pereaet
- otoeeo → ereae

## Why it fails: the Voynich is too predictable for a letter swap

A substitution only relabels signs, so it cannot change how predictable the next sign is. Measured as conditional entropy (bits of surprise per sign, given the previous sign):

| Text | bits |
|---|---:|
| voynich_letters | 2.09 |
| voynich_groups | 2.35 |
| latin | 3.30 |
| italian | 3.10 |

The Voynich is far more predictable than Latin or Italian, and a homophonic key (several signs for one letter) makes the decoded text even *more* predictable, not less. So a simple Fontana-style substitution of Latin or Italian cannot produce text like the Voynich. This agrees with the earlier comparison in VALIDATION.md (h2 2.11 vs 3.2–3.4).

## Limits

- The star-name check could only use 20 of the 24 words: c@132hsc@133hain, o@167chal, c@181hdai@133hy, o@167olchc@133hy contain rare @-signs with no stable reading. (The pre-registration said 22; the true count of distinct plain words is 20.)
- Venetian is represented by 19th-century dialect verse (8,500 words); no 15th-century Paduan or Venetian prose was available. Italian is Tuscan (Dante, Matteo Villani).
- Not tested: abbreviation systems, null signs, a code-book of whole words, a syllabic cipher, or languages other than Latin and Italian. Any of these could change the picture.
- Venetian has no positive control of its own (too little held-out text); it is judged against the Italian control.
- Not established here: whether Fontana's cipher was mono- or homophonic. Both were tested.
- This tests Fontana's *methods*, not Fontana as author. A failure does not rule him out.
