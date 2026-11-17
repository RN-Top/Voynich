# Does the manuscript read better backwards?

Pre-registration: `analyses/backwards_prereg.md`. Code: `analyses/backwards_test.py` (seed 408). Data: `voynich_integrated.json` (ZL3b).

| Direction | Result |
|---|---|
| Words in a line | **left to right (forwards)** |
| Lines in a paragraph | **top to bottom (forwards)** |
| Letters in a word | **same direction as Latin/Italian (forwards)** |
| Pages in the book | **cannot be tested from the text** |

## Test 1: words in a line

3902 paragraph lines with 4+ words.

- Word length: first word 5.47 letters, middle words 5.01, last word 4.74. First minus last = +0.729, within-line shuffle p = < 1e-4.
- Ending in -m: 622 last words vs 15 first words. Difference in share = +0.1556, p = < 1e-4.
- Decision: **left to right (forwards)**.

## Test 2: lines in a paragraph

274 paragraphs with 3+ lines. Shortest line is the bottom line in 164, the top line in 7, a middle line in 88, tied in 15.
Binomial test bottom vs top: p = < 1e-4. Decision: **top to bottom (forwards)**.

## Test 3: letters in a word

L_k = ln(variety of word endings / variety of word beginnings), k letters. Below 0: endings less varied. Reading backwards flips the sign.

| Text | k=1 | k=2 | k=3 |
|---|---|---|---|
| italian_dante | -0.233 | -0.025 | -0.021 |
| latin_bede | -0.205 | -0.142 | -0.091 |
| latin_caesar | -0.227 | -0.161 | -0.092 |
| latin_isidore_plants | -0.202 | -0.142 | -0.080 |
| Voynich (EVA letters) | -0.242 [-0.262, -0.219] | -0.138 [-0.153, -0.121] | -0.096 [-0.109, -0.082] |
| Voynich (letter groups, robustness) | -0.256 [-0.275, -0.238] | -0.179 [-0.191, -0.165] | -0.092 [-0.103, -0.080] |

38692 Voynich words (words with unreadable or rare-character marks left out). Brackets: 95% interval from resampling pages.

Decision: **same direction as Latin/Italian (forwards)**.

## Test 4: pages in the book

207 pages have paragraph text. Pages that end without a paragraph end: f68r1, f84v. Pages that start without a paragraph start: none.
Fewer than 10 pages run on, so, as fixed in advance, **page direction cannot be tested from the text**. Almost every page starts and finishes its own text, so nothing in the writing shows which page comes next.

## Limits

- German could not be included as a reference (see `Data/reference/SOURCES.md`).
- Test 3 compares with Latin and Italian only. A language that puts its variety at word ends would look "mirrored" without being written backwards.
- Test 1's -m measure repeats a known result; the word-length measure is new.
