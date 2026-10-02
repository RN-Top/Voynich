# Pre-registration: writing types, word order, and where meaning sits in a word

Committed 2026-10-02, **before** either test below is run. Amend only below the line at the end.

## Why

The project author asks to (1) separate the different kinds of writing in the manuscript and (2) work
toward decoding it as a made-up (constructed) language. Decoding any unknown language starts with two
questions: does word order carry information (syntax), and which part of a word carries the topic (the
part a dictionary would be built from)?

## Writing types (ZL3b, canonical parser)

| Type | Words |
|---|---:|
| Paragraph text, Currier A | 11,362 |
| Paragraph text, Currier B | 23,676 |
| Ring text on circular diagrams (C) | 2,376 |
| Labels (L) | 1,190 |
| Radial text (R) | 354 |

Each type gets a descriptive profile (size, vocabulary, word length, common beginnings and endings, share of
its words also found in paragraph text). Tests run only on types with at least 1,500 usable word pairs.

## W1. Does word order carry information?

Statistic: mutual information (bits) between neighbouring words on the same line. Words seen fewer than 5
times in that type count as one "rare" word. **Known line-start and line-end habits are removed:** only
pairs where neither word is the first or last on its line are scored. The null shuffles those interior
words within their line (1,000 shuffles, seed 20261002), so only word order changes.

Result per type: excess MI over the shuffled mean, and p (one-sided). Order carries information if
p < 0.01. The size of the excess is reported for comparison between types.

## W2. Does the start or the end of a word carry the topic?

Paragraph text only. For each word take its **beginning** (first 2 letters) and its **ending** (last 2
letters). Statistic: mutual information between that part and the page's section (Herbal, Pharmaceutical,
Biological, Stars/Recipes, ...). Null: section labels are shuffled between pages **within the same Currier
language**, so the A/B difference does not count (2,000 shuffles, seed 20261002). Result: excess MI over the
null for beginnings and for endings, with p values.

Decision: whichever part has the larger excess with p < 0.01 is called the topic-carrying part. If both pass,
both are reported, with the larger one first. If neither passes, there is no detectable topic signal at this
level.

This does not tell a constructed language from a natural one: in both, roots carry topic and endings carry
grammar. It tells us where to look when building a dictionary.

---
Amendments (dated, below this line only):
