# Pre-registration: do flower colours line up with the text? ("the flowers are the keys")

Committed 2026-10-03, **before** any flower colour is recorded and before the test is run. Amend only below the
line at the end.

## Idea (from the project author)

In medieval correspondences, plants belonged to planets (often judged by flower colour), and planets ruled metals.
If the flowers are keys, plant pages whose flowers share a colour should share vocabulary.

## Step 1: colour classification (done first, by eye, from `uploads/yale_ms408_facsimile.pdf`)

For every Herbal-section page (parser section "Herbal"), record the dominant colour of the flower or bloom parts
(the topmost reproductive structures): **blue**, **red** (including brown-red), **yellow** (including tan and
gold), **white** (outline only, uncoloured), **green**, or **none** (no distinct flower). Pages where two colours
are equally prominent are recorded as **mixed**. The classification is saved to `analyses/flower_colours.csv`
**before** any text comparison is run.

## Step 2: test

Each page's paragraph text becomes a root-count vector (`analyses/root_dictionary_test.root_of`). Similarity is the
cosine between pages. Statistic: mean similarity of same-colour pairs minus mean similarity of different-colour
pairs. Only pages coloured blue, red, yellow, white or green are used (not mixed or none). Null: colour labels
shuffled among pages **within the same Currier language** (10,000 shuffles, seed 20261003). Pass: p < 0.01.

## Descriptive

Number of pages per colour. The opening words of the pages in each colour group.

---
Amendments (dated, below this line only):

**2026-10-03.** Step 1 done: all 118 Herbal pages classified by eye from contact sheets (about 380 px per page)
and saved in `analyses/flower_colours.csv` before any text comparison. Small or faint flowers make some calls
uncertain (notably white vs yellow, and red vs mixed).
