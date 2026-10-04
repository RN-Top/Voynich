# Validation status

See also [REPLICATION.md](REPLICATION.md) for how an independent group can reproduce every number.

**Update:** code for the hypotheses that were not supported has been moved to [`archive/`](archive/README.md),
and the app now presents only the supported structural results. The tests and their outcomes remain
recorded here.

This file records what currently survives independent testing and what does not.
It follows the independent nine-step review by Juan Gabriel Molina (September 2026)
and a re-run of the key tests on the full corpus with `structural_validation.py`.

Reproduce everything below with:

```bash
pip install -r requirements.txt
python structural_validation.py            # ~15 s; writes output/structural_validation_report.md
```

The full, regenerated numbers are in [`output/structural_validation_report.md`](output/structural_validation_report.md).
The run is seeded, and every figure is computed from `data/ZL3b-n.txt`. Nothing is hard-coded.

## Summary

| Claim | Status | Evidence |
|---|---|---|
| -m / -am tokens prefer physical line ends | **Supported** | 605 of 861 paragraph-text -m/-am tokens are line-final (OR ≈ 20.7). Within-line shuffle p ≈ 5e-5 (20,000 perms). The reviewer's independent sample agrees (OR ≈ 3.4, p ≈ 5e-5). |
| Other endings have positional preferences too | **Supported (new)** | -y and -dy lean line-final (OR ≈ 1.8). -eey, -eedy, -ey, -ol, -or and -edy lean mid-line (OR 0.24–0.48). |
| C→L→P→R order beats a within-line shuffle | Weak | Pair score 0.2216 vs 0.2146, p ≈ 0.002. |
| C→L→P→R carries information beyond Markov structure | **Not supported** | Fails Markov-1 (p ≈ 0.13) and Markov-2 (p ≈ 0.40) twins. The 4-token full-cycle rate falls *below* every null. |
| C→L→P→R is the manuscript's preferred order | Mixed | Ranks #1/24 on the full corpus and on both random folio halves. Ranks #5/24 in Currier A and #2/24 in Currier B. The reviewer's untouched split gave #3/24. |
| Knowing the state predicts the next state | **Not supported** | 0.017 bits/token of information gain; accuracy 31.7% vs 28.3% majority baseline. |
| The published ending→state role map is what the manuscript selects | **Not supported** | Random groupings of the same endings (best of 6 cycles each) score higher than the published map: p ≈ 0.99. |
| Published glosses predict manuscript context | **Not supported** | Glossed tokens fall in the section their meaning predicts 28.1% of the time; shuffled glosses do 26.8% ± 7.0% (p ≈ 0.41). |
| 90.2% blind holdout prediction | **Withdrawn** | See below. |
| 99.79% Macer Floridus manifold congruence | **Withdrawn** | See below. |
| Δ = −1.018 directional routing shift | **Withdrawn / under review** | See below. |
| Venetian / German procedural semantics | Not established | No test in this repository constrains the glosses independently of the morphology they were derived from. |

## Clean blind holdout (added 1 October 2026)

A replacement for the withdrawn 90.2% test. Run it with `python blind_holdout.py`; results are in
[`output/blind_holdout_report.md`](output/blind_holdout_report.md). It is also on the Holdout tab of the app.

- **Holdout:** 43 folios, drawn at random (seed 20261001) from the 216 folios never used for cribs, the
  dossier or the old holdout. The list is in `data/blind_holdout_v1.json`. It was committed on its own,
  before any scoring code existed, and must not be edited.
- **Model:** trained only on the other 184 folios. Its single input is each token's ending under the
  frozen parser rules.
- **Targets:** none of them can be read off the token's own spelling.

| Target | Result | Verdict |
|---|---|---|
| A. Which token ends the line (15 endings) | AUC 0.671 vs 0.501 chance, p ≈ 0.0005 | **PASS** |
| A. Same, using only the 4 states C/L/P/R | AUC 0.581 vs 0.501, p ≈ 0.0005 | **PASS** (weaker) |
| B. Label / diagram text vs paragraph text | AUC 0.635 vs 0.500, p ≈ 0.0005 | **PASS** |
| C. Which section each folio belongs to | 65.1% correct; always guessing "Herbal" also scores 65.1% | **FAIL** |
| D. A token's stem (prefix and ending removed) predicts its ending | 0.775 bits/token better than ignoring the stem, p ≈ 0.001 | **PASS** |

Target D was added later, as Juan's "recurring carrier stems" check. It was committed before its first
run on this holdout. Part of its signal is orthographic (letters next to the ending), so it shows
consistent word-building across pages, not meaning.

The endings carry real, transferable information about line position and page layout on pages the
model never saw. Grouping the endings into the four C/L/P/R states loses about 30% of that
information (0.048 → 0.034 bits per token). This is consistent with the affix-role tournament:
position is carried by individual endings more than by the four-state grouping.

The rule that section prediction must also beat the majority guess was added after the first run.
It is stricter only, and no score changed.

## Transfer to a second representation

`python transfer_test.py` reruns the frozen tests on a second representation of the text: ZL's last
alternative readings, with uncertain spaces not treated as word breaks (36,218 tokens instead of
38,958). Every verdict is unchanged. -m/-am line-end OR is 20.7 vs 20.3; blind A AUC 0.671 vs 0.675;
blind B AUC 0.635 vs 0.644; blind D 0.775 vs 0.744 bits; C→L→P→R still fails the Markov twins.
Details are in [`output/transfer_report.md`](output/transfer_report.md).

This shows the results don't hinge on ZL's editorial choices. It is **not** an independent
transcription. Takahashi's `IT2a-n.txt` (voynich.nu) could not be downloaded from the environment
these tests ran in. Run `python transfer_test.py --corpus IT2a-n.txt`, or upload the file in the
app's sidebar, to complete the external-transfer step.

## Structure-only presentation

Following the advice to strip the model back to what works, the app now shows only the structural results.
The glosses and the four-state presentation have been removed from it; their code is in `archive/`.

## What kind of system? (October 2026)

### Is line-final -m/-am a space-saving device? (pre-registered)

Pre-registration: `analyses/m_abbreviation_prereg.md`, committed before the code
(`analyses/m_abbreviation_test.py`). Report: [`output/m_abbreviation_report.md`](output/m_abbreviation_report.md).

- **Decision under the pre-registered rule: H_space supported.**
- The key result: -m/-am is about **half as common at the end of paragraphs** (8.5% vs 16.1% of
  line-final tokens, p ≈ 1e-4), where the scribe was not short of room. An end-of-unit marker
  ("seal", "finis", "flush") predicts the opposite, so the terminator reading is disfavoured.
- Line-final -m/-am forms are shorter than the same stem's mid-line forms (p ≈ 1e-4). This is
  partly built in, because -am is a short ending.
- Lines ending in -m/-am are **not** measurably fuller (P1 fails), so it is not simply "ran out of room".
- -m/-am words reuse ordinary stems: they are normal words in a line-end form, not a special vocabulary.

Best current reading: **-m/-am is a scribal line-end variant**, used when a line breaks inside running
text and avoided at paragraph ends.

### Comparison with real Latin and a simple cipher (exploratory)

`analyses/comparison_fingerprint.py` applies one generic pipeline (ending = last 2 letters) to Voynich
paragraph text, Latin recipe prose (Apicius), medieval Latin prose (Albertanus, 13th c.; Bede, 8th c.),
and Apicius under a fixed verbose letter cipher. Report:
[`output/comparison_fingerprint_report.md`](output/comparison_fingerprint_report.md).

| | Voynich | Latin texts | Latin, verbose cipher |
|---|---:|---:|---:|
| Strongest line-final ending, odds ratio | **22.9** (-am); **1.8** once the same words are re-lined | 1.7–2.8 | 1.7 |
| Conditional character entropy h2 (bits) | 2.11 | 3.20–3.36 | 2.39 |
| Mean word length | 4.96 | 5.7–6.1 | 11.8 |
| Stem → ending information (bits/word) | 1.35 | 3.5–3.7 | 3.35 |
| Same word twice in a row | 0.84% (0.37% if shuffled) | 0.01–0.21% | 0.21% |

What this suggests:
- The line-end effect **disappears when the Voynich's own words are re-lined**, so it belongs to
  the physical lines of the manuscript. This fits the scribal-convention reading above.
- Voynich characters are far more predictable than Latin letters (low h2). A letter-by-letter cipher
  of Latin moves h2 toward Voynich but makes words more than twice too long, so a simple letter
  cipher of Latin does not fit.
- Voynich endings are much less tied to their stems than Latin inflections are, under this generic
  definition.

Limits: Latin only (Italian or German texts can be dropped into `data/comparison/`); the re-lined
texts have no real manuscript lines; h2 depends on the transcription alphabet. A faithful
implementation of the published Timm & Schinner self-citation algorithm is still needed for a fair
"hoax" comparison. A first, simplified version produced unrealistic text and was removed rather
than tuned.

### Do the two halves of a folded sheet belong together? (pre-registered)

Pre-registration: `analyses/fold_sheets_prereg.md`. Code: `analyses/fold_sheets_test.py`. Report:
[`output/fold_sheets_report.md`](output/fold_sheets_report.md).

The idea, from the project author: folding brings the front, back and center fold together. In a
gathering, leaf k and leaf lo+hi−k are halves of one folded sheet.

- **Pre-registered decision: Supported.** Sheet halves share more vocabulary than random leaf pairs in the
  same gathering: cosine 0.573 vs 0.472, p ≈ 1e-4. This holds even after excluding center-fold
  (adjacent) pairs: 36 sheets.
- **Same scribe and language don't explain it** (exploratory follow-up): 21 of 27 same-scribe,
  same-language sheets, p ≈ 2e-4.
- **No positional line-up.** The same word at the same spot when folded is not significant without
  adjacent pairs (p ≈ 0.015).
- **Reading:** sheets look like units of writing, consistent with the text being written on loose sheets
  before binding. That is useful for reconstructing the original page order. It does **not** show a
  positional key.

### Fold overlay (exploratory)

The idea: fold the front and back pages in toward the center; the words that land on each other form
a key. `archive/pages/12_Fold_Overlay.py` (built on `archive/analyses/fold_overlay.py`, now archived) folds any page onto any other,
mirroring it left-to-right. Positions are approximated from line number and place in the line. It
then folds every other page onto the same target, for a fair comparison.

| Folded page → target | Same word | Same ending | Other pages scoring at least as high |
|---|---:|---:|---|
| f1r → f116r | 0.5% | 8.4% (typical 6.8%) | 30% / 23% |
| f1r → f58r | 0.5% | 13.1% (typical 8.0%) | 10% / 9% |
| f1r → f58v | 0.0% | 12.6% (typical 9.1%) | 100% / 20% |
| f116r → f58r | 0.2% | 6.9% (typical 8.0%) | 18% / 66% |
| f116r → f58v | 0.0% | 7.7% (typical 9.3%) | 100% / 71% |

None of these stand out from ordinary pages. f58r/f58v were used as the center, as the middle of
gathering H (whose central leaves f59–64 are missing). Exact page coordinates from the Beinecke images
would make the overlay more precise than this line-and-word approximation.

### Looking for a key inside the manuscript (October 2026)

**Zodiac labels as day names (pre-registered).** Each sign has 29–30 labelled figures, about one per day.
If the labels name days, the same position on different months should carry the same name.
Pre-registration: `analyses/zodiac_days_prereg.md`. Code: `analyses/zodiac_days_test.py`. Report:
[`output/zodiac_days_report.md`](output/zodiac_days_report.md).
**Decision: Not supported.** Best-rotation positional similarity is 0.123, against 0.125 for shuffled
labels (p = 0.76). Almost all labels start with `o` (`ot-`, `ok-`, `ol-`, `op-`), unlike running text.

**Anomaly scan (exploratory).** `analyses/anomaly_scan.py`, also the app page *Anomaly Scan*. Each page
is compared with pages of the same section and Currier language. Report:
[`output/anomaly_scan_report.md`](output/anomaly_scan_report.md).
- It finds the transcription's key-like pages on its own: **f57v #1** (score 21) and **f49v #9**.
- f1r ranks near the bottom, because its Roman-alphabet "key" is in the margin and is not part of the
  transcribed Voynich text. That needs the page images.
- New candidates: f86v3 and fRos (rosettes), f67r1 (12-sector diagram), f67v2, f17r, f3r, f105v, f116r.

**Key-like sequences.** The f57v ring repeats a 17-symbol cycle four times. The f49v margin column repeats
"p o ● y e ●" twice. Neither contains the most common letters of the running text (e, h, a, c, i), so
neither looks like a complete alphabet for the main script. They read more like lists of special
symbols. f57v and f58r (the transcription suspects a key there too) sit at the center of the book,
beside the missing leaves f59–64.

## Instrument hypothesis (October 2026)

Do the circular diagrams show a measuring instrument (astrolabe/volvelle)? Pre-registered in
`analyses/instrument_prereg.md`, checked against the Yale images. Pointer lines: 1 (needed 3). Centre
pivots: none (needed 2). Labels repeating at the same angular position on non-zodiac circles: p = 0.0195
(needed < 0.01). Rim strokes could not be counted at PDF resolution. **Not supported** under the
pre-registered rule, whatever the rim count. Details: `output/instrument_report.md`.

## Fifth-element cycle (October 2026)

Does the C → L → P → R cycle work if the roleless words (`?`, 14% of paragraph text) are added as a fifth,
"grounding" step? Pre-registered in `analyses/fifth_element_prereg.md`. In every placement, full five-step
runs occur **less** often than in shuffled or Markov text (p = 0.97 and 0.99 against Markov-1 and Markov-2).
**Not supported.** Details: `output/fifth_element_report.md`.

## Alchemy (October 2026)

Do the drawings show the usual marks of an alchemical book? Pre-registered in `analyses/alchemy_prereg.md`;
every page of the Yale images viewed. No fire, stills or alembics (the pool-and-pipe pages f78r, f81r and f83v
are borderline and excluded by the rule). No metal or planet signs. **Not supported.** The pictures fit
herbal, pharmacy, healing-bath and astrology books better. Details: `output/alchemy_report.md`.

## Writing types, word order, topic location (October 2026)

Pre-registered in `analyses/writing_types_prereg.md`. Splitting the text into paragraph A, paragraph B, ring
text, labels and radial text: **word order carries information** beyond line-start/line-end habits in A, B
and ring text (p = 0.001; not caused by repeated words). **Word beginnings track the page's topic more than
endings do** (with the A/B difference removed). **Supported.** Details: `output/writing_types_report.md`.

## Label beginnings vs picture kind (October 2026)

Do labels on different kinds of picture (jars vs plant parts; bathing figures vs pools) start differently, on
the same pages? Pre-registered in `analyses/dictionary_prereg.md`. Neither passed (p = 0.080, 0.34): **not
supported**. Not part of the verdict: jar-label *endings* differ from plant-part-label endings (p = 0.002), a
lead for a follow-up test. Details: `output/dictionary_report.md`.

## Set phrases and grammar links (October 2026)

Pre-registered in `analyses/phrases_prereg.md`. Paragraph text has about 3 times as many strongly bound word
pairs (set phrases) as shuffled text, in both Currier A and B. The strongest link between neighbouring words runs
from a word's **ending** to the next word's **beginning** (e.g. -dy → qok-). This holds whether or not
uncertain spaces are split. **Supported.** Details: `output/phrases_report.md`.

## Zodiac halves (October 2026)

Do the light and dark halves of Aries and Taurus share label beginnings? Pre-registered in
`analyses/zodiac_halves_prereg.md`. It passed by its own rule (p = 0.0025), but an extra check after the run
found the cause: all four half-pages are equally similar whatever their sign, because their labels are mostly
`ot-`. The effect is page format, not sign. **Not counted as evidence.** The pre-registered control was too
weak, and that is recorded rather than hidden. Details: `output/zodiac_halves_report.md`.

## Plant-name anchors (October 2026)

Are the pharmacy plant-part labels plant names that reappear on their herbal page? Pre-registered in
`analyses/plant_anchor_prereg.md`. Label words are no more page-concentrated in herbal text than ordinary words
(p = 0.11), and 115 of 182 never appear there. **Not supported.** An extra check after the run found that f58r/f58v
show no excess. Details: `output/plant_anchor_report.md`.

## Refrains (October 2026)

Does the text repeat longer phrases, as prayers or charms do? Pre-registered in `analyses/refrains_prereg.md`.
Dialect B repeats 3-word formulas well beyond chance (12 vs 0.6), mostly on the bath pages. There are no long
(4-word) refrains, and dialect A has no repeats at all. **Partly supported.** This fits short formulas
(instructions, recipes or brief charms), not long prayers. Details: `output/refrains_report.md`.

## Ground test: labels in their own page's text (October 2026)

Does a page's paragraph text repeat that page's label words more than other pages of the same section do?
Pre-registered in `analyses/ground_prereg.md`. Bath pages: 24 vs 23.2 expected (p = 0.45). All sections: 60 vs 58.2
(p = 0.38). **Not supported**: no link between the text and its page's labelled pictures was found.
Details: `output/ground_report.md`.

## Rare symbols in first lines (October 2026)

Do rare symbols (ZL3b `@nnn`) land in the first line of pages and paragraphs more than chance? Pre-registered in
`analyses/rare_symbols_prereg.md`, with shuffles within each page. Page-first lines: 32 vs 8.3; paragraph-first
lines: 36 vs 9.6 (both p = 0.0001). **Supported.** The commonest rare symbols sit in line-first words, which fits
decorated initial forms. Details, and a map of where every rare symbol lands: `output/rare_symbols_report.md`.

## Plant openings and star names (October 2026)

Do the opening words of herbal pages share unusual spellings with star labels more than with other labels?
Pre-registered in `analyses/plant_star_prereg.md`. 13 of 116 opening words share a rare 3-letter chunk with star
labels, against 4.4 expected (p = 0.0002). This holds when the comparison labels are matched on starting with
"o" + gallows (p = 0.0003; labelled extra check). The typical form is star label = "o" + plant opening stem
(koaiin ~ okoaly, pocheody ~ opocphor). **Supported**, as a lead that plant and star names share stems.
Details: `output/plant_star_report.md`.

## Fibonacci numbers (October 2026)

Do counts (words per line, letters per word, lines per paragraph and page, words and labels per page) land on
Fibonacci numbers, or on the doubled sequence 10/16/26/42, more than on their neighbours? Pre-registered in
`analyses/fibonacci_prereg.md`. The Fibonacci test formally passed, but only because 5 letters is the peak
Voynich word length, which breaks the test's smoothness assumption. Without it: 33.2% vs 33.3% expected (p = 0.59).
The doubled sequence: no preference (p = 0.78). **Not supported**, and the design flaw is recorded.
Details: `output/fibonacci_report.md`.

## Name-link map (October 2026)

Every pairing of paragraph-opening words (by section) with label types (42 cells, Bonferroni-corrected).
Pre-registered in `analyses/name_map_prereg.md`. The first run used too few draws to ever pass; this is recorded and
the test was rerun with 20,000. Two links pass: Herbal × star labels (the earlier finding) and Biological × pharmacy
plant-part labels (3 vs 0.6, p = 0.00005; small counts). Both follow the same form, label = "o" + opening word (e.g.
*tokol → otokol*), and several near misses do too. **Supported, tentatively**: "o" may mark a name or label form
of a word. Details: `output/name_map_report.md`.

## "o" as a name-forming prefix (October 2026)

Are labels starting with "o" more often "o + an existing word" than ordinary paragraph words starting with "o"?
Pre-registered in `analyses/o_prefix_prereg.md`, length-matched. Labels 41% vs paragraph words 39% (p = 0.84).
**Not supported.** "o" is a general prefix everywhere. This corrects the reading of the plant–star and
name-map links: they show shared roots, not a special name-forming "o". Details: `output/o_prefix_report.md`.

## Root dictionary (October 2026)

Word roots (prefix q/o/y and ending stripped by a fixed rule) follow the page's section: 0.214 vs 0.103 bits,
p = 0.0005 (shuffles within Currier language). Pre-registered in `analyses/root_dictionary_prereg.md`. 23 roots are
section-specific at FDR 5%, all in Currier-B sections. Recipe pages favour *cheed, lkee, rar, pair, alk, tched*.
Bath pages favour *rsh, sheckh, lsh, lch*. No Herbal or Pharmacy roots pass. **Supported.**
Details: `output/root_dictionary_report.md`.

## Bath roots in bath-picture labels (October 2026)

Do the bath-page roots (rsh, sheckh, lsh, lch) appear in labels on the bath pictures? Pre-registered in
`analyses/bath_roots_prereg.md`. There are only 4 hits among 1,186 label words, so the result is **too few to test**.
Descriptive only: 3 of the 4 are on bath pages, all labelling women, none labelling pools. Details:
`output/bath_roots_report.md`.

## Calendar cycles in the star-marked paragraphs (October 2026)

The 285 surviving star-marked paragraphs (about 335–365 with the missing folios 109–110) were tested for recurring
similarity at week (7), month (27–31) and any spacing from 2 to 40. Pre-registered in `analyses/cycles_prereg.md`.
Week p = 0.09, month p = 0.45, no other spacing passes. **Not supported.** Details: `output/cycles_report.md`.

## Scribe vs topic (October 2026)

Scribe and section overlap almost completely, so the two were separated (pre-registered in
`analyses/scribes_prereg.md`). Herbal pages by different scribes use different roots (p = 0.0005; scribe and
dialect cannot be separated). Within scribes 1 and 2, roots still change with section (p = 0.0005). Word order and
the ending → next-beginning link hold for **every** scribe with enough text (1, 2, 3). **Supported**: writer and
topic both matter, and the grammar belongs to the shared system. Each scribe's text, in book order:
`output/scribes/`. Details: `output/scribes_report.md`.

## Shared grammar table across scribes (October 2026)

Is the ending → next-beginning pattern the same for scribes 1, 2 and 3? Pre-registered in
`analyses/grammar_table_prereg.md`. Log-lift tables correlate 0.67–0.88 between scribes, against 0.17–0.36 for
shuffled text (p = 0.001 for every pair). Scribes 2 and 3 agree almost as well as each scribe agrees with itself.
**Supported: one grammar shared by different writers.** Recurring rules include -ar/-or → ai/al/ar,
-ol → k-words, -dy → qo-. Details: `output/grammar_table_report.md`.

## Glue words vs content words (October 2026)

In known languages, short frequent words are topic-neutral. Among Currier-B words of similar frequency, is length
related to topic-boundness? Pre-registered in `analyses/glue_words_prereg.md`. ρ = −0.02, p = 0.77: **not
supported**. Several short words are strongly topic-bound (*qol, sol, dy, am*). This is another difference from an
ordinary language. Details: `output/glue_words_report.md`.

## Slot freedom compared with Latin (October 2026)

How much does a word's start (first 2 letters) limit its end (last 2 letters)? Measured the same way in Voynich A
and B, three Latin texts, and an enciphered Latin text. Pre-registered in `analyses/slots_prereg.md`. Two resampling
errors in the first run were found and corrected (recorded). Voynich 0.065–0.073; Latin 0.101–0.284; cipher 0.218.
The Voynich is the lowest, but its interval overlaps Bede's, so the result is **MIXED** under the rule. Word parts
combine more freely than in Latin, but the separation is not decisive. Details: `output/slots_report.md`.

## 19 / Metonic cycle (October 2026)

Do diagram counts equal 19, 235 or 6,940, or do ring texts repeat every 19 steps? Pre-registered in
`analyses/nineteen_prereg.md`. The method detects the known 17-glyph cycle on f57v (control, p = 0.002). No
period-19 repetition (word level p = 0.41, glyph level p = 0.39). One count of 19 among 203 (pharmacy labels,
f102v2). **Not supported.** Details: `output/nineteen_report.md`.

## Zipf's law of abbreviation (October 2026)

Are frequent words shorter, as in all human languages? Pre-registered in `analyses/brevity_prereg.md`. Voynich B
0.11 (the weakest of six texts), Voynich A 0.22, Latin 0.18–0.41, cipher 0.17. **MIXED.** The Latin recipe text is
also weak, so genre may explain Voynich B's low value. Details: `output/brevity_report.md`.

## Frequency match: Voynich as letter-for-letter Latin (October 2026)

Pre-registered in `analyses/freqmatch_prereg.md`: a rank-frequency key improved by hill climbing to maximise
Latin letter-pair likelihood. The control (enciphered Latin) was cracked 100%. The Voynich scored high on letter
pairs (formally "consistent"), but its best keys give only 10–16% real Latin words, against 86% for Latin and 12%
for reversed Latin. The pre-registered criterion was too weak (recorded). **Conclusion: not simple-substitution
Latin.** Details: `output/freqmatch_report.md`.

## Rhythm: beats in lines, waves down pages (October 2026)

Does any word ending recur at a regular spacing within lines, or does the share of qo- words rise and fall in
waves from line to line? Pre-registered in `analyses/rhythm_prereg.md`. Nothing passes the corrected thresholds.
There are near misses at 6 lines (A) and 7 lines (B). **Not supported.** Details: `output/rhythm_report.md`.

## Vowels and consonants (Sukhotin) (October 2026)

Do Voynich symbols alternate like vowels and consonants? Pre-registered in `analyses/vowels_prereg.md`. The method
recovers a e i o u in Latin. Voynich alternation above its own shuffled baseline is 56–82% of Latin's in all four
cases (dialect × symbol scheme). **Supported: alphabet-like.** The vowel-like symbols are mainly o, a, e, y. The
result is strongest with ch/sh treated as single letters. Caveat: strict slot patterns also produce alternation.
Details: `output/vowels_report.md`.

## Star-name crib and sound shapes vs languages (October 2026)

Pre-registered in `analyses/sound_shapes_prereg.md`. With vowels a, e, o, y, star labels do not match the
consonant/vowel shapes of 32 medieval astrolabe star names more than other labels do (p = 0.45): **not supported**.
Compared with Latin and 26 modern languages by word sound shape, no language is closer to the Voynich than the
Voynich is to a letter-shuffled copy of itself: **no close language**. Details: `output/sound_shapes_report.md`.

## Diagram labels as measurements (October 2026)

Are labels farther apart around a wheel less alike, as coordinates would be? Pre-registered in
`analyses/coordinates_prereg.md`, on the 12 zodiac wheels (298 positioned labels). Correlation between angular
distance and label dissimilarity +0.050, against +0.001 shuffled (p = 0.0009). **Supported, weakly.** A scribe
drifting while labelling in order around the wheel would produce the same pattern. Details:
`output/coordinates_report.md`.

## Label gradient: position or writing order? (October 2026)

Pre-registered in `analyses/coord_vs_drift_prereg.md`. Zodiac label similarity follows angle when writing order is
controlled (partial ρ = +0.046, p = 0.0014). Writing order adds nothing when angle is controlled (p = 0.20).
**Verdict: position (measurement-like)**, not scribal drift. Writing orientation around the wheel remains a possible
cause. Details: `output/coord_vs_drift_report.md`.

## Writing orientation as the cause of the label gradient (October 2026)

Pre-registered in `analyses/orientation_prereg.md`. Labels at the same absolute angle on different zodiac wheels are
not more alike (ρ = +0.003, p = 0.25), so page orientation does not explain the within-wheel gradient. **The
measurement-like reading stands:** labels vary gradually with position within their own wheel. Details:
`output/orientation_report.md`.

## Counting: do zodiac labels lengthen steadily around each wheel? (October 2026)

Pre-registered in `analyses/counting_prereg.md`, with the same best-start search for real and shuffled labels. Mean
best correlation 0.480 against 0.421 shuffled (p = 0.025): **not supported** at p < 0.01, though suggestive. The best
starts and directions vary between wheels. Details: `output/counting_report.md`.

## Sun–Moon phase pages (October 2026)

Image check, pre-registered in `analyses/sun_moon_prereg.md`. Where Sun and Moon are drawn together (f68r1, f68r2),
the Moon is a crescent even when opposite the Sun: **not a phase table**. Observation made after looking (a lead,
not evidence): f67r2's 12 moons nearly alternate red crescent / gold disc (6 + 6), consistent with alternating 30-
and 29-day lunar months (a 354-day lunar year). Details: `output/sun_moon_report.md`.

## Flower colours as keys (October 2026)

All 118 herbal pages were classified by flower colour from the images **before** comparing text
(`analyses/flower_colours.csv`). Pre-registered in `analyses/flower_colour_prereg.md`. Pages with the same flower
colour do not share more vocabulary than other pages (p = 0.74, shuffled within Currier language). **Not
supported.** Details: `output/flower_colour_report.md`.

## Plant-matching star labels on marked stars, f68r (October 2026)

From Erin's photo of the f68r fold-out, the star labels on f68r1 and f68r2 were placed on their individual stars, and
each star's centre was classified as hollow ring, dark dot or plain. On f68r1 (the discovery panel), 3 of the 5
plant-matching labels sat on ringed stars (p = 0.21, noticed after looking). The pre-registered confirmation on
f68r2 + f68r3 found 0 of 4 on marked stars, against 0.8 expected (p = 1.0). **Not supported.** Pre-registration:
`analyses/star_centres_prereg.md`. Details: `output/star_centres_report.md`. The label-to-star placements
(`analyses/star_centres_*.csv`) are a reusable by-product.

## The metal key: planetary scale and sevens (October 2026)

Flower colours were mapped to metals with a period key fixed in advance (heraldic planetary tinctures: white = Moon
and silver, green = Venus and copper, yellow = Sun and gold, red = Mars and iron, blue = Jupiter and tin).

- **Test 1:** pages whose metals sit closer on the medieval planetary scale ("music of the spheres") do not have more
  similar text (ρ = −0.08, p = 0.21).
- **Test 2:** herbal pages 7 apart in book order are not more alike than pages 6 or 8 apart (p = 0.42), and no other
  lag from 3 to 12 stands out.

**Not supported.** Pre-registration: `analyses/metal_key_prereg.md`. Details: `output/metal_key_report.md`.

## Correspondence chains: herb → star → body (October 2026)

Do the rare word chunks shared by herbal openings and star labels continue into the bathing, pool and zodiac-figure
labels (a herb → star → body chain)? **No.** 1 chain was found against 4.8 expected (p = 1.0): the body labels
*avoid* the herb–star roots. Secondary result: herb → star → **remedy** (pharmacy jar and plant-part labels) gave 3
chains against 1.2 expected (p = 0.08, not significant). Examples: tydlo (f9r) → otydy/otydg (stars) → otyda/otydary
(f88r/v), and tdokchcfhy → chocfhy → ykocfhy/sochorcfhy. Pre-registration: `analyses/chains_prereg.md`. Details:
`output/chains_report.md`.

## f67r2: the 12 moons as full and hollow months (October 2026)

From Erin's photo, each of f67r2's 12 moons was classified as red crescent (6) or gold (6), and each moon label was
placed on its moon. The labels run clockwise around the ring in the same order as the transcription.

- **Alternation:** colours alternate at 10 of 12 steps (chance 6.6), with two breaks (gold–gold at 86°/115° and
  red–red at 152°/177°). p = 0.067, **not significant** at the registered 0.025.
- **Labels:** red-moon and gold-moon labels are no more alike within colour than across (p = 0.50).

**Not supported.** Pre-registration: `analyses/moon_months_prereg.md`. Details: `output/moon_months_report.md`.

## Two-colour leaves (October 2026)

All 118 herbal pages were classified for leaves painted in two colours, as on f1v (21 yes) **before** any text
comparison. Two-colour pages are not textually closer to each other than to other pages (p = 0.49), and they are
not over-represented among the star-matching openings (1 of 21; p = 0.94). **Not supported.** Pre-registration:
`analyses/leaf_colour_prereg.md`. Details: `output/leaf_colour_report.md`.

## f57v ring (descriptive, October 2026)

Ring 3 is exactly 17 symbols × 4 repeats (68 symbols; 3 variants). Its rare symbols @169 and @172 recur only in the
single-letter margin column of f66r. Not a test. Notes: `analyses/f57v_ring_notes.md`.

## Implementation problems found and fixed

1. **The live app loaded zero tokens from the corpus.** Every IVTFF text line starts with
   `<f…`, and the old `app.py` loader treated every such line as a folio header, then
   skipped it. So the dashboard's headline figures were all fallback constants: token
   count 0, "69.4%" line flush, "Δ = −1.018", a 20-token hand-typed "holdout", a "30.3%"
   baseline and "p = 0.0000". Even with that fixed, the old loader split on whitespace,
   which would have merged each ZL line into one token, because ZL separates words with
   `.` and `,`.
   *Fix:* `app.py` now loads through the canonical `parser.parse_zl3b` and nothing else.
2. **Numerical fallbacks.** All of them are removed. A value that cannot be computed now
   shows `not computed`. The same applies to the offline sample corpus and the default
   transition, Slot Ω, reader and colophon tables.
3. **Two state maps.** `app.py` had its own macrostate rules. For example, it put `-ol`
   and `-or` in L, while `parser.py` puts `-ol` in P. The app now delegates to `parser.py`.
4. **Parser details.** The `<->` drawing-gap marker was gluing neighbouring words
   together on 627 lines. Line-end flags were also computed before empty tokens were
   dropped. Both are fixed. The parser now records `locus_type` (P / L / C / R), so
   paragraph text can be separated from labels, rings and radii.
5. **Macer Floridus alignment.** `engine_manifold_align.py` (now in `archive/`) built the "historical" target
   vectors with `np.random.randn()`. It also aligned 10 anchors in 16 dimensions, where an
   orthogonal map fits almost any configuration. The resulting 99.79% says nothing about
   Macer Floridus. The module now refuses to run without a real, tokenised target corpus.
   It requires at least 3 anchors per dimension and reports a shuffled-anchor null.
6. **"Semantic" and "affix-role" tournaments in the app.** Both used to compute bigram
   mutual information of tokens (or prefix+suffix strings) against a global shuffle,
   which tests neither semantics nor the role map. They now run tests 6 and 5 of
   `structural_validation.py`.

## Withdrawn headline claims

- **90.2% blind prediction (394/437).** The five holdout folios (`f70v2`, `f71r`, `f72r1`,
  `f72v1`, `f72v2`) are also in `blind_test.SEEN_FOLIOS`, the folios already used for the
  dossier. The score also compares `predict_apparatus_role` with `get_expected_role`, and
  both are suffix rules applied to the same token string. That measures how much two rule
  sets overlap, not prediction of independent ground truth. On the real tokens of those
  folios the agreement is 70.6% (538 tokens) against a 31.6% label-shuffle baseline. A
  clean replacement needs a new holdout, chosen and frozen before any rules are adjusted.
- **99.79% Macer Floridus congruence.** It came from random target geometry (see item 5
  above). To rebuild it, supply a real Macer Floridus transcription to
  `CrossLingualManifoldAligner.run_alignment_benchmark`.
- **Δ = −1.018.** This was the fallback constant shown when the loader returned no data.
  The same formula on correctly parsed tokens gives **Δ ≈ +1.50**: `-al` is *more* likely
  than `-ar` to be followed by a `k-`/`d-` token, which is the opposite sign. Any claim
  built on the sign of this shift, including the "hoax falsified" framing, needs to be
  re-derived.

## What looks real

The morphology-plus-position layer holds up. Voynich endings are not distributed
randomly with respect to the physical line, and -m/-am is the strongest case by a wide
margin. The literature has noted a line-final preference for `m` before, so this confirms
the parser captures a real property of the text. It is not by itself evidence for any
reading of it.

## Suggested next steps

1. Keep the structural layer frozen and meaning-free. Diagram vs prose, line position and carrier
   stems now pass on blind folios; section does not. **Still open:** an independent transcription
   (Takahashi `IT2a-n.txt`; see REPLICATION.md) and Currier hand as a target.
2. ~~Pre-register a new holdout~~ Done: `data/blind_holdout_v1.json` (see above). For the next rule
   version, draw a fresh holdout (v2) rather than reusing v1.
3. Rebuild the semantic layer only on top of targets the glosses make *different*
   predictions for. Then re-run the semantic permutation tournament. If the published
   glosses win decisively there, that result would matter.
4. Try ending-level position models (per-ending line-final rates) before four-state
   machines. The per-ending table suggests position is carried by individual endings
   more than by the C/L/P/R grouping.
