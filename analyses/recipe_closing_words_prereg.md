# Pre-registration: do recipe sections use a closing vocabulary? (October 2026)

Date: 2026-10-04. Written before the full analysis runs.

## Idea

Medieval recipes end entries with set phrases like *"probatum est"* (it is proven) or *"et sic"* (and so). If the Voynich recipe section follows this tradition, a small vocabulary of words should appear at the end of paragraphs far more often than chance, marking entry closures. This would be a formulaic system, like medieval recipe structure.

## Data

- **Words:** all words in the Biological and Stars/Recipes sections (`locus_type == 'P'`), cleaned.
- **Paragraph ends:** words where `is_para_end == True` (end of a paragraph).
- **Baseline:** the fraction of all recipe words that end a paragraph (expected by chance).

## Statistic

For each word appearing ≥3 times in the recipe sections:
- Count total occurrences and paragraph-final occurrences.
- Binomial test (one-sided): how unlikely is this many paragraph-ends if the word has the baseline probability?

## Prediction

A set of words (at least 5–10) will show p < 0.05, ending paragraphs 2–3× more often than baseline. This would suggest a recognized closing vocabulary.

## Threshold

p < 0.05 per word, uncorrected. At least 5 words with p < 0.05 count as support.

## Weakness

No prior hypothesis on which words should be closers, so this is partly exploratory. Multiple testing could inflate Type I error.
