# Voynich Manuscript: Structural Findings (October 2026)

**Erin (RN-Top/Voynich)**. Every result below was pre-registered: the prediction, statistic, null model and
threshold were committed to this repository before the test was first run. Failed tests and design mistakes are
reported alongside the successes in [VALIDATION.md](VALIDATION.md). None of this decodes the text. It describes the
text's structure.

Data: ZL3b transliteration (`data/ZL3b-n.txt`, IVTFF, version 3b of 13/05/2025), parsed by `parser.py`. Images: the
Yale Beinecke MS 408 digital facsimile.

## Main findings

### 1. Plant-page openings share word roots with star names; "o" may mark a name form

- **Test:** do the first words of the herbal pages share unusual 3-letter chunks with the star labels (f67r2,
  f68r1–3) more than with the same number of other labels?
- **Result:** 13 of 116 opening words share a chunk with star labels, against 4.4 expected (p = 0.0002).
- **Robustness:**
  - **Matched control.** Labels often begin "o" + gallows, so the comparison labels were matched on that start.
    The result holds: 13 vs 4.5 (p = 0.0003).
  - **Section-wide map (42 cells, Bonferroni).** A second, independent link appears: bath-page paragraph openings ×
    pharmacy plant-part labels (3 vs 0.6, p = 0.00005).
- **Recurring form:** label = **"o" + paragraph-opening word**:

  | Opening word | Label |
  |---|---|
  | koaiin / koary / koair (f3v, f6v, f13v) | okoaly (star, f68r1) |
  | pocheody / pochaiin / pochof (f16r, f19v, f27v) | opocphor (star, f68r2) |
  | tydlo (f9r) | otydy (star, f68r1), otydg (star, f68r3) |
  | o+@167+chal (f56r) | o+@167+olch… (star, f68r2) |
  | tokol (f82v, bath page) | otokol (plant-part label, f88v) |

- **Reading:** plant and star names (and labels elsewhere) appear to be built from shared roots, with a
  prefix "o" forming the label or name.
- **Caveats:** small counts (13 and 3 words); each link is a shared 3-letter chunk. The first run of the map test
  used too few permutations to reach its threshold, and was rerun with 20,000 (recorded).
- **Files:** `analyses/plant_star_*`, `analyses/name_map_*`, and `output/plant_star_report.md`,
  `output/name_map_report.md`.

### 2. Rare symbols concentrate in first lines

ZL3b `@nnn` symbols land in page-first lines 4× more than chance (32 vs 8.3) and in paragraph-first lines likewise
(36 vs 9.6). Both p = 0.0001, with the null shuffling which line counts as "first" within each page. The commonest
rare symbols sit in line-first words, which fits decorated initial forms.
Files: `analyses/rare_symbols_*`, `output/rare_symbols_report.md`.

### 3. The text behaves like language, not lists or generated noise

| Finding | Result | Files |
|---|---|---|
| Word order carries information beyond line-start/end habits | Currier A, B and ring text, p = 0.001; not caused by repeated words | `writing_types_*` |
| Set phrases | about 3× more strongly bound word pairs than shuffled text (A: 16 vs 4.8; B: 100 vs 28.7) | `phrases_*` |
| Grammar link | a word's **ending** predicts the next word's **beginning** most strongly (e.g. -dy → qok-) | `phrases_*` |
| Topic | word **beginnings** track the page's section more than endings do (A/B difference removed) | `writing_types_*` |
| Short formulas | Currier B repeats 3-word formulas (12 vs 0.6), concentrated on the bath pages; no long refrains | `refrains_*` |
| Line-end form | -m/-am is a line-end variant (605 of 861 line-final; rare at paragraph ends) | `m_abbreviation_*` |
| Writing units | the two halves of a folded sheet share more vocabulary than other page pairs | `fold_sheets_*` |

## Tested and not supported (selection)

Translations (Venetian/German glosses); the C→L→P→R cycle (also with a fifth step); a fold-over key; zodiac labels
as day names; the circles as a measuring instrument; alchemy (no apparatus or metal signs); pharmacy labels as plant
names; labels repeated in their own page's text; label beginnings by picture type; Fibonacci counts (the formal pass
was a word-length artifact); zodiac halves sharing labels (explained by page format). Full list with numbers:
[VALIDATION.md](VALIDATION.md).

## How to reproduce

```bash
pip install -r requirements.txt
python analyses/plant_star_test.py
python analyses/name_map_test.py
python analyses/rare_symbols_test.py
python analyses/writing_types_test.py
python analyses/phrases_test.py
```

Each script writes its report to `output/`. The pre-registration for each test is the matching
`analyses/*_prereg.md`, and its git history shows that it was committed before the code first ran.

## Open questions for reviewers

1. Has the "o + opening word" relation between labels and paragraph openings been reported before?
2. Is a shared rare 3-letter chunk a fair similarity measure, or is there a better standard?
3. A full-resolution mapping of the f68r star labels to individual drawn stars would allow testing whether the
   matching stars are special. Does such a mapping exist?
