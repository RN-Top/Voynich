# Pre-registration: does the manuscript read better backwards?

Written 17 November 2026, before any of the tests below were run. Code: `analyses/backwards_test.py`.
Report: `output/backwards_report.md`.

## The idea

Some theories say the manuscript was flipped: written or bound so that it should be read the other way.
"Flipped" can mean four different things, and each gets its own test:

1. **Words in a line**: right to left instead of left to right.
2. **Lines in a paragraph**: bottom to top instead of top to bottom.
3. **Letters in a word**: mirror writing, each word spelled backwards.
4. **Pages in the book**: the book read back to front.

Turning the book upside down combines 1, 2 and 3.

## Why "which way reads better" needs care

Most text statistics give exactly the same answer forwards and backwards. For example, how predictable
the next word is, averaged over a long text, equals how predictable the previous word is. A test built on
those would always say "no difference" whatever the truth. So each test below uses something that does
have a direction: where a writer runs out of room, how a paragraph ends, or how known languages of the
time spell their words.

Data: `voynich_integrated.json` built from ZL3b (`build_integrated.py`), EVA letters. Only paragraph text is
used for tests 1, 2 and 4. All words are used for test 3. Seed 408.

## Test 1: words in a line

A writer who runs short of room squeezes the words at the end of the line they are writing towards.
If the lines were written left to right, the squeeze is on the right. If written right to left, it is on the left.

- Lines: paragraph lines with at least 4 words.
- Measures: (a) first word length minus last word length (EVA letters); (b) share of last words ending
  in -m minus share of first words ending in -m.
- Null: shuffle word order within each line, 10,000 times. Two-sided p.
- **Decision:** left to right if both measures are positive with p < 0.01. Right to left if both are
  negative with p < 0.01. Otherwise inconclusive.
- Known in advance: -m prefers line ends (VALIDATION.md, 605 of 861), so measure (b) is not blind.
  Measure (a) has not been looked at.

## Test 2: lines in a paragraph

A paragraph written top to bottom ends where the text runs out, so its last line is usually the short one.
Written bottom to top, the short line would be at the top.

- Paragraphs: paragraph units with at least 3 lines.
- Count paragraphs whose shortest line (EVA letters) is the bottom line (B) and those where it is the
  top line (T). Ties for shortest are left out.
- Null: under random line order the shortest line is as likely to be at the top as the bottom.
  Two-sided binomial test of B against T.
- **Decision:** top to bottom if B > T with p < 0.01. Bottom to top if T > B with p < 0.01.
  Otherwise inconclusive.
- Limit: ZL3b marks paragraph breaks partly from the page layout, so this is a check of the layout as
  much as of the text.

## Test 3: letters in a word (mirror writing)

In Latin and Italian, the languages most often proposed for the manuscript's setting, words end in a
small set of endings (-us, -um, -is, -o, -a…) while their beginnings vary much more. Spelled backwards,
that pattern flips.

- Measure for a text: L_k = ln( H(last k letters) / H(first k letters) ), where H is the entropy of the
  word-ending or word-beginning, over word tokens of length at least k+1, for k = 1, 2, 3.
  Below 0 means endings are less varied than beginnings. Reading backwards gives exactly −L_k.
- Baselines: four reference texts in `Data/reference/` (Caesar, Isidore on plants, Bede, Dante).
- Voynich: L_k with a 95% interval from resampling pages (2,000 times).
- **Decision:** first, every reference text must have L_k < 0 for k = 1, 2, 3. If not, the test is void.
  Then: Voynich's interval entirely below 0 for every k means the letters run the same way as the
  reference languages, so mirror reading makes it *less* like them. Entirely above 0 for every k means it
  looks like those languages spelled backwards. Otherwise inconclusive.
- Robustness, not part of the decision: repeat with common EVA letter groups counted as single
  letters (ch, sh, cth, ckh, cph, cfh, iin, ii, ee).
- Limit: some real languages put their variety at the end of words. A "mirror" result would show the
  text is unlike Latin and Italian, not that it was written backwards.

## Test 4: pages in the book

The only text clue to page order would be paragraphs that run from one page onto the next.

- Before writing this I counted: only 2 of 207 pages with paragraph text end without a paragraph end.
- **Decision fixed in advance:** if fewer than 10 pages end mid-paragraph, page direction cannot be
  tested from the text, and the report says so and lists those pages. If 10 or more, compare how
  often an open-ended page is followed by a page that starts mid-paragraph, forwards against backwards
  (Fisher exact test, p < 0.01).

## Overall

"Reads better backwards" is supported for a direction only if that direction's test gives the reversed
result. Inconclusive and void results are reported as they are, not counted either way.
