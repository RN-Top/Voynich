# Retracted: the "alchemical recipe" reading (17 November 2026)

Everything in this folder was added on 17 November 2026 under the claim that the Voynich is "a medieval alchemical
pharmaceutical recipe collection written in abbreviated Latin with monoalphabetic substitution." That claim is
withdrawn. The files are kept, not deleted, so the reasoning and its mistakes stay visible.

## Why it was withdrawn

1. **The "@-number measurement codes" are not in the manuscript.** Strings such as `@130;` or `@254;` are how the
   ZL3b transliteration writes a rare glyph that has no EVA letter. The file says so itself
   (`Data/Zl3b-n.txt`, line 21: *"a thick non-Voynich symbol resembling an underlined 29 (commented as @254; )"*).
   They are all above 100 because they are character code numbers, not dosages or batch numbers. The "43 batch
   identifiers" in `step2_measurement_codes.py` are therefore transcription markup.
2. **The cipher-type result contradicted itself.** The index of coincidence, 0.0813, was reported as falling "exactly
   in" the monoalphabetic range 0.065–0.080. It is above that range, and the same run also suggested a
   polyalphabetic component.
3. **The recognition model did not support it.** `build_recognition_model.py` found no difference between the
   Voynich and the shuffled control (its own verdict: "hypothesis NOT supported").
4. **The cipher solvers produced no readable text.** `crack_cipher*.py` mapped some letters but decoded no passage.
   The one Latin word reported, *aqua*, came from a known-plaintext search seeded with Latin words such as *aqua*.
5. **The word meanings were never tested.** Glosses such as *dar = take* or *ol = oil* were assigned, not checked on
   pages they were not built from.
6. **A properly controlled test now rules out simple substitution.** The pre-registered Fontana-method decoder
   (`analyses/fontana_cipher_prereg.md`, report `output/fontana_cipher_report.md`) tried 36 substitution variants
   (one or several signs per letter; forwards, reversed or mirrored; Latin, Italian, Venetian). Its solver recovers
   real Latin and Italian enciphered the same way at 94–100%, but no variant decodes the Voynich. The Voynich is
   more predictable letter-to-letter than Latin or Italian, which a letter swap cannot produce.

## Results from this batch that still stand

- `build_recognition_model.py`: Voynich and shuffled control did not differ on vowel ratio or character diversity.
- `definitive_cipher_test.py`: the earlier `fontana_cipher_mapping.json` key produced 0% matches. That key has no
  documented source, so this says nothing about Fontana's real cipher; the pre-registered decoder covers that.

## What replaced it

See the top-level [README](../README.md) and [VALIDATION.md](../VALIDATION.md). For reviewers, start at
[FOR_REVIEWERS.md](../FOR_REVIEWERS.md).
