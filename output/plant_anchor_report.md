# Are the pharmacy plant-part labels plant names?

Pre-registration: `analyses/plant_anchor_prereg.md`. 192 label words (182 distinct, 4+ letters) from the pharmacy plant-part labels; herbal text 11,396 words on 116 pages.

- Label words that occur anywhere in herbal text: 67 of 182
- Label words seen 2+ times in herbal text (tested in A1): 48

## A1. Are label words concentrated like names?

- Mean concentration of label words: **0.302**
- Same-frequency ordinary herbal words: 0.286 (10,000 draws)
- p = 0.106 → **FAIL**

## A2. Candidate anchors (descriptive, not a test)

| Label word | On pharmacy page(s) | Herbal count | Concentration | Herbal page |
|---|---|---:|---:|---|
| okeoly | f99r | 1 | 1.00 | f58v |
| arody | f88v | 1 | 1.00 | f40v |
| osain | f102v2 | 1 | 1.00 | f10r |
| chokam | f89v2 | 1 | 1.00 | f52r |
| opaldaiin | f89v1 | 1 | 1.00 | f58v |
| sory | f99r | 1 | 1.00 | f1r |
| sodar | f89r2 | 1 | 1.00 | f53r |
| arol | f99v | 1 | 1.00 | f40v |
| osal | f88r | 1 | 1.00 | f58r |
| darar | f99r | 1 | 1.00 | f58r |
| otair | f89v2 | 1 | 1.00 | f58v |
| olsy | f99v | 1 | 1.00 | f5r |
| oram | f88r | 1 | 1.00 | f33v |
| otaldy | f101v | 1 | 1.00 | f58r |
| sarol | f102v2 | 1 | 1.00 | f39v |
| cpheor | f88v | 1 | 1.00 | f17v |
| doly | f89r2 | 1 | 1.00 | f43v |
| okeeos | f100r | 1 | 1.00 | f26v |
| orar | f101v | 1 | 1.00 | f58r |
| otaly | f88r, f99v | 3 | 0.67 | f58r |

## Reading the result

- **A1 failed.** Pharmacy plant-part labels are no more concentrated on single herbal pages than ordinary words of
  the same frequency (0.302 vs 0.286, p = 0.11). Two-thirds of the label words (115 of 182) never appear in herbal
  text at all.
- **The candidate list is weak.** Almost all candidates were seen only once in herbal text, and a word seen once
  always has concentration 1.0. So the list does not single out names, and the planned side-by-side drawing
  comparison was not done: it would add impressions without evidence.
- **Extra check (added after the run, not pre-registered):** many candidates land on f58r/f58v, text-only pages
  the anomaly scan had flagged. They hold 6.6% of herbal words and 6.3% of label-word matches, which is no excess.
  Against random pharmacy-word sets of the same size, their hit rate gives p = 0.07. **Not a lead.**

Conclusion: no evidence that the plant-part labels are plant names that reappear in the herbal entries. Either the
labels are not names, the herbal text does not name its plant, or the two sections use different spellings.
