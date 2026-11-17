# Pre-registration: does any of Fontana's cipher methods turn the Voynich into Latin or Italian?

Written and committed before `analyses/fontana_cipher_decoder.py` was first run. Nothing here may be
changed after the first run. Any later change is recorded in the report as a deviation.

## Question

Giovanni Fontana (Padua/Venice, c. 1395–1455) enciphered parts of his *Bellicorum instrumentorum liber*
(BSB Cod.icon. 242) and other works. The scholarship (Battisti & Saccaro Battisti, *Le macchine cifrate di
Giovanni Fontana*, 1984; summaries on ciphermysteries.com) describes the cipher as a **substitution with an
invented alphabet**: Latin plaintext, each letter written as a made-up sign. Sources disagree on whether it is
strictly one sign per letter (monoalphabetic) or sometimes several signs per letter (homophonic). Reversed
(mirror) writing is a common technique of the period and was suggested for this project, but we could not
confirm it in the Fontana scholarship, so it is tested as a reasonable variant, not as a documented one.

The repository's earlier `fontana_cipher_mapping.json` (circles with direction marks) has no documented source
for its sign forms, so it is not used as a key. Instead the key is left unknown and solved for, which covers
**every** possible invented alphabet of each type.

## Methods tested (all combinations)

| Factor | Levels |
|---|---|
| Voynich sign inventory | (a) EVA letters; (b) EVA letter groups as single signs: cth ckh cph cfh ch sh iiin iin in ii eee ee |
| Writing direction | (1) forwards; (2) letters of each word reversed; (3) whole line mirrored |
| Key type | (M) monoalphabetic: one sign per letter; (H) homophonic: several signs may share a letter |
| Plaintext language | Latin; Italian (Dante + Matteo Villani, Tuscan); Venetian (19th-c. *Rime veneziane*, a dialect proxy) |

2 × 3 × 2 × 3 = **36 runs**. Each run: hill-climbing solver, 6 random restarts, 6,000 steps each, maximizing a
character trigram model (with word spaces) of the language. Signs used fewer than 20 times are dropped together
with their words. Seed 1453.

## Train / test split

Voynich paragraph text from `voynich_integrated.json`. Folios are split at random (seed 1453) into a
**training half**, on which the key is solved, and a **test half**, on which it is scored. All numbers below are
from the test half, so a key cannot score well just by being fitted to the same text.

## Controls (set before running)

- **Positive control (should pass):** held-out Latin (Albertanus of Brescia) and held-out Italian (last 20% of
  Villani), never seen by the language models, enciphered with a random key of the same type (M: random
  one-to-one; H: the 6 commonest letters each split into 2 signs), cut to the same training size as the Voynich,
  and solved with the identical solver. 3 random keys per type and language.
- **Random baseline (should fail):** the Voynich training and test text with its signs shuffled at random
  across the whole text (keeps sign frequencies and word lengths, destroys order), solved identically.
  5 shuffles per run setting, using the inventory (a), forwards, for each key type and language.

## Measures (on the test half)

1. **Fit, bits per letter:** cross-entropy of the decoded test text under the language model. Lower is better.
2. **Real-word rate:** share of decoded test words of 3+ letters that occur in the language's reference
   vocabulary (all words from the model and control texts).
3. **Star-name check:** the 14 plant-page opening words and the star labels they share chunks with
   (`output/plant_star_report_integrated.md` on the backwards-reading-test branch) are decoded. Count how many
   of these 22 distinct words land within one letter edit of a star or plant name of 5+ letters in
   `Data/fontana_reference/name_lexicon.txt`.

## Pass rules (per run)

- **R1 (fit):** test bits/letter lower than *every* random-baseline run for that key type and language, **and**
  no more than halfway from the positive-control mean to the baseline mean.
- **R2 (words):** real-word rate above *every* random-baseline run, **and** at least half the positive-control
  mean.
- **R3 (star names):** star-name hits greater than the 95th percentile of the same count under 1,000 random keys
  of the same type.

A method **decodes** the Voynich only if R1 and R2 both pass. R3 is a supporting check and cannot pass a method
on its own. The positive controls must pass R1 and R2 against the baseline, otherwise the test is reported as
unable to decide.

## What a failure means

A failure rules out *simple* versions of Fontana's methods (invented-alphabet substitution, with or without
homophones and reversed writing) applied to Latin or Italian with these sign inventories. It does not rule out
Fontana as the author, nor a cipher with abbreviations, nulls, a code-book, or a language not tested here.
