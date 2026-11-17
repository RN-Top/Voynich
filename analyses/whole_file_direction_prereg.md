# Pre-registration: the whole integrated file, forwards and backwards

Written 17 November 2026, before running. Code: `analyses/whole_file_direction_test.py`.
Report: `output/whole_file_direction_report.md`.

## What is compared

Two copies of `voynich_integrated.json`, scored the same way:

- **Forwards:** the file as built.
- **Backwards:** a full flip. Pages in reverse order, lines on each page in reverse order, words in each
  line in reverse order, and letters in each word reversed. Labels and drawings stay with their page.

The script can save the backwards copy (`--save`) so other tests can be pointed at it.

## Why the earlier backwards test is not enough

`analyses/backwards_test.py` used only the writing. This test uses the text, the labels next to the
drawings, and the drawing type of each page together.

Many whole-file scores are the same in both copies and cannot decide anything. Examples: how many label
words also appear in their page's text, and which drawing type sits next to which. These are reported
as a check that the flip kept everything together. Only the scores below can differ between the copies.

## Score A: where a page's label words show up in its text

On pages with both labels and paragraph text, find every paragraph word that matches one of the page's
own label words. Measure where it falls in the page's paragraph text, from 0 (first word) to 1 (last).
In herbals and recipe books the thing being described is usually named at the start of its entry.

- Statistic: mean position of the matches. Null: shuffle word order within each page, 10,000 times.
- Score B is the same with the page's "topic words" in place of label words. Topic words are words used
  2+ times on the page and on no other page. Position is that of each word's first use.
  This covers the herbal pages, which mostly have no labels.
- For each copy, "names come first" means a mean position below the shuffled mean with p < 0.01.

## Decision

- **Forwards fits better:** forwards shows "names come first" on A or B and backwards shows it on neither.
- **Backwards fits better:** the reverse.
- **No preference:** both or neither show it, or A and B point different ways.
- Pages with no labels and no topic words are left out, and the report says how many.

Limits: A covers about 40 pages. Page order cannot change A or B, so this test says nothing about page
order. The earlier test showed that the text cannot settle page order.

Seed 408.
